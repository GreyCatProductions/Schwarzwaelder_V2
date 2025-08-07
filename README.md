# Schwarzwaelder

**Automated Weather Reporter for Schwarzwaldradio**

This tool automatically logs into Schwarzwaldradio’s Wetterwaechter portal and submits the current weather for your city every day using Selenium and the OpenWeatherMap API.

---

## Features

- **Headless or GUI mode**  
  Run in headless mode (no browser window) or with a visible Firefox window.

- **Automatic login & form fill**  
  - Clicks through the cookie banner (`Cookie_Clicker.py`) 
  - Opens the login dialog and submits credentials from your `.env`
  - Fills city, state, temperature & weather condition (`Form_Fillout.py`) 

- **Weather lookup**  
  Uses OpenWeatherMap to fetch temperature & map weather codes to German Schwarzwaldradio specific descriptions (`Weather_API.py`)

- **Daily-run guard**  
  Skips submission if already run today (`Autostarter.py`) 

- **Windows autostart**  
  Installs itself into your registry so it runs on login. You do not need to upload the weather anymore this will do it for you when you start the pc

---

## Requirements

- Registered account at https://www.schwarzwaldradio.com/schwarzwaldtaler-profil/
- Python 3.9+ (Should work with older ones too)
- [Firefox](https://www.mozilla.org/firefox/)

## How to install?
1. Download the DOWNLOAD_ME folder
2. Open it, make sure its unzipped
4. Fill out the data in .env. Make sure the account you type in is registered.
5. Run Schwarzwaelder.exe
6. Schwarzwaelder.exe will add itself to windows autostart. You will not need to run it anymore
