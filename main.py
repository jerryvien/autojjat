import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to get Chrome options with proxy
def get_chrome_options(user_data_dir=None):
    chrome_options = uc.ChromeOptions()
    if user_data_dir:
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    
    # Set additional arguments to minimize detection
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
    
    return chrome_options

# Configuration

# URL to navigate
formal_url = "https://www.popmart.com/my"
automation_url = "https://www.popmart.com/my/largeShoppingCart"

# Initialize Chrome driver
# Step 1: Formal session (full browser for login)
user_data_directory = r"E:\autojjat\chrome_profile"
formal_options = uc.ChromeOptions()
formal_options.add_argument(f"--user-data-dir={user_data_directory}")
driver = uc.Chrome(executable_path=r"E:\autojjat", options=formal_options)

# Open the formal URL for manual login
driver.get(formal_url)
input("Please log in manually on the formal URL and press Enter to continue...")

# Step 2: Refresh browser with minimal mode
minimal_options = get_chrome_options(user_data_directory)
# Set additional arguments to minimize detection after formal session
minimal_options.add_argument("--disable-gpu")
minimal_options.add_argument("--disable-extensions")
minimal_options.add_argument("--no-sandbox")
minimal_options.add_argument("--disable-setuid-sandbox")
minimal_options.add_argument("--disable-blink-features=AutomationControlled")
minimal_options.add_argument("--blink-settings=imagesEnabled=false")
#minimal_options.add_argument("--headless")  # Run in headless mode

# Close formal session and start new minimal session
driver.quit()
driver = uc.Chrome(executable_path=r"E:\autojjat", options=minimal_options)



try:
    # Open the URL
    driver.get(automation_url)

    # Wait for the page to load completely with countdown
    for i in range(5, 0, -1):
        print(f"Waiting for page to fully load: {i} seconds remaining...")
        time.sleep(1)

    # Keep trying to click the first checkbox until successful
    try:
        while True:
            try:
                checkbox = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]'))
                )
                if checkbox.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                    checkbox.click()
                    print("Checkbox clicked successfully!")
                    break
            except Exception as e:
                print("Stock not yet ready. Retrying in 5 seconds...")
                for i in range(5, 0, -1):
                    print(f"Refreshing in: {i} seconds remaining...")
                    time.sleep(1)
                driver.refresh()

        # Wait for the checkout button to be clickable
        checkout_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[2]/div[3]/button'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
        driver.execute_script("arguments[0].click();", checkout_button)
        print("Button clicked successfully!")
    except Exception as e:
        print("Error: The button did not become clickable within the time limit.")
        print(e)

    # Perform other actions as needed here

    time.sleep(5)  # Let the page load for a while before quitting

finally:
    # Close the browser
    driver.quit()
