import sys
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# IPRoyal Proxy Configuration (with whitelisting, so no authentication needed)
proxy_host = 'geo.iproyal.com'
proxy_port = '11248'  # Updated proxy port

# PopMart URLs
checkout_url = "https://www.popmart.com/my/largeShoppingCart"
checkbox_xpath = '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]'
checkout_button_xpath = '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[2]/div[3]/button'

# Function to get a new proxy (simulated for this script)
def get_new_proxy():
    # Here we simulate getting a new proxy
    # For whitelisted proxies, only host and port are needed
    return {
        "host": proxy_host,
        "port": proxy_port
    }

# Function to start Chrome with the selected profile, optional proxy, and silent mode
def start_chrome_with_profile(profile_path, use_proxy=False, run_silent=True):
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

    try:
        # Directly navigate to the checkout page
        driver.get(checkout_url)
        print(f"Navigated to checkout page for profile at '{profile_path}'.")

        # Try to find and click the checkout button until the URL changes
        while True:
            try:
                # Refresh the target elements using JavaScript
                refresh_element(driver, checkbox_xpath)
                refresh_element(driver, checkout_button_xpath)

                # Ensure the checkbox element is properly checked before proceeding
                checkbox = driver.find_element(By.XPATH, checkbox_xpath)
                while not checkbox.is_selected():
                    checkbox.click()
                    print("Attempting to check the checkbox...")
                    WebDriverWait(driver, 2).until(lambda d: checkbox.is_selected())
                print("Checkbox is now properly checked.")

                # Wait for the button to be present in the DOM and clickable (reduced wait time)
                wait = WebDriverWait(driver, 1)  # Reduced wait time to ensure element is present
                checkout_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, checkout_button_xpath))
                )
                print("Checkout button is found and clickable.")

                # Click the button
                checkout_button.click()
                print("Checkout button clicked.")

                # Monitor URL change using a polling mechanism for faster detection
                if fast_monitor_url_change(driver, checkout_url, timeout=0.1, poll_frequency=0.1):
                    print("URL changed successfully. Action was successful.")
                    break
                else:
                    print("URL did not change. Refreshing elements and retrying...")

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
