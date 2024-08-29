import pyautogui
import time
import os
import sys
import replicate
import requests
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

def upload_image_to_vps(image_path):
    url = 'https://serverIP.space/api/upload.php'  # Updated URL
    files = {'screenshot': open(image_path, 'rb')}
    token = os.getenv('SECRET_KEY')  # Get the secret key from the environment variable
    data = {'token': token}
    
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            return result.get('url')
        else:
            log(f"Failed to upload image: {result.get('message')}")
    else:
        log(f"Failed to upload image. Server responded with status code {response.status_code}")
    return None



def process_screenshot_with_ai():
    # Assume screenshot.png is in the same directory as dibot.py
    screenshot_path = os.path.join(os.path.dirname(__file__), 'screenshot.png')

    log(f"Processing screenshot '{screenshot_path}' with AI to identify required fields.")

    # Upload the screenshot to your VPS
    image_url = upload_image_to_vps(screenshot_path)
    if not image_url:
        log("Image upload failed. Exiting.")
        return None

    # Run the AI model using Replicate's API
    output = replicate.run(
        "yorickvp/llava-13b:<API_KEY>",
        input={
            "image": image_url,
            "top_p": 1,
            "prompt": "Analyze the screenshot and identify the form fields including 'username', 'email', and 'password'. For each identified field, return the field name along with its position on the screen in pixel coordinates (x, y). The output should be a structured JSON object with each field's name and position.\n",
            "max_tokens": 1024,
            "temperature": 0.2
        }
    )

    # Iterate over the output to retrieve the processed data
    processed_data = {'fields': []}
    for item in output:
        # Assuming the output is a JSON object with field names and positions
        processed_data['fields'].append(item)

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
    capture_screenshot()  # No need to return or pass the screenshot path since it's hardcoded in process_screenshot_with_ai
    field_data = process_screenshot_with_ai()  # Call the function without arguments
    if field_data:
        fill_form_fields(field_data)
    log("Task completed successfully.")

if __name__ == "__main__":
    main()
