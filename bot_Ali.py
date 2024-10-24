import sys
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,datetime
import requests

# IPRoyal Proxy Configuration (with whitelisting, so no authentication needed)
proxy_host = 'geo.iproyal.com'
proxy_port = '11248'  # Updated proxy port
proxy_country_code = '_country-my'

# Construct the full proxy address
proxy = f'{proxy_country_code}@{proxy_host}:{proxy_port}'
# URL to get the current public IP address
url = 'https://ipv4.icanhazip.com'

# Define the proxies dictionary for HTTP and HTTPS (no auth required due to whitelisting)
proxies = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}'
}

# PopMart URLs
checkout_url = "https://www.aliexpress.com/item/1005007951632351.html?spm=a2g0o.store_pc_home.slider_2009828709109.0&gatewayAdapt=4itemAdapt&aff_fcid=897de1267f3c4a3996e7a4436f57fdd1-1729784126644-07007-_DE2PBXB&tt=CPS_NORMAL&aff_fsk=_DE2PBXB&aff_platform=portals-tool&sk=_DE2PBXB&aff_trace_key=897de1267f3c4a3996e7a4436f57fdd1-1729784126644-07007-_DE2PBXB&terminal_id=8f1f0d32009e489fa29dba27b45531c4&afSmartRedirect=y"
#checkout_url = "https://www.aliexpress.com/item/1005005762305303.html?spm=a2g0o.order_list.order_list_main.5.21ef1802d4yHHT"
#buy now button ALi express
checkout_button_xpath = '//*[@id="root"]/div/div[1]/div/div[2]/div/div/div[6]/button[1]'
payment_button_xpath = '//*[@id="placeorder_wrap__inner"]/div/div[2]/div[2]/div/div/div[2]/button'


# Function to get a new proxy (simulated for this script)
def get_new_proxy():
    # Here we simulate getting a new proxy
    # For whitelisted proxies, only host and port are needed
    return {
        "host": proxy_host,
        "port": proxy_port
    }

# Function to get public IP address
def get_public_ip(proxies=None):
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"Error occurred: {e}"

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

# Function to start Chrome with the selected profile, optional proxy, and silent mode
def start_chrome_with_profile(profile_path, use_proxy=True, run_silent=True):
    # Define Chrome options with user data directory
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={profile_path}')
    
    # Disable images, CSS, and other unnecessary resources to improve speed
    chrome_prefs = {
        "profile.default_content_setting_values": {
            "images": 2,  # Disable images
            "stylesheet": 2,  # Disable stylesheets
            "cookies": 1,
            "javascript": 1,
            "plugins": 1,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "automatic_downloads": 2
        }
    }
    chrome_options.experimental_options["prefs"] = chrome_prefs
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')

    # Apply proxy settings if use_proxy is True
    if use_proxy:
        proxy = get_new_proxy()
        chrome_options.add_argument(f'--proxy-server=http://{proxy["host"]}:{proxy["port"]}')
        print(f"Proxy enabled: {proxy['host']}:{proxy['port']}")

    # Run Chrome in headless (silent) mode if run_silent is True
    if run_silent:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

    # Initialize undetected Chrome with the selected profile and proxy settings
    driver = uc.Chrome(options=chrome_options)

    #start_time = datetime.datetime.now()

    try:
        # Directly navigate to the checkout page
        driver.get(checkout_url)
        print(f"Navigated to checkout page for profile at '{profile_path}'.")

        # Try to find and click the checkout button until the URL changes
        while True:
            try:
                # Wait for the button to be present in the DOM and clickable (reduced wait time)
                #wait = WebDriverWait(driver, 0.1)  # Reduced wait time to ensure element is present
                checkout_button = driver.find_element(By.XPATH, checkout_button_xpath)
            
                #print("Checkout button is found and clickable.")

                # Click the button
                checkout_button.click()
                #print("Checkout button clicked.")
                # Start the timer
                start_time = 0

                # Monitor URL change using a polling mechanism for faster detection
                if fast_monitor_url_change(driver, checkout_url, timeout=0.1, poll_frequency=0.1):
                    print("URL changed successfully. Action was successful.")
                    # Start the timer
                    start_time = datetime.datetime.now()
                    # Wait for the button to be present in the DOM and clickable (reduced wait time)
                    #time.sleep(5)
                    #wait = WebDriverWait(driver, 0.1)  # Reduced wait time to ensure element is present
                    payment_button = driver.find_element(By.XPATH, payment_button_xpath)

                    #print("Payment button is found and clickable.")
                    # Click the button
                    payment_button.click()
                    #print("Payment button clicked.")

                    break
                else:
                    print("URL did not change. Refreshing elements and retrying...")
                     # Refresh the target elements using JavaScript
                    refresh_element(driver, checkout_button_xpath)

            except Exception as e:
                # Specific validation for "no such window" or "web view not found" errors
                if "no such window" in str(e) or "web view not found" in str(e):
                    print("Added to cart done. The window has already been closed.")
                    break
                else:
                    print(f"An error occurred while trying to click the checkout button: {e}")

    except Exception as e:
        print(f"An error occurred for profile '{profile_path}': {e}")
    finally:
        # Keep the browser open
        # After URL changes, open a new tab and close the current one
        # End the timer and calculate the elapsed time
        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        print(f"Total time taken from first click to program finish: {elapsed_time} seconds")
        
        print(f"Browser for profile at '{profile_path}' will remain open. Close it manually when done.")
        while True:
            pass

# Function to refresh specific elements on the page using JavaScript
def refresh_element(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].innerHTML = arguments[0].innerHTML;", element)
    print(f"Element at '{xpath}' refreshed.")

# Function to monitor URL change after clicking the button using polling for faster detection
def fast_monitor_url_change(driver, initial_url, timeout=5, poll_frequency=0.1):
    """
    Monitors the URL change to confirm if the action was successful.
    Returns True if the URL changes, otherwise False.
    Uses a polling mechanism to speed up URL change detection.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if driver.current_url != initial_url:
            return True
        driver.implicitly_wait(poll_frequency)  # Implicit wait instead of time.sleep for responsiveness
    return False

# Function to open a new tab and close the current one, keeping the session
def open_new_tab_and_close_current(driver, new_url):
    #driver.execute_script("window.open('');")  # Open a new blank tab
    #driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
    driver.get(new_url)  # Navigate to the new URL
    print(f"Navigated to new tab with URL: {new_url}")
    #time.sleep(5)
    # Wait for the button to be present in the DOM and clickable (reduced wait time)
    wait = WebDriverWait(driver, 3)  # Reduced wait time to ensure element is present
    checkout_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, payment_button_xpath))
        )
    print("Payment button is found and clickable.")
    # Click the button
    checkout_button.click()
    print("Payment button clicked.")
    #driver.close()  # Close the previous tab
    #driver.switch_to.window(driver.window_handles[0])  # Switch back to the remaining tab
    #print("Closed the previous tab and kept the new tab open.")

if __name__ == "__main__":
    
    # Ensure that the profile path is provided
    if len(sys.argv) < 2:
        print("Usage: python bot.py <profile_path> [use_proxy] [run_silent]")
        sys.exit(1)

    # Get the profile path from the arguments
    profile_path = sys.argv[1]

    # Optional argument to use proxy
    use_proxy = len(sys.argv) > 2 and sys.argv[2].lower() == 'true'

    # Optional argument to run Chrome in silent (headless) mode
    run_silent = len(sys.argv) > 3 and sys.argv[3].lower() == 'true'

    # Start Chrome with the profile, optional proxy, and silent mode
    start_chrome_with_profile(profile_path, use_proxy, run_silent)
