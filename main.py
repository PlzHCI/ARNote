# Author: Xianhao
import os
import socketio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Initialize Selenium WebDriver

from prompt import process_input  # Import the process_input function
# Import the process_single_image function
from OCR import inference_single_image

service = Service('./chromedriver')
driver = webdriver.Chrome(service=service)

# Open the Google sign-in page
driver.get("https://oculus.com/casting")

# Maximize the browser window
driver.maximize_window()
time.sleep(1)

# Initialize Socket.IO client
sio = socketio.Client()

# Connect to the server on port 3000
sio.connect('http://127.0.0.1:3000/')

# Define a handler for a specific event, e.g., 'screenshot'
@sio.on('screenshot')
def on_screenshot(data):
    print("Received 'screenshot' event with data:", data)
    # Generate a unique filename based on the current time
    timestamp = int(time.time())
    screenshot_filename = f'images/screenshot_{timestamp}.png'
    # Take a screenshot and save it
    driver.save_screenshot(screenshot_filename)
    print(f"Screenshot taken and saved as '{screenshot_filename}'")
    # execute OCR detection and append to single_result.txt
    inference_result = inference_single_image(screenshot_filename, os.environ.get('GOOGLE_CLOUD_API_KEY'))
    print(f"OCR result: {inference_result}")
    
    
    
@sio.on('ideation')
def on_ideation(data):
    # Read the contents of single_result.txt
    print("Received 'require ideation' event with data:", data)
    with open('single_result.txt', 'r') as file:
        response = file.read()  # Save the data into response variable
    
    # Call the process_input function with the response
    result = process_input(response)  # Process the input
    print(f"Ideation result below:\n{result}")
    sio.emit('result', result)

# Keep the session running until manually stopped
try:
    while True:
        user_input = input("Choose the action: \n'x' to stop the script \n's' to take a screenshot \n'e' to broadcast 'screenshot' event \nPut your choice: ")
        if user_input.lower() == 'x':
            break
        elif user_input.lower() == 's':
            # Take a screenshot and save it
            driver.save_screenshot('images/screenshot.png')
            print("Screenshot taken and saved as 'screenshot.png'")
        else:
            print("Invalid input. Please try again.")
finally:
    # Release resources
    driver.quit()
    sio.disconnect()

