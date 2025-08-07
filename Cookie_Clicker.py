import logging
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout
)

class CookieManager:
    def __init__(self, driver, timeout: int = 3):
        self.driver = driver
        self.timeout = timeout
        self.accepted = False

    def try_accept_cookies(self) -> None:
        if self.accepted:
            return

        try:
            shadow_host = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#usercentrics-root"))
            )
            logging.info("Accepting cookies...")
            button = self.driver.execute_script(
                "const root = arguments[0].shadowRoot;"
                "return root.querySelector('button[data-testid=\\'uc-accept-all-button\\']');",
                shadow_host
            )
            if button:
                button.click()
                self.accepted = True
                logging.info("Cookies accepted")
            else:
                logging.info("Accept button not found inside banner")
        except Exception:
            logging.info("No cookie banner found or error during acceptance; continuing.")
