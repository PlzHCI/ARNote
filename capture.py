from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import cv2
import time
import requests
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Selenium WebDriver
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service)

# Open the Google sign-in page
driver.get("https://accounts.google.com/signin")

# Maximize the browser window
driver.maximize_window()
time.sleep(1)

# Locate the email input field and enter your email
email_input = driver.find_element(By.ID, "identifierId")
email_input.send_keys("liu03008@umn.edu")

# Click the 'Next' button
next_button = driver.find_element(By.ID, "identifierNext")
next_button.click()

# Wait for the password field to load
time.sleep(1)  # Adjust the sleep time as necessary

# Locate the Internet ID input field and enter your ID
internet_id_input = driver.find_element(By.ID, "username")  # Update with the correct ID or name
internet_id_input.send_keys("liu03008")  # Replace with your actual Internet ID

# Locate the password input field and enter your password
password_input = driver.find_element(By.ID, "password")  # Update with the correct ID or name
password_input.send_keys("UMinnesota2013Jqmnxl")  # Replace with your actual password

# Click the 'Sign In' button
sign_in_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")  # Use XPath to locate the button
sign_in_button.click()

# Wait for the login process to complete
time.sleep(5)

# Click the 'Yes, this is my device' button
yes_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Yes, this is my device')]")
yes_button.click()

# Wait for the 'Continue' button to appear
time.sleep(5)  # Adjust the sleep time as necessary

time.sleep(5)
# Open the webpage
url = "https://www.oculus.com/casting"
driver.get(url)

time.sleep(50)
# Release resources

