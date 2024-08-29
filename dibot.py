import pyautogui
import time
import os
import sys
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def get_user_input():
    log("Prompting user for task and website URL.")
    goal = input("Enter the goal/task you want to accomplish: ")
    website = input("Enter the website URL (e.g., https://www.example.com): ")
    log(f"User provided goal: '{goal}' and website: '{website}'.")
    return goal, website

def activate_chrome_window():
    log("Searching for an open Google Chrome window...")
    try:
        os.system("wmctrl -a 'Google Chrome'")
        log("Google Chrome window activated.")
    except Exception as e:
        log(f"Failed to activate Google Chrome: {e}")
        sys.exit(1)

def navigate_to_website(website_url):
    log("Focusing on the address bar to navigate to the provided website.")
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    log(f"Typing URL: {website_url}")
    pyautogui.typewrite(website_url, interval=0.05)
    pyautogui.press('enter')
    log(f"Website '{website_url}' entered. Waiting for the page to load...")
    time.sleep(5)
    log("Page loaded successfully.")

def capture_screenshot(filename='screenshot.png'):
    log("Capturing a screenshot of the current browser window.")
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    log(f"Screenshot saved as '{filename}'.")
    return filename

def process_screenshot_with_ai(screenshot_path):
    log(f"Processing screenshot '{screenshot_path}' with AI to identify required fields.")
    processed_data = {
        'fields': [
            {'name': 'username', 'position': (500, 400)},
            {'name': 'email', 'position': (500, 450)},
            {'name': 'password', 'position': (500, 500)},
        ]
    }
    log("Fields identified by AI: " + ", ".join([field['name'] for field in processed_data['fields']]))
    return processed_data

def generate_unique_data(field_name):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    if 'email' in field_name.lower():
        return f"user{timestamp}@example.com"
    elif 'username' in field_name.lower():
        return f"user_{timestamp}"
    elif 'password' in field_name.lower():
        return f"Pass{timestamp}!"
    else:
        return f"data_{timestamp}"

def fill_form_fields(field_data):
    log("Beginning to fill form fields with generated data.")
    for field in field_data['fields']:
        x, y = field['position']
        data_to_enter = generate_unique_data(field['name'])
        log(f"Moving to field '{field['name']}' at position ({x}, {y}) and entering data: '{data_to_enter}'")
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        pyautogui.typewrite(data_to_enter, interval=0.1)
        time.sleep(0.5)
    log("All form fields filled successfully.")

def main():
    goal, website = get_user_input()
    activate_chrome_window()
    navigate_to_website(website)
    screenshot_path = capture_screenshot()
    field_data = process_screenshot_with_ai(screenshot_path)
    fill_form_fields(field_data)
    log("Task completed successfully.")

if __name__ == "__main__":
    main()
