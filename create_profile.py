import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL to get the current public IP address
url = 'https://ipv4.icanhazip.com'

# IP Royal Proxy Configuration
proxy_host = 'geo.iproyal.com'
proxy_port = '12321'
proxy_username = 'iproyal4174'
proxy_password = 'dfIjovni'

# Construct the proxy URL with authentication
proxy = f'{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'

# Define the proxies dictionary for HTTP and HTTPS
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

# Function to rotate IP using IP Royal and open an undetected Chrome browser
def rotate_ip_and_browse(target_url):
    # Step 1: Show current IP without proxy
    print("Fetching current IP without proxy...")
    current_ip = get_public_ip()
    print(f"Current IP: {current_ip}\n")

    # Step 2: Show the IP after applying the proxy
    print("Fetching IP using IP Royal proxy...")
    proxy_ip = get_public_ip(proxies=proxies)
    print(f"Proxy IP: {proxy_ip}\n")

    # Step 3: Start an undetected browser with the proxy and visit the target URL
    print("Starting undetected Chrome browser with the new proxy...")

    # Configure Chrome options with the proxy
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')

    # Initialize undetected Chrome with the proxy settings
    driver = uc.Chrome(options=chrome_options)

    try:
        # Open the target URL
        driver.get(target_url)
        print(f"Successfully opened URL: {target_url}")

        # Wait for a few seconds to simulate browsing
        time.sleep(10)

    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    target_url = "https://www.popmart.com/my"

    # Rotate IP and open browser to visit the target URL
    rotate_ip_and_browse(target_url)