from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Selenium WebDriver
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service)

# Open the Google sign-in page
driver.get("https://oculus.com/casting")

# Maximize the browser window
driver.maximize_window()
time.sleep(1)


# Keep the session running until manually stopped
try:
    while True:
        user_input = input("Choose the action: \n'x' to stop the script \n's' to take a screenshot \nPut your choice: ")
        if user_input.lower() == 'x':
            break
        elif user_input.lower() == 's':
            # Take a screenshot and save it
            driver.save_screenshot('images/screenshot.png')
            print("Screenshot taken and saved as 'screenshot.png'")
finally:
    # Release resources
    driver.quit()

