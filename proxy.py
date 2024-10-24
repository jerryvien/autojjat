import os
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL to get the current public IP address
url = 'https://ipv4.icanhazip.com'

# IPRoyal Proxy Configuration
proxy_host = 'geo.iproyal.com'
proxy_port = '12321'
proxy_username = 'iproyal4174'
proxy_password = 'dfIjovni_country-my'
proxy_country_code = '_country-my'

# Construct the full proxy address
proxy = f'{proxy_country_code}@{proxy_host}:{proxy_port}'
proxy_auth = f'{proxy_username}:{proxy_password}'

# Define the proxies dictionary for HTTP and HTTPS
proxies = {
    'http': f'http://{proxy_auth}@{proxy}',
    'https': f'http://{proxy_auth}@{proxy}'
}

# Step 1: Verify Proxy Using requests
def verify_proxy():
    try:
        # Make a request using the proxy to verify the IP address
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Raise an error for bad responses
        print(f"Public IP Address through Proxy: {response.text.strip()}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return False
    return True

# Step 2: Automate the Chrome Browser with Proxy Authentication
def automate_with_proxy(profile_directory, profile_name, target_url):
    user_profile_path = os.path.join(profile_directory, profile_name)
    os.makedirs(user_profile_path, exist_ok=True)

    # Chrome options setup
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_profile_path}')
    chrome_options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')

    # Initialize undetected Chrome with the proxy settings
    driver = uc.Chrome(options=chrome_options)

    try:
        # Open a test page to trigger proxy authentication
        driver.get("https://www.google.com")
        try:
            # Wait for the authentication alert to appear
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            # Automate authentication by entering the credentials
            alert.send_keys(f"{proxy_username}\t{proxy_password}")
            alert.accept()
            print("Proxy authentication completed.")
        except Exception as e:
            print("No authentication alert detected or failed to authenticate:", e)

        # Verify IP Address in browser (Optional)
        driver.get("https://whatismyipaddress.com/")
        print("Opened What's My IP page to verify proxy usage.")

        # Open the target URL
        driver.get(target_url)
        print(f"Successfully opened URL: {target_url}")

        # Keep the browser open for manual actions
        input("Press Enter to close the browser and save the profile...")

    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

# Main Function
if __name__ == "__main__":
    # Step 1: Verify Proxy
    if verify_proxy():
        print("Proxy verified successfully.")

        # Step 2: Automate with Proxy
        target_url = "https://www.popmart.com/my"
        profile_directory = os.path.join(os.getcwd(), "chrome_profiles")
        profile_name = "BOT001"

        # Automate the browser session
        automate_with_proxy(profile_directory, profile_name, target_url)
    else:
        print("Proxy verification failed. Please check your proxy configuration.")