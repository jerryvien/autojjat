import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# PopMart URLs and XPaths
checkout_url = "https://www.popmart.com/my/largeShoppingCart"
confirmation_url = "https://www.popmart.com/my/order-confirmation?source=cart"
checkout_button_xpath = '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[2]/div[3]/button'
payment_button_xpath = '//*[@id="__next"]/div/div/div[2]/div[1]/div[1]/div/button'

# Proxy Configuration
proxy_host = 'geo.iproyal.com'
proxy_port = '11248'
proxy_country_code = '_country-my'
proxy = f'{proxy_country_code}@{proxy_host}:{proxy_port}'

# Function to initialize Chrome with options
def start_chrome(profile_path, use_proxy=False, headless=False):
    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={profile_path}')
    if use_proxy:
        options.add_argument(f'--proxy-server=http://{proxy}')
        print(f"Proxy enabled: {proxy}")
    if headless:
        options.add_argument('--headless')
    return uc.Chrome(options=options)

# Function to refresh page and wait for element to be clickable
def wait_for_clickable(driver, xpath, refresh=True, timeout=2):
    while True:
        try:
            if refresh:
                # Refresh the page
                driver.refresh()
                print("Page refreshed.")
            
            # Wait for the element to be clickable
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            print(f"Clicked element at {xpath}")
            return True

        except Exception as e:
            print(f"Element not clickable yet, retrying... Error: {e}")

# Function to wait for payment button to be ready and clickable
def wait_for_payment_button(driver, xpath, timeout=10):
    while True:
        try:
            # Wait for the payment button to be clickable without refreshing
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            print("Payment button clicked!")
            return True

        except Exception as e:
            print(f"Payment button not ready, waiting... Error: {e}")

# Function to handle checkout and payment
def process_checkout(driver):
    # Navigate to checkout page
    driver.get(checkout_url)

    # Keep refreshing until checkout button is clickable
    print("Waiting for checkout button...")
    wait_for_clickable(driver, checkout_button_xpath)

    # After successful checkout, navigate to payment page
    driver.get(confirmation_url)

    # Wait for the payment button to be ready
    print("Waiting for payment button...")
    wait_for_payment_button(driver, payment_button_xpath)

    # Wait for further instruction
    print("Payment process completed. Waiting for further instructions.")
    input("Press Enter to close the browser when done...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bot.py <profile_path> [use_proxy] [headless]")
        sys.exit(1)

    profile_path = sys.argv[1]
    use_proxy = len(sys.argv) > 2 and sys.argv[2].lower() == 'true'
    headless = len(sys.argv) > 3 and sys.argv[3].lower() == 'true'

    driver = start_chrome(profile_path, use_proxy, headless)
    try:
        process_checkout(driver)
    finally:
        driver.quit()
