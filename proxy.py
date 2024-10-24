import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Proxy Configuration
proxy_host = 'geo.iproyal.com'
proxy_port = '12321'

# Configuration for Chrome profiles
profile_directory = os.path.join(os.getcwd(), "chrome_profiles")
profile_name = "BOT001"
user_profile_path = os.path.join(profile_directory, profile_name)
os.makedirs(user_profile_path, exist_ok=True)

# Chrome options setup
chrome_options = uc.ChromeOptions()
chrome_options.add_argument(f'--user-data-dir={user_profile_path}')
chrome_options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')

# Initialize undetected Chrome with the proxy settings in visible mode
driver = uc.Chrome(options=chrome_options)

try:
    # Open a test page to trigger proxy authentication
    print("Opening a webpage to trigger proxy authentication...")
    driver.get("https://www.google.com")
    time.sleep(5)  # Allow time for the proxy authentication pop-up to appear

    # Manually enter the credentials in the pop-up
    # Wait until the user enters credentials and hits OK before proceeding

    # Verify IP Address (Optional)
    driver.get("https://whatismyipaddress.com/")
    print("Opened What's My IP page to verify proxy usage.")

    # Perform other actions, like opening the target URL
    target_url = "https://www.popmart.com/my"
    driver.get(target_url)
    print(f"Successfully opened URL: {target_url}")

    # Keep the browser open to allow manual actions
    input("Press Enter to close the browser and save the profile...")

finally:
    driver.quit()
    print("Browser closed.")