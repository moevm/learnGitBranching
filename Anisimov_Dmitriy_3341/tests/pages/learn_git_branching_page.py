import json
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://learngitbranching.js.org/"
TYPE_DELAY_SECONDS = 0.08
ACTION_DELAY_SECONDS = 1.0
AFTER_ENTER_DELAY_SECONDS = 3.0


class LearnGitBranchingPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def open_level(self, level_id):
        self.driver.get(f"{BASE_URL}?locale=ru_RU")
        self.wait_for_js("window.debug_Main_getSandbox && document.querySelector('#commandTextField')")
        self._dismiss_ads()
        self.skip_start_dialogs()
        self.click_level(level_id)
        self.skip_level_dialogs()
        self.sleep(3)
        self.hide_goal_if_visible()
        self.wait_for_command_queue()
        self.wait_until_idle()

    def skip_start_dialogs(self):
        for _ in range(3):
            self.click_active_modal_next_or_ok()
            self.sleep(2.4)
        self.sleep(3)

    def click_level(self, level_id):
        selector = f"#levelIcon-{level_id}"
        self.wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, selector).is_displayed())
        self.driver.find_element(By.CSS_SELECTOR, selector).click()
        self.sleep(ACTION_DELAY_SECONDS)

    def skip_level_dialogs(self):
        self.wait_for_js("document.querySelector('.modalView.inFront.show .terminal-window-holder .toolbar .controls .close')")
        self.driver.execute_script(
            """
const closeButton = document.querySelector(
  '.modalView.inFront.show .terminal-window-holder .toolbar .controls .close'
);
if (closeButton) closeButton.click();
"""
        )
        self.sleep(2)

    def click_active_modal_next_or_ok(self):
        self.wait_for_js(
            """
Array.from(document.querySelectorAll('.modalView.inFront.show button'))
  .find(button => /\\b(Next|OK)\\b/.test(button.innerText))
"""
        )
        self.driver.execute_script(
            """
const button = Array.from(document.querySelectorAll('.modalView.inFront.show button'))
  .find(button => /\\b(Next|OK)\\b/.test(button.innerText));
if (button) button.click();
"""
        )

    def run(self, command, wait_for_finish=True):
        self._focus_command_line()
        self._send_keys(Keys.CONTROL, "a")
        self._send_keys(Keys.BACKSPACE)
        self.sleep(ACTION_DELAY_SECONDS)

        for char in command:
            self._send_keys(char)
            time.sleep(TYPE_DELAY_SECONDS)

        self._send_keys(Keys.ENTER)
        self.wait_for_js(f"debug_CommandLineStore_getCommandHistory()[0] === {json.dumps(command)}")
        self.sleep(AFTER_ENTER_DELAY_SECONDS)
        if wait_for_finish:
            self._wait_for_latest_command_to_finish(command)
        self.wait_until_idle()
        return self.last_command()

    def _focus_command_line(self):
        self._close_active_modal_if_visible()
        self.driver.find_element(By.ID, "commandTextField")
        self.driver.execute_script(
            """
const field = document.querySelector('#commandTextField');
field.focus();
field.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
"""
        )
        self.wait.until(lambda driver: driver.execute_script("return document.activeElement && document.activeElement.id") == "commandTextField")
        self.sleep(ACTION_DELAY_SECONDS)

    def _send_keys(self, *keys):
        if len(keys) == 2 and keys[0] == Keys.CONTROL:
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(keys[1]).key_up(Keys.CONTROL).perform()
            return
        ActionChains(self.driver).send_keys(*keys).perform()

    def _close_active_modal_if_visible(self):
        self.driver.execute_script(
            """
const modal = document.querySelector('.modalView.inFront.show');
if (!modal) return;
const closeButton = modal.querySelector('.toolbar .controls .close, .close');
if (closeButton) closeButton.click();
"""
        )
        self.sleep(ACTION_DELAY_SECONDS)

    def wait_for_command_queue(self):
        try:
            self.wait_for_js(
                """
(() => {
  const commands = debug_Main_getSandbox().commandCollection.models;
  return commands.every(command => !['inqueue', 'processing'].includes(command.get('status')));
})()
""",
                timeout=20,
            )
        except TimeoutException:
            self.sleep(ACTION_DELAY_SECONDS)

    def hide_goal_if_visible(self):
        self.driver.execute_script(
            """
const button = document.querySelector('.showGoalWrapper button');
if (button) button.click();
"""
        )
        self.sleep(ACTION_DELAY_SECONDS)

    def wait_for_level_success(self, level_id):
        self.wait_for_js(f"debug_LevelStore_isLevelSolved({json.dumps(level_id)})", timeout=45)
        self.sleep(3)

    def wait_until_idle(self):
        try:
            self.wait_for_js("!debug_GlobalStateStore_getIsAnimating()", timeout=15)
        except TimeoutException:
            pass
        self.sleep(ACTION_DELAY_SECONDS)

    def svg_text(self):
        return self.driver.execute_script("return document.querySelector('svg').textContent;")

    def last_command(self):
        raw = self.driver.execute_script(
            """
const commands = debug_Main_getSandbox().commandCollection.models;
const command = commands[commands.length - 1];
if (!command) return JSON.stringify(null);
const error = command.get('error');
return JSON.stringify({
  raw: command.get('rawStr'),
  status: command.get('status'),
  result: command.get('result') || '',
  error: error ? (error.message || error.toString()) : ''
});
"""
        )
        return json.loads(raw)

    def is_level_solved(self, level_id):
        return bool(self.driver.execute_script(f"return debug_LevelStore_isLevelSolved({json.dumps(level_id)})"))

    def wait_for_js(self, expression, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: bool(driver.execute_script(f"return Boolean({expression});"))
        )

    def _wait_for_latest_command_to_finish(self, command):
        escaped_command = json.dumps(command)
        self.wait_for_js(
            f"""
(() => {{
  const commands = debug_Main_getSandbox().commandCollection.models;
  const latest = commands[commands.length - 1];
  if (!latest || latest.get('rawStr') !== {escaped_command}) return false;
  return !['inqueue', 'processing'].includes(latest.get('status'));
}})()
""",
            timeout=30,
        )

    def _dismiss_ads(self):
        self.driver.execute_script(
            """
const dismiss = document.querySelector('#biteReadUpsellDismiss');
if (dismiss) dismiss.click();
"""
        )

    def sleep(self, seconds):
        time.sleep(seconds)
