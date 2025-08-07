import datetime
import os
import sys
import winreg as reg


def add_to_autostart(executable_path):
    program_name = os.path.basename(executable_path)

    if is_program_in_autostart(program_name):
        print("Already in autostart!")
        return

    try:
        registry_key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with reg.OpenKey(registry_key, key_path, 0, reg.KEY_WRITE) as key:
            reg.SetValueEx(key, program_name, 0, reg.REG_SZ, executable_path)
        print(f"{program_name} has been added to autostart.")
    except Exception as e:
        print(f"Failed to add to autostart: {str(e)}")

def is_program_in_autostart(program_name) -> bool:
    try:
        registry_key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with reg.OpenKey(registry_key, key_path, 0, reg.KEY_READ) as key:
            try:
                reg.QueryValueEx(key, program_name)
                return True  #
            except FileNotFoundError:
                return False
    except Exception as e:
        print(f"Error reading the registry: {str(e)}")
        return False

def check_if_uploaded_today(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
                last_upload_date = file.read().strip()

        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if last_upload_date == today_date:
            print("Data has already been uploaded today. Exiting.")
            sys.exit(0)

def save_last_upload_timestamp(path):
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(path, "w") as file:
        file.write(today_date)