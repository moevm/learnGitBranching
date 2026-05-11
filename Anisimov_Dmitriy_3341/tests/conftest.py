import os
import json
import time
import urllib.request

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tests.pages.learn_git_branching_page import LearnGitBranchingPage


@pytest.fixture(scope="session")
def selenium_url():
    return os.getenv("SELENIUM_REMOTE_URL", "http://selenium-hub:4444/wd/hub")


@pytest.fixture
def driver(selenium_url):
    options = Options()
    options.add_argument("--window-size=1440,1000")
    browser = _create_remote_driver(selenium_url, options)
    browser.implicitly_wait(0)
    yield browser
    browser.quit()


@pytest.fixture
def lgb(driver):
    return LearnGitBranchingPage(driver)


def _create_remote_driver(selenium_url, options):
    _wait_for_selenium_status(selenium_url)
    return webdriver.Remote(command_executor=selenium_url, options=options)


def _wait_for_selenium_status(selenium_url):
    status_url = selenium_url.removesuffix("/wd/hub") + "/status"
    last_error = None
    for _ in range(60):
        try:
            with urllib.request.urlopen(status_url, timeout=2) as response:
                status = json.loads(response.read().decode("utf-8"))
                if response.status == 200 and status.get("value", {}).get("ready"):
                    return
        except Exception as exc:
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"Selenium Grid is not available at {selenium_url}") from last_error
