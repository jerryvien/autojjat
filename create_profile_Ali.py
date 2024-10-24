import os
import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import shutil

# URL to get the current public IP address
url = 'https://ipv4.icanhazip.com'

# IPRoyal Proxy Configuration (with whitelisting or automatic credentials)
proxy_host = 'geo.iproyal.com'
proxy_port = '11248'  # Updated proxy port
proxy_country_code = '_country-my'

# Construct the full proxy address
proxy = f'{proxy_country_code}@{proxy_host}:{proxy_port}'

# Define the proxies dictionary for HTTP and HTTPS (using credentials if not whitelisted)
proxies = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}'
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
    print("Fetching IP using IPRoyal proxy...")
    proxy_ip = get_public_ip(proxies=proxies)
    print(f"Proxy IP: {proxy_ip}\n")

    # Step 3: Start an undetected browser with proxy settings
    print(f"Starting undetected Chrome browser for profile '{profile_name}' with the new proxy...")

    # Configure Chrome options with user data directory
    user_profile_path = os.path.join(profile_directory, profile_name)
    os.makedirs(user_profile_path, exist_ok=True)

    # Define Chrome options with minimal traffic settings
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_profile_path}')
    #chrome_options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')
    
    # Arguments to reduce browser traffic
    #chrome_options.add_argument("--disable-extensions")  # Disable extensions
    #chrome_options.add_argument("--disable-gpu")  # Disable GPU
    #chrome_options.add_argument("--disable-images")  # Disable images (handled in blink settings below)
    #chrome_options.add_argument("--disable-animations")  # Disable animations
    #chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable loading images
    #chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flag detection
    #chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
    #chrome_options.add_argument("--disable-setuid-sandbox")  # Disable setuid sandbox

    # Initialize undetected Chrome with the proxy settings
    driver = uc.Chrome(options=chrome_options)

    try:
        # Step 4: Open the target URL (PopMart Login Page)
        driver.get(target_url)
        print(f"Successfully opened URL: {target_url}")

        # Wait for input in terminal to proceed
        input("Press Enter to perform further actions...")

        # Perform further actions after confirmation

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
    target_url = "https://www.aliexpress.com/"  # Updated URL for PopMart login
    profile_directory = os.path.join(os.getcwd(), "chrome_profiles")  # Directory to store Chrome profiles

    # Create and manage multiple profiles
    os.makedirs(profile_directory, exist_ok=True)

    # Determine the next profile name based on existing profiles
    existing_profiles = [d for d in os.listdir(profile_directory) if os.path.isdir(os.path.join(profile_directory, d))]
    next_index = len(existing_profiles) + 1
    profile_name = f"ALIBOT{next_index:03d}"  # Creates BOT001, BOT002, etc.

    # Rotate IP and open browser to visit the target URL with the newly created profile
    rotate_ip_and_browse(target_url, profile_directory, profile_name)