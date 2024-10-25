import sys
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# PopMart URLs and XPaths
checkout_url = "https://www.popmart.com/my/largeShoppingCart"
confirmation_url = "https://www.popmart.com/my/order-confirmation?source=cart"
svg_checkbox_xpath = '//*[@id="__next"]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/svg'
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

# Function to ensure SVG checkbox is clicked and selected
def ensure_svg_checkbox_selected(driver, xpath, max_retries=10):
    retries = 0
    while retries < max_retries:
        try:
            # Click the SVG checkbox
            svg_checkbox = interact_until_success(driver, xpath, action='click')

            # Check if the checkbox is selected using JavaScript
            is_selected = driver.execute_script(
                "var elem = document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; "
                "return elem && elem.getAttribute('class').includes('selected');", 
                xpath
            )

            if is_selected:
                print("SVG checkbox is successfully selected.")
                return True
            else:
                print("SVG checkbox not selected, retrying...")
        except Exception as e:
            print(f"Error while selecting SVG checkbox: {e}")

        # Refresh the whole page if checkbox is not selected
        driver.refresh()
        print("Page refreshed to reload elements.")
        retries += 1

    print("Max retries reached. Could not select the SVG checkbox.")
    return False

# Function to wait for URL change
def wait_for_url_change(driver, initial_url, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(lambda d: d.current_url != initial_url)
        print(f"URL changed to: {driver.current_url}")
        return True
    except Exception as e:
        print(f"URL did not change. Error: {e}")
        return False

# Function to handle checkout and payment
def process_checkout(driver):
    driver.get(checkout_url)

    # Ensure the SVG checkbox is selected before proceeding
    if not ensure_svg_checkbox_selected(driver, svg_checkbox_xpath):
        print("Failed to select the SVG checkbox. Exiting...")
        return

    # Start timer for the time measurement
    start_time = time.time()

    # Click the checkout button and check for URL change
    initial_url = driver.current_url
    interact_until_success(driver, checkout_button_xpath)

    # Wait for URL change after clicking the checkout button
    if wait_for_url_change(driver, initial_url):
        driver.get(confirmation_url)

        # Click the payment button and measure time
        interact_until_success(driver, payment_button_xpath)

        # Calculate and display the elapsed time
        elapsed_time = time.time() - start_time
        print(f"Time from checkout button clicked to payment button clicked: {elapsed_time:.2f} seconds")
    else:
        print("Checkout button did not lead to a URL change.")

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
