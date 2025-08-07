import os
import logging
import sys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Cookie_Clicker
import Driver_Initializer
import Form_Fillout
from Autostarter import save_last_upload_timestamp, check_if_uploaded_today, add_to_autostart, is_program_in_autostart
import traceback

class Schwarzwaelder:
    def __init__(self, env_file=".env"):
        self._load_env(env_file)
        self.url = os.getenv("SWR_LOGIN_URL", "https://www.schwarzwaldradio.com/wetter-melden/")
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.timeout = int(os.getenv("SWR_TIMEOUT", 10))
        self.city = os.getenv("CITY")
        self.state = os.getenv("STATE")
        self.headless = os.getenv("HEADLESS", "False").lower() in ("1", "true", "yes")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            stream=sys.stdout
        )
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _load_env(filename):
        """Reads plain-text .env file and sets os.environ entries."""
        if getattr(sys, "frozen", False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(__file__)
        path = os.path.join(base, filename)
        try:
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    key, val = line.split("=", 1)
                    os.environ[key] = val
        except FileNotFoundError:
            print(f"No {filename} found at {path!r}")

    def _wait_for_ready(self, driver):
        """Wait until document.readyState is 'complete'."""
        WebDriverWait(driver, self.timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def _click_anmelde(self, driver):
        """Opens the login dialog by clicking the 'Anmelden' button."""
        self.logger.info("Opening login dialog...")
        WebDriverWait(driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Anmelden']]")
        )).click()

    def _login(self, driver):
        """Fills and submits the login form."""
        self.logger.info("Filling login credentials...")
        email_field = WebDriverWait(driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))
        )
        email_field.clear()
        email_field.send_keys(self.email)

        pw_field = WebDriverWait(driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
        )
        pw_field.clear()
        pw_field.send_keys(self.password)

        self.logger.info("Submitting login form...")
        WebDriverWait(driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Anmelden']]")
        )).click()

    def run(self):
        if not self.email or not self.password or not self.city or not self.state:
            raise EnvironmentError("Environment variables must be set!. Open the .env file and fill out the credentials!")

        driver = None
        try:
            driver = Driver_Initializer.initialize_driver(self.headless)
            driver.get(self.url)
            self.logger.info(f"Loaded URL: {self.url}")

            self._wait_for_ready(driver)
            cookie_mgr = Cookie_Clicker.CookieManager(driver)
            cookie_mgr.try_accept_cookies()

            self._click_anmelde(driver)
            self._login(driver)
            sleep(2)
            cookie_mgr.try_accept_cookies()

            self._wait_for_ready(driver)
            self.logger.info("Login successful, filling weather form...")

            Form_Fillout.fillout_form(driver, self.city, self.state)
            self.logger.info("Weather form submitted successfully.")

        except Exception as e:
            self.logger.exception(f"Error during workflow execution: {e}")
        finally:
            if driver:
                driver.quit()
                self.logger.info("Driver closed.")
            return True

if __name__ == "__main__":
    retries = 3
    while retries > 0:
        try:
            log_path = os.path.join(os.path.dirname(sys.executable), "last_upload.txt")
            add_to_autostart(sys.executable)

            check_if_uploaded_today(log_path)
            app = Schwarzwaelder()
            app.run()
            save_last_upload_timestamp(log_path)
            print("Successfully finished!")
            sys.exit(0)
        except EnvironmentError as e:
            sys.exit(1)
        except Exception as e:
            traceback.print_exc()
            retries -= 1
            print("An error occurred!. Retrying...")

    input("Failed to send form successfully 3 times! Press Enter to exit...")
