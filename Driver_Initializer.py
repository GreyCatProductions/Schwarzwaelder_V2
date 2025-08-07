from selenium import webdriver

def initialize_driver(headless: bool) -> webdriver:
    tries = 5
    cooldown = 30

    while tries > 0:
        try:
            opts = webdriver.FirefoxOptions()
            opts.headless = headless
            driver = webdriver.Firefox(options=opts)
            return driver
        except Exception as e:
            print(f"Error initializing driver. Retrying: {e}")
            tries -= 1

    return None