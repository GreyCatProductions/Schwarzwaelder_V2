import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Weather_API import get_weather

logging.basicConfig(level=logging.INFO)
TIMEOUT = 10

class WeatherFormPage:
    CITY_INPUT     = (By.ID,    "cf_city")
    STATE_SELECT   = (By.ID,    "cf_state")
    TEMP_INPUT     = (By.ID,    "cf_temperature")
    WEATHER_SELECT = (By.ID,    "cf_weather_condition")
    PRIVACY_LABEL  = (By.CSS_SELECTOR, "label[for='cf_privacy']")
    SUBMIT_BTN     = (By.XPATH, "//input[@type='submit' and @value='Abschicken']")

    def __init__(self, driver):
        self.driver = driver

    def _load_and_scroll(self, locator):
        """
        Wait for presence of the element, scroll it into view, and return it.
        """
        elem = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(locator)
        )
        # Scroll element to center of view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", elem
        )
        return elem

    def wait_clickable(self, locator):
        """
        Load, scroll, then wait for clickable and return element.
        """
        self._load_and_scroll(locator)
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(locator)
        )

    def fill_city(self, city: str) -> None:
        logging.info(f"Fülle Stadt: {city}")
        elem = self.wait_clickable(self.CITY_INPUT)
        elem.clear()
        elem.send_keys(city)

    def fill_state(self, state: str) -> None:
        logging.info(f"Wähle Bundesland: {state}")
        dropdown = self.wait_clickable(self.STATE_SELECT)
        Select(dropdown).select_by_visible_text(state)

    def fill_temperature(self, temperature: str) -> None:
        logging.info(f"Füge Temperatur ein: {temperature}")
        elem = self.wait_clickable(self.TEMP_INPUT)
        elem.clear()
        elem.send_keys(temperature)

    def fill_weather(self, weather: str) -> None:
        logging.info(f"Wähle Wetterbedingung: {weather}")
        dropdown = self.wait_clickable(self.WEATHER_SELECT)
        Select(dropdown).select_by_visible_text(weather)

    def accept_privacy(self) -> None:
        logging.info("Akzeptiere Datenschutz")
        elem = self.wait_clickable(self.PRIVACY_LABEL)
        elem.click()

    def submit(self) -> None:
        logging.info("Sende Formular ab")
        btn = self.wait_clickable(self.SUBMIT_BTN)
        btn.click()


def fillout_form(driver, city: str, state: str):
    """
    High-level function to fill out the weather form.
    """
    page = WeatherFormPage(driver)
    try:
        temperature, weather = get_weather(city)

        time.sleep(1)
        page.fill_city(city)
        time.sleep(1)
        page.fill_state(state)
        time.sleep(1)
        page.fill_temperature(str(temperature))
        time.sleep(1)
        page.fill_weather(weather)
        time.sleep(1)
        page.accept_privacy()
        time.sleep(1)
        page.submit()

    except TimeoutException as e:
        logging.error(f"Element nicht gefunden oder nicht klickbar: {e}")
        raise
