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
checkout_button_xpath = '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[2]/div[3]/button'

# Function to get a new proxy (simulated for this script)
def get_new_proxy():
    # Here we simulate getting a new proxy
    # For whitelisted proxies, only host and port are needed
    return {
        "host": proxy_host,
        "port": proxy_port
    }

# Function to start Chrome with the selected profile and proxy
def start_chrome_with_profile(profile_path, proxy):
    # Define Chrome options with user data directory and proxy
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={profile_path}')
    #chrome_options.add_argument(f'--proxy-server=http://{proxy["host"]}:{proxy["port"]}')

    # Initialize undetected Chrome with the selected profile and proxy settings
    driver = uc.Chrome(options=chrome_options)

    try:
        # Directly navigate to the checkout page
        driver.get(checkout_url)
        print(f"Navigated to checkout page for profile at '{profile_path}'.")
        # Wait for a few seconds to allow the page to fully load
        #time.sleep(3)
        # Get the initial URL before clicking the button
        initial_url = driver.current_url

        # Keep clicking the checkout button until the URL changes
         # Wait for the button to be present in the DOM and clickable
        wait = WebDriverWait(driver, 5)  # Longer wait time to ensure element is present
        checkout_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, checkout_button_xpath))
                )
        print("Checkout button is found and clickable.")
        while True:
            try:
                # Scroll to the button and click
                #driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
                checkout_button.click()
                print("Checkout button clicked.")

                # Monitor URL change to verify if the action was successful
                if monitor_url_change(driver, initial_url):
                    print("URL changed successfully. Action was successful.")
                    break
                else:
                    print("URL did not change. Retrying click in 3 seconds...")
                    #time.sleep(3)

            except Exception as e:
                print(f"An error occurred while trying to click the checkout button: {e}")
                #time.sleep(3)

        # Keep the browser open
        print(f"Browser for profile at '{profile_path}' will remain open. Close it manually when done.")
        while True:
            pass

    except Exception as e:
        print(f"An error occurred for profile '{profile_path}': {e}")

    finally:
        # Close the browser when the script is manually stopped
        driver.quit()
        print(f"Browser for profile '{profile_path}' closed.")

# Function to monitor URL change after clicking the button
def monitor_url_change(driver, initial_url, timeout=0.0001):
    """
    Monitors the URL change to confirm if the action was successful.
    Returns True if the URL changes, otherwise False.
    """
    try:
        WebDriverWait(driver, timeout).until(lambda d: d.current_url != initial_url)
        return True
    except:
        return False

if __name__ == "__main__":
    # Ensure that the profile path is provided
    if len(sys.argv) != 2:
        print("Usage: python bot.py <profile_path>")
        sys.exit(1)

    # Get the profile path from the arguments
    profile_path = sys.argv[1]

    # Get a new proxy for the profile (no authentication required since proxies are whitelisted)
    proxy = get_new_proxy()

    # Start Chrome with the profile and the assigned proxy
    start_chrome_with_profile(profile_path, proxy)