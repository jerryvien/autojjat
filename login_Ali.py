import sys
import undetected_chromedriver as uc

# Function to open a Chrome profile with a given path and proxy
def open_chrome_with_profile(profile_path, proxy_host, proxy_port, proxy_username=None, proxy_password=None, headless=False):
    """
    Opens a Chrome browser with the specified user profile and proxy settings.

    Parameters:
    - profile_path (str): The path to the Chrome profile directory.
    - proxy_host (str): The host of the proxy.
    - proxy_port (str): The port of the proxy.
    - proxy_username (str, optional): The username for proxy authentication. Default is None.
    - proxy_password (str, optional): The password for proxy authentication. Default is None.
    - headless (bool, optional): Whether to run Chrome in headless mode. Default is False.
    """
    # Define Chrome options with user data directory and proxy
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={profile_path}')  # Use the specified profile directory

    # Set up proxy if provided
    if proxy_username and proxy_password:
        chrome_options.add_argument(f'--proxy-server=http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}')
    else:
        chrome_options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')  # Whitelisted proxy

    # Enable headless mode if required
    if headless:
        chrome_options.add_argument('--headless')  # Run in headless mode for silent execution
        chrome_options.add_argument('--disable-gpu')  # Disable GPU to reduce overhead
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images to reduce loading time
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize the Chrome driver with the specified options
    driver = uc.Chrome(options=chrome_options)

    try:
        # Open a specified URL for testing, e.g., PopMart's login page
        driver.get("https://www.aliexpress.com/")
        print(f"Opened Chrome with profile at '{profile_path}'. You can now interact with the browser.")

        # Keep the browser open for manual interaction
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()
        print(f"Browser for profile at '{profile_path}' closed.")

if __name__ == "__main__":
    # Ensure that the profile path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python open_profile_with_proxy.py <profile_path>")
        sys.exit(1)

    # Get the profile path from the arguments
    profile_path = sys.argv[1]

    # Configuration for proxy
    proxy_host = 'geo.iproyal.com'
    proxy_port = '11248'  # Updated proxy port
    proxy_username = None  # If no proxy authentication is needed, leave as None
    proxy_password = None  # If no proxy authentication is needed, leave as None

    # Open the Chrome profile with proxy
    open_chrome_with_profile(profile_path, proxy_host, proxy_port, proxy_username, proxy_password, headless=False)