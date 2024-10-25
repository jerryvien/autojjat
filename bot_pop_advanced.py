import sys
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# PopMart URLs and XPaths
checkout_url = "https://www.popmart.com/my/largeShoppingCart"
confirmation_url = "https://www.popmart.com/my/order-confirmation?source=cart"
checkbox_xpath = '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]'
checkout_button_xpath = '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[2]/div[3]/button'
payment_button_xpath = '//*[@id="__next"]/div/div/div[2]/div[1]/div[1]/div/button'

# Function to initialize Chrome with options
def start_chrome(profile_path, use_proxy=False, headless=False):
    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={profile_path}')
    if use_proxy:
        options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')
    if headless:
        options.add_argument('--headless')
    return uc.Chrome(options=options)

# Function to interact with elements until successful
def interact_until_success(driver, xpath, action='click', delay=0.2):
    while True:
        try:
            # Locate the element and ensure it is clickable
            elem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Perform the action (click)
            if action == 'click':
                elem.click()
                print(f"Successfully clicked element at {xpath}")
            
            # Return the element for further checks if needed
            return elem

        except Exception as e:
            print(f"Retrying: Element not ready. Error: {e}")
            
            # Refresh the element using JavaScript, but only if it exists
            is_present = driver.execute_script(
                f"return document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue != null;"
            )
            if is_present:
                driver.execute_script(
                    f"var elem = document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; "
                    "if (elem) { elem.innerHTML += ''; }"
                )
            else:
                print(f"Element not found for XPath: {xpath}")

# Function to ensure checkbox is selected before proceeding
def ensure_checkbox_selected(driver, xpath):
    while True:
        # Click the checkbox
        checkbox = interact_until_success(driver, xpath, action='click')
        
        # Check if the checkbox is selected
        if checkbox.is_selected():
            print("Checkbox is successfully selected.")
            return True  # Proceed if checkbox is selected
        else:
            print("Checkbox not selected, retrying...")

# Function to handle checkout and payment
def process_checkout(driver):
    driver.get(checkout_url)

    # Ensure the checkbox is selected before proceeding
    ensure_checkbox_selected(driver, checkbox_xpath)

    # Start timer for the time measurement
    start_time = time.time()

    # Click the checkout button and proceed
    interact_until_success(driver, checkout_button_xpath)
    driver.get(confirmation_url)

    # Click the payment button and measure time
    interact_until_success(driver, payment_button_xpath)

    # Calculate and display the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Time from checkout button clicked to payment button clicked: {elapsed_time:.2f} seconds")

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
        print("Payment button clicked. Browser will stay open for further actions.")
        input("Press Enter to close the browser when done...")
    finally:
        driver.quit()
