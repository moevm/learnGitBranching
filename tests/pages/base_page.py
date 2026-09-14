import json
import time
from dataclasses import dataclass
from typing import Iterable

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


@dataclass(frozen=True)
class CommandResult:
    raw: str
    status: str
    result: str
    error: str

    @property
    def failed(self) -> bool:
        command_result = "Command Result" in self.error
        return not command_result and (bool(self.error) or self.status == "error")


class BasePage:
    """Пользовательские действия в Learn Git Branching и переход из Moodle."""

    COMMAND_INPUT = (By.ID, "commandTextField")
    LEVEL_IDS = {
        "rampup/cherryPick": "move1",
        "rampup/interactiveRebase": "move2",
        "mixed/grabbingOneCommit": "mixed1",
        "mixed/jugglingCommits": "mixed2",
        "mixed/jugglingCommits2": "mixed3",
        "mixed/tags": "mixed4",
        "mixed/describe": "mixed5",
        "rebase/manyRebases": "advanced1",
    }

    def __init__(self, driver, settings):
        self.driver = driver
        self.settings = settings
        self.wait = WebDriverWait(driver, settings.command_timeout)

    def open_level(self, level_id: str) -> None:
        expected_id = self.LEVEL_IDS.get(level_id, level_id)
        self._open_application()
        self._wait_for_application()
        self._dismiss_ads()
        self._dismiss_start_dialogs()
        self._enter_command_text(
            f"level {expected_id} --noFinishDialog --noIntroDialog"
        )
        self.wait_for_js(
            """
(() => {
  const sandbox = window.debug_Main_getSandbox && debug_Main_getSandbox();
  return sandbox && sandbox.currentLevel &&
    sandbox.currentLevel.level && sandbox.currentLevel.level.id === arguments[0];
})()
""",
            expected_id,
        )
        self.wait_for_command_queue()
        self._close_visible_modal()
        self.wait_until_idle()

    def wait_for_command_queue(self) -> None:
        self.wait.until(
            lambda driver: driver.execute_script(
                """
const sandbox = window.debug_Main_getSandbox && debug_Main_getSandbox();
if (!sandbox || !sandbox.commandCollection) return false;
return sandbox.commandCollection.models.every((command) => {
  const status = command.get('status');
  return status !== 'inqueue' && status !== 'processing';
});
"""
            ),
            message="LearnGitBranching command queue did not become idle",
        )

    def run(self, command: str) -> CommandResult:
        self._submit(command)
        return self.command_result(command)

    def run_many(self, commands: Iterable[str]) -> list[CommandResult]:
        return [self.run(command) for command in commands]

    def interactive_rebase(
        self, base_ref: str, ordering: Iterable[str]
    ) -> CommandResult:
        command = f"git rebase -i {base_ref}"
        wanted_order = list(ordering)
        self._enter_command_text(command)
        self.wait_for_js(
            """
(() => {
  const sandbox = window.debug_Main_getSandbox && debug_Main_getSandbox();
  return sandbox && sandbox.commandCollection.models.some(
    item => item.get('rawStr') === arguments[0]
  );
})()
""",
            command,
        )
        self.wait_for_js(
            "document.querySelector('.modalView.inFront.show .rebaseEntries')"
        )
        self.driver.execute_script(
            """
const wantedOrder = arguments[0];
const modal = document.querySelector('.modalView.inFront.show');
const list = modal.querySelector('.rebaseEntries');
const entries = Object.fromEntries(
  Array.from(list.querySelectorAll('.rebaseEntry')).map(entry => [entry.id, entry])
);

for (const commitId of wantedOrder) {
  const entry = entries[commitId];
  if (!entry) throw new Error(`Commit ${commitId} is absent from rebase dialog`);
  list.appendChild(entry);
}

for (const entry of Array.from(list.querySelectorAll('.rebaseEntry'))) {
  if (!wantedOrder.includes(entry.id)) entry.querySelector('button').click();
}

modal.querySelector('.confirmButton').click();
""",
            wanted_order,
        )
        self._wait_for_command_completion(command)
        self.wait_until_idle()
        return self.command_result(command)

    def wait_for_level_success(self, level_id: str) -> None:
        expected_id = self.LEVEL_IDS.get(level_id, level_id)
        self.wait_for_js(
            "window.debug_LevelStore_isLevelSolved && "
            "debug_LevelStore_isLevelSolved(arguments[0])",
            expected_id,
        )

    def is_level_solved(self, level_id: str) -> bool:
        expected_id = self.LEVEL_IDS.get(level_id, level_id)
        return bool(
            self.driver.execute_script(
                "return Boolean(window.debug_LevelStore_isLevelSolved && "
                "debug_LevelStore_isLevelSolved(arguments[0]));",
                expected_id,
            )
        )

    def graph_text(self) -> str:
        return self.driver.execute_script(
            "const graph = document.querySelector('svg'); "
            "return graph ? graph.textContent : '';"
        )

    def terminal_output(self) -> str:
        return self.driver.execute_script(
            "const terminal = document.querySelector('#commandDisplay'); "
            "return terminal ? terminal.innerText : '';"
        )

    def command_result(self, command: str) -> CommandResult:
        raw = self.driver.execute_script(
            """
const commands = debug_Main_getSandbox().commandCollection.models;
const matching = commands.filter(item => item.get('rawStr') === arguments[0]);
const item = matching[matching.length - 1];
if (!item) return JSON.stringify(null);
const error = item.get('error');
return JSON.stringify({
  raw: item.get('rawStr') || '',
  status: item.get('status') || '',
  result: item.get('result') || '',
  error: error ? (error.message || error.toString()) : ''
});
""",
            command,
        )
        payload = json.loads(raw)
        if payload is None:
            raise AssertionError(f"Команда не найдена в истории: {command}")
        return CommandResult(**payload)

    def wait_until_idle(self) -> None:
        try:
            self.wait_for_js(
                "!window.debug_GlobalStateStore_getIsAnimating || "
                "!debug_GlobalStateStore_getIsAnimating()",
                timeout=15,
            )
        except TimeoutException:
            pass

    def wait_for_js(self, expression: str, *args, timeout: int | None = None) -> None:
        wait = WebDriverWait(self.driver, timeout or self.settings.command_timeout)
        wait.until(
            lambda driver: bool(
                driver.execute_script(f"return Boolean({expression});", *args)
            )
        )

    def _open_application(self) -> None:
        if not self.settings.moodle_course_url:
            self.driver.get(self.settings.target_url)
            return

        self.driver.get(self.settings.moodle_course_url)
        self._login_to_moodle_if_needed()
        if self._has_command_input():
            return
        self._open_moodle_activity()

    def _login_to_moodle_if_needed(self) -> None:
        if not self._has_element(By.ID, "username"):
            return
        if not self.settings.moodle_username or not self.settings.moodle_password:
            raise RuntimeError(
                "Moodle запросил авторизацию, но MOODLE_USERNAME или "
                "MOODLE_PASSWORD не заполнены"
            )
        self.driver.find_element(By.ID, "username").send_keys(
            self.settings.moodle_username
        )
        self.driver.find_element(By.ID, "password").send_keys(
            self.settings.moodle_password
        )
        self.driver.find_element(By.ID, "loginbtn").click()
        WebDriverWait(self.driver, self.settings.command_timeout).until(
            lambda driver: not self._has_element(By.ID, "username")
        )
        if self.driver.current_url != self.settings.moodle_course_url:
            self.driver.get(self.settings.moodle_course_url)

    def _open_moodle_activity(self) -> None:
        if self.settings.moodle_activity_url:
            self.driver.get(self.settings.moodle_activity_url)
        else:
            activity = self._find_activity_link()
            existing_windows = set(self.driver.window_handles)
            activity.click()
            self._switch_to_new_window(existing_windows)
        self._switch_to_application_frame()

    def _find_activity_link(self):
        activity_name = self.settings.moodle_activity_name.casefold()

        def locate(driver):
            links = driver.find_elements(
                By.CSS_SELECTOR,
                "a[href*='/mod/lti/view.php'], .activityinstance a, "
                "a[href*='/mod/url/view.php']",
            )
            matching = [
                link for link in links if activity_name in (link.text or "").casefold()
            ]
            return matching[0] if matching else False

        try:
            return self.wait.until(locate)
        except TimeoutException as exc:
            raise RuntimeError(
                "Элемент LearnGitBranching не найден на странице курса. "
                "Укажите точное MOODLE_ACTIVITY_NAME или MOODLE_ACTIVITY_URL"
            ) from exc

    def _switch_to_new_window(self, existing_windows: set[str]) -> None:
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: bool(set(driver.window_handles) - existing_windows)
            )
        except TimeoutException:
            return
        new_window = (set(self.driver.window_handles) - existing_windows).pop()
        self.driver.switch_to.window(new_window)

    def _switch_to_application_frame(self) -> None:
        if self._has_command_input():
            return

        def find_frame(driver):
            driver.switch_to.default_content()
            for frame in driver.find_elements(By.TAG_NAME, "iframe"):
                driver.switch_to.default_content()
                driver.switch_to.frame(frame)
                if self._has_command_input():
                    return True
            driver.switch_to.default_content()
            return False

        if not self.wait.until(find_frame):
            raise RuntimeError("Интерфейс LearnGitBranching не найден в элементе Moodle")

    def _wait_for_application(self) -> None:
        self.wait.until(lambda driver: self._has_command_input())
        self.wait_for_js("window.debug_Main_getSandbox")

    def _dismiss_start_dialogs(self) -> None:
        for _ in range(10):
            clicked = self.driver.execute_script(
                """
const modal = document.querySelector('.modalView.inFront.show');
if (!modal) return false;
const buttons = Array.from(modal.querySelectorAll('button'));
const button = buttons.find(item => /^(Next|OK|Далее|ОК)$/i.test(item.innerText.trim())) ||
  modal.querySelector('.icon-circle-arrow-right, .icon-ok, .toolbar .controls .close');
if (!button) return false;
button.click();
return true;
"""
            )
            if not clicked:
                break
            time.sleep(0.25)

    def _dismiss_ads(self) -> None:
        self.driver.execute_script(
            """
const dismiss = document.querySelector('#biteReadUpsellDismiss');
if (dismiss) dismiss.click();
"""
        )

    def _close_visible_modal(self) -> None:
        self.driver.execute_script(
            """
const modal = document.querySelector('.modalView.inFront.show');
if (!modal) return;
const close = modal.querySelector('.toolbar .controls .close, .close');
if (close) close.click();
"""
        )

    def _submit(self, command: str) -> None:
        self._enter_command_text(command)
        self._wait_for_command_completion(command)
        self.wait_until_idle()

    def _wait_for_command_completion(self, command: str) -> None:
        self.wait_for_js(
            """
(() => {
  const sandbox = window.debug_Main_getSandbox && debug_Main_getSandbox();
  if (!sandbox) return false;
  const matches = sandbox.commandCollection.models.filter(
    item => item.get('rawStr') === arguments[0]
  );
  const latest = matches[matches.length - 1];
  return latest && !['inqueue', 'processing'].includes(latest.get('status'));
})()
""",
            command,
        )

    def _enter_command_text(self, command: str) -> None:
        self._close_visible_modal()
        self.wait.until(lambda driver: driver.find_element(*self.COMMAND_INPUT))
        self.driver.execute_script(
            """
const field = document.querySelector('#commandTextField');
field.focus();
field.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
"""
        )
        self.wait.until(
            lambda driver: driver.execute_script(
                "return document.activeElement && document.activeElement.id"
            )
            == "commandTextField"
        )
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).send_keys(Keys.BACKSPACE).send_keys(command).send_keys(Keys.ENTER).perform()

    def _has_command_input(self) -> bool:
        return bool(self.driver.find_elements(*self.COMMAND_INPUT))

    def _has_element(self, by: str, value: str) -> bool:
        return bool(self.driver.find_elements(by, value))
