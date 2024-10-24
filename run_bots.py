import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import multiprocessing

# Function to get Chrome options with a user profile and proxy
def get_chrome_options_with_proxy(user_data_dir=None, headless=False, proxy=None):
    chrome_options = uc.ChromeOptions()
    if user_data_dir:
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    
    # Set additional arguments to minimize detection
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images

    # Set up proxy if available
    if proxy:
        chrome_options.add_argument(f"--proxy-server=http://{proxy['ip']}:{proxy['port']}")
    
    return chrome_options

# Function to load proxy information from the profile folder
def load_proxy_info(profile_path):
    proxy_file = os.path.join(profile_path, "proxy_info.txt")
    if os.path.exists(proxy_file):
        proxy = {}
        with open(proxy_file, "r") as f:
            for line in f:
                key, value = line.strip().split('=')
                proxy[key] = value
        return proxy
    return None

# Function to run the bot for a specific user profile
def run_bot(user_data_directory, formal_url, automation_url, executable_path):
    # Load proxy information
    proxy = load_proxy_info(user_data_directory)

    # Step 1: Formal session (full browser for login)
    formal_options = get_chrome_options_with_proxy(user_data_dir=user_data_directory, proxy=proxy)
    driver = uc.Chrome(executable_path=executable_path, options=formal_options)

    # Open the formal URL for manual login
    driver.get(formal_url)
    input(f"Please log in manually for profile '{user_data_directory}' and press Enter to continue...")

    # Step 2: Refresh browser with minimal mode
    minimal_options = get_chrome_options_with_proxy(user_data_dir=user_data_directory, headless=True, proxy=proxy)
    driver.quit()
    driver = uc.Chrome(executable_path=executable_path, options=minimal_options)

    try:
        # Open the URL
        driver.get(automation_url)

        # Wait for a few seconds to ensure the page is fully loaded with countdown
        for i in range(5, 0, -1):
            print(f"[{user_data_directory}] Waiting for page to load: {i} seconds remaining...")
            time.sleep(1)

        # Keep trying to click the checkout button until successful
        while True:
            try:
                checkout_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[2]/div[3]/button'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
                checkout_button.click()
                print(f"[{user_data_directory}] Checkout button clicked successfully!")
                break
            except Exception as e:
                print(f"[{user_data_directory}] Checkout button not yet ready. Retrying in 5 seconds...")
                for i in range(5, 0, -1):
                    print(f"[{user_data_directory}] Refreshing in: {i} seconds remaining...")
                    time.sleep(1)
                driver.refresh()

        # Perform other actions as needed here
        time.sleep(5)  # Let the page load for a while before quitting

    finally:
        # Close the browser
        driver.quit()

# Main script to run multiple bots
if __name__ == "__main__":
    formal_url = "https://www.popmart.com/my"
    automation_url = "https://www.popmart.com/my/largeShoppingCart"
    executable_path = r"E:\autojjat"

    # Determine the current working directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    chrome_profiles_directory = os.path.join(current_directory, "chrome_profiles")

    # Load all available profiles
    user_profiles = [os.path.join(chrome_profiles_directory, d) for d in os.listdir(chrome_profiles_directory) if os.path.isdir(os.path.join(chrome_profiles_directory, d))]

    # Create and start multiple processes
    processes = []
    for user_data_directory in user_profiles:
        p = multiprocessing.Process(target=run_bot, args=(user_data_directory, formal_url, automation_url, executable_path))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()