import os
import undetected_chromedriver as uc

# IPRoyal Proxy Configuration (with whitelisting, so no authentication needed)
proxy_host = 'geo.iproyal.com'
proxy_port = '11248'  # Updated proxy port

# PopMart URLs
checkout_url = "https://www.popmart.com/my/largeShoppingCart"

# Function to list available profiles
def list_profiles(profile_directory):
    return [d for d in os.listdir(profile_directory) if os.path.isdir(os.path.join(profile_directory, d))]

# Function to get a new proxy (simulated for this script)
def get_new_proxy():
    # Here we simulate getting a new proxy
    # For whitelisted proxies, only host and port are needed
    return {
        "host": proxy_host,
        "port": proxy_port
    }

# Function to start Chrome with the selected profile and proxy
def start_chrome_with_profile(profile_directory, profile_name, proxy):
    user_profile_path = os.path.join(profile_directory, profile_name)

    # Define Chrome options with user data directory and proxy
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_profile_path}')
    chrome_options.add_argument(f'--proxy-server=http://{proxy["host"]}:{proxy["port"]}')

    # Initialize undetected Chrome with the selected profile and proxy settings
    driver = uc.Chrome(options=chrome_options)

    try:
        # Directly navigate to the checkout page
        driver.get(checkout_url)
        print(f"Navigated to checkout page for profile '{profile_name}'.")
    except Exception as e:
        print(f"An error occurred for profile '{profile_name}': {e}")

if __name__ == "__main__":
    # Define the profile directory path
    profile_directory = os.path.join(os.getcwd(), "chrome_profiles")  # Directory containing Chrome profiles

    # List available profiles in the profile directory
    profiles = list_profiles(profile_directory)

    # Start Chrome for each profile with a different proxy
    if profiles:
        for profile_name in profiles:
            # Get a new proxy for each profile (no authentication required since proxies are whitelisted)
            proxy = get_new_proxy()

            # Start Chrome with the profile and the assigned proxy
            start_chrome_with_profile(profile_directory, profile_name, proxy)
    else:
        print("No profiles found in the profile library.")