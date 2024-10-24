import os
import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil

# URL to get the current public IP address
url = 'https://ipv4.icanhazip.com'

# IP Royal Proxy Configuration
proxy_host = 'geo.iproyal.com'
proxy_port = '12321'
proxy_username = 'iproyal4174'
proxy_password = 'dfIjovni'

# Define the proxies dictionary for HTTP and HTTPS
proxies = {
    'http': f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
    'https': f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'
}

# Function to get public IP address
def get_public_ip(proxies=None):
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"Error occurred: {e}"

# Function to authenticate proxy and open Chrome browser after successful verification
def rotate_ip_and_browse(target_url, profile_directory, profile_name):
    # Step 1: Show current IP without proxy
    print("Fetching current IP without proxy...")
    current_ip = get_public_ip()
    print(f"Current IP: {current_ip}\n")

    # Step 2: Show the IP after applying the proxy
    print("Fetching IP using IP Royal proxy...")
    proxy_ip = get_public_ip(proxies=proxies)
    print(f"Proxy IP: {proxy_ip}\n")

    # Step 3: Start an undetected browser with FoxyProxy extension
    print(f"Starting undetected Chrome browser for profile '{profile_name}' with the new proxy...")

    # Configure Chrome options with user data directory
    user_profile_path = os.path.join(profile_directory, profile_name)
    os.makedirs(user_profile_path, exist_ok=True)

    # Define Chrome options
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_profile_path}')
    chrome_options.add_argument('--load-extension=IPRoyal.crx')  # Load the FoxyProxy extension

    # Initialize undetected Chrome with the proxy settings
    driver = uc.Chrome(options=chrome_options)

    try:
        # Open FoxyProxy extension page to configure proxy settings
        driver.get("chrome-extension://<FOXYPROXY_EXTENSION_ID>/popup.html")

        # Wait for the FoxyProxy setup page to load and configure the proxy
        time.sleep(5)  # Wait for the FoxyProxy extension to load completely
        driver.find_element(By.ID, 'proxyHost').send_keys(proxy_host)
        driver.find_element(By.ID, 'proxyPort').send_keys(proxy_port)
        driver.find_element(By.ID, 'proxyUsername').send_keys(proxy_username)
        driver.find_element(By.ID, 'proxyPassword').send_keys(proxy_password)
        driver.find_element(By.ID, 'saveProxy').click()
        time.sleep(2)  # Wait for the settings to be applied

        # Verify IP Address with the configured FoxyProxy
        driver.get(url)
        time.sleep(2)
        public_ip = driver.find_element(By.TAG_NAME, "body").text.strip()
        print(f"IP address after proxy in browser: {public_ip}\n")

        # Step 4: Open the target URL (PopMart) and What's My IP page
        driver.get(target_url)
        print(f"Successfully opened URL: {target_url}")

        # Open What's My IP page to verify the proxy is being used
        driver.execute_script("window.open('https://whatismyipaddress.com/', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        print("Opened What's My IP page.")

        # Wait for a few seconds to simulate browsing
        input("Press Enter to close the browser and save the profile...")

    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

    # Step 5: Clean up unnecessary files to reduce profile storage size
    cleanup_chrome_profile(user_profile_path)

# Function to clean up unnecessary files from Chrome profile directory
def cleanup_chrome_profile(profile_path):
    # Removing unnecessary files to minimize storage
    cache_path = os.path.join(profile_path, "Default", "Cache")
    code_cache_path = os.path.join(profile_path, "Default", "Code Cache")
    gpu_cache_path = os.path.join(profile_path, "Default", "GPUCache")
    
    for path in [cache_path, code_cache_path, gpu_cache_path]:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            print(f"Removed cache directory: {path}")

if __name__ == "__main__":
    target_url = "https://www.popmart.com/my"
    profile_directory = os.path.join(os.getcwd(), "chrome_profiles")  # Directory to store Chrome profiles

    # Create and manage multiple profiles
    os.makedirs(profile_directory, exist_ok=True)

    # Determine the next profile name based on existing profiles
    existing_profiles = [d for d in os.listdir(profile_directory) if os.path.isdir(os.path.join(profile_directory, d))]
    next_index = len(existing_profiles) + 1
    profile_name = f"BOT{next_index:03d}"  # Creates BOT001, BOT002, etc.

    # Rotate IP and open browser to visit the target URL with the newly created profile
    rotate_ip_and_browse(target_url, profile_directory, profile_name)