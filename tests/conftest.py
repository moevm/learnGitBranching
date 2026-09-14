import json
import os
import time
import urllib.request
from dataclasses import dataclass

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tests.pages.learn_git_page import LearnGitPage


@dataclass(frozen=True)
class TestSettings:
    selenium_url: str
    target_url: str
    moodle_course_url: str
    moodle_username: str
    moodle_password: str
    moodle_activity_name: str
    moodle_activity_url: str
    command_timeout: int


@pytest.fixture(scope="session")
def settings() -> TestSettings:
    return TestSettings(
        selenium_url=os.getenv(
            "SELENIUM_REMOTE_URL", "http://selenium-hub:4444/wd/hub"
        ),
        target_url=os.getenv(
            "TARGET_URL", "https://learngitbranching.js.org/?locale=ru_RU&NODEMO"
        ),
        moodle_course_url=os.getenv("MOODLE_COURSE_URL", ""),
        moodle_username=os.getenv("MOODLE_USERNAME", ""),
        moodle_password=os.getenv("MOODLE_PASSWORD", ""),
        moodle_activity_name=os.getenv("MOODLE_ACTIVITY_NAME", "LearnGitBranching"),
        moodle_activity_url=os.getenv("MOODLE_ACTIVITY_URL", ""),
        command_timeout=int(os.getenv("SELENIUM_COMMAND_TIMEOUT", "40")),
    )


@pytest.fixture
def driver(settings: TestSettings):
    _wait_for_selenium(settings.selenium_url)
    options = Options()
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-dev-shm-usage")
    if os.getenv("LOCAL_HEADLESS", "").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")
    if settings.selenium_url.lower() == "local":
        browser = webdriver.Chrome(options=options)
    else:
        browser = webdriver.Remote(
            command_executor=settings.selenium_url,
            options=options,
        )
    browser.implicitly_wait(0)
    yield browser
    browser.quit()


@pytest.fixture
def git_page(driver, settings: TestSettings) -> LearnGitPage:
    page = LearnGitPage(driver, settings)
    return page


def _wait_for_selenium(selenium_url: str) -> None:
    if selenium_url.lower() == "local":
        return
    status_url = selenium_url.removesuffix("/wd/hub") + "/status"
    last_error = None
    for _ in range(60):
        try:
            with urllib.request.urlopen(status_url, timeout=2) as response:
                payload = json.loads(response.read().decode("utf-8"))
                if response.status == 200 and payload.get("value", {}).get("ready"):
                    return
        except Exception as exc:  # Grid может ещё запускаться.
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"Selenium Grid недоступен: {selenium_url}") from last_error
