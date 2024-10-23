import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Function to get Chrome options
def get_chrome_options():
    chrome_options = uc.ChromeOptions()
    
    # Set additional arguments to minimize detection
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images

    return chrome_options

# Configuration

# URL to navigate
url = "https://www.popmart.com/my/largeShoppingCart"

# Initialize Chrome driver
options = get_chrome_options()
driver = uc.Chrome(executable_path="C:\\Users\\Jerry\\Downloads\\chromedriver-win64\\chromedriver-win64", options=options)

try:
    # Open the URL
    driver.get(url)

    # Keep trying to click the select product button until successful
    while True:
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div'))
            )
            button.click()
            print("Select product button clicked successfully!")
            break
        except Exception as e:
            print("Retrying to click the select product button...")
            time.sleep(random.uniform(2, 4))  # Add a random delay to mimic human behavior

    # Keep trying to click the checkout button until successful
    while True:
        try:
            checkout_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[2]/div[3]/button'))
            )
            checkout_button.click()
            print("Checkout button clicked successfully!")
            break
        except Exception as e:
            print("Retrying to click the checkout button...")
            time.sleep(random.uniform(2, 4))  # Add a random delay to mimic human behavior

    # Perform other actions as needed here

    time.sleep(5)  # Let the page load for a while before quitting

finally:
    # Close the browser
    driver.quit()
