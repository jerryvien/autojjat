import sys
import os
import undetected_chromedriver as uc

# IPRoyal Proxy Configuration (with whitelisting, so no authentication needed)
proxy_host = 'geo.iproyal.com'
proxy_port = '11248'  # Updated proxy port

# PopMart URLs
checkout_url = "https://www.popmart.com/my/largeShoppingCart"

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
    chrome_options.add_argument(f'--proxy-server=http://{proxy["host"]}:{proxy["port"]}')

    # Initialize undetected Chrome with the selected profile and proxy settings
    driver = uc.Chrome(options=chrome_options)

    try:
        # Directly navigate to the checkout page
        driver.get(checkout_url)
        print(f"Navigated to checkout page for profile at '{profile_path}'.")

        # The browser will remain open for user actions
        print(f"Browser for profile at '{profile_path}' will remain open. Close it manually when done.")

        # Run indefinitely until the browser is manually closed
        while True:
            pass

    except Exception as e:
        print(f"An error occurred for profile '{profile_path}': {e}")

    finally:
        # Close the browser when the script is manually stopped
        driver.quit()
        print(f"Browser for profile '{profile_path}' closed.")

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