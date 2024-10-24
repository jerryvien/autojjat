import os
import requests
import zipfile
import undetected_chromedriver as uc
import time
import shutil

# URL to get the current public IP address
url = 'https://ipv4.icanhazip.com'

# IP Royal Proxy Configuration
proxy_host = 'geo.iproyal.com'
proxy_port = '12321'
proxy_username = 'iproyal4174'
proxy_password = 'dfIjovni'

# Construct the proxy URL with authentication
proxy = f'{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'

# Define the proxies dictionary for HTTP and HTTPS
proxies = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}'
}

# Function to get public IP address
def get_public_ip(proxies=None):
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"Error occurred: {e}"

# Function to create proxy authentication extension for Chrome
def create_proxy_extension(proxy_host, proxy_port, proxy_username, proxy_password):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxy Auto Auth Extension",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = f"""
    var config = {{
            mode: "fixed_servers",
            rules: {{
              singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
              }},
              bypassList: ["localhost"]
            }}
    }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_username}",
                    password: "{proxy_password}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );
    """

    # Create a temporary directory to store the extension files
    plugin_dir = os.path.join(os.getcwd(), "proxy_auth_plugin")
    os.makedirs(plugin_dir, exist_ok=True)

    # Write the manifest and background script
    with open(os.path.join(plugin_dir, "manifest.json"), "w") as f:
        f.write(manifest_json)

    with open(os.path.join(plugin_dir, "background.js"), "w") as f:
        f.write(background_js)

    # Create a zip file of the extension to load into Chrome
    plugin_path = os.path.join(os.getcwd(), "proxy_auth_plugin.zip")
    with zipfile.ZipFile(plugin_path, 'w') as zipf:
        zipf.write(os.path.join(plugin_dir, "manifest.json"), "manifest.json")
        zipf.write(os.path.join(plugin_dir, "background.js"), "background.js")

    return plugin_path

# Function to create and save user profile
def rotate_ip_and_browse(target_url, profile_directory, profile_name):
    # Step 1: Show current IP without proxy
    print("Fetching current IP without proxy...")
    current_ip = get_public_ip()
    print(f"Current IP: {current_ip}\n")

    # Step 2: Show the IP after applying the proxy
    print("Fetching IP using IP Royal proxy...")
    proxy_ip = get_public_ip(proxies=proxies)
    print(f"Proxy IP: {proxy_ip}\n")

    # Step 3: Create the proxy authentication extension
    proxy_extension_path = create_proxy_extension(proxy_host, proxy_port, proxy_username, proxy_password)

    # Step 4: Start an undetected browser with the proxy and visit the target URL
    print(f"Starting undetected Chrome browser for profile '{profile_name}' with the new proxy...")

    # Configure Chrome options with the proxy and user data directory
    user_profile_path = os.path.join(profile_directory, profile_name)
    os.makedirs(user_profile_path, exist_ok=True)

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_profile_path}')
    chrome_options.add_extension(proxy_extension_path)

    # Initialize undetected Chrome with the proxy settings
    driver = uc.Chrome(options=chrome_options)

    try:
        # Open the target URL
        driver.get(target_url)
        print(f"Successfully opened URL: {target_url}")

        # Browser remains open for you to create accounts or perform other actions manually
        input("Press Enter to close the browser and save the profile...")

    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

    # Step 5: Clean up unnecessary files to reduce profile storage size
    cleanup_chrome_profile(user_profile_path)

# Function to clean up unnecessary files from Chrome profile directory
def cleanup_chrome_profile(profile_path):
    # Removing unnecessary files to minimize storage
    cache_path = os.path.join(profile_path, "Default", "Cache")
    code_cache_path = os.path.join(profile_path, "Default", "Code Cache")
    gpu_cache_path = os.path.join(profile_path, "Default", "GPUCache")
    
    for path in [cache_path, code_cache_path, gpu_cache_path]:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            print(f"Removed cache directory: {path}")

if __name__ == "__main__":
    target_url = "https://www.popmart.com/my"
    profile_directory = os.path.join(os.getcwd(), "chrome_profiles")  # Directory to store Chrome profiles

    # Create and manage multiple profiles
    os.makedirs(profile_directory, exist_ok=True)

    # Determine the next profile name based on existing profiles
    existing_profiles = [d for d in os.listdir(profile_directory) if os.path.isdir(os.path.join(profile_directory, d))]
    next_index = len(existing_profiles) + 1
    profile_name = f"BOT{next_index:03d}"  # Creates BOT001, BOT002, etc.

    # Rotate IP and open browser to visit the target URL with the newly created profile
    rotate_ip_and_browse(target_url, profile_directory, profile_name)