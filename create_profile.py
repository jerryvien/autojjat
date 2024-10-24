import os
import requests

# Function to get a new proxy from IP Royal API
def get_new_proxy(api_key):
    url = "https://api.iproyal.com/get-proxy"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        proxy_info = response.json()
        return {
            "ip": proxy_info["ip"],
            "port": proxy_info["port"],
            "username": proxy_info.get("username"),
            "password": proxy_info.get("password")
        }
    else:
        raise Exception(f"Failed to get new proxy: {response.status_code}, {response.text}")

# Function to create user profiles
def create_user_profiles(num_profiles, current_directory, api_key):
    user_profiles = []
    for i in range(1, num_profiles + 1):
        profile_name = f"BOT{i:03d}"  # Creates BOT001, BOT002, etc.
        profile_path = os.path.join(current_directory, "chrome_profiles", profile_name)
        os.makedirs(profile_path, exist_ok=True)  # Create directory if it doesn't exist
        proxy = get_new_proxy(api_key)
        
        # Save proxy info to a file for each profile
        proxy_file = os.path.join(profile_path, "proxy_info.txt")
        with open(proxy_file, "w") as f:
            f.write(f"ip={proxy['ip']}\n")
            f.write(f"port={proxy['port']}\n")
            if proxy.get("username") and proxy.get("password"):
                f.write(f"username={proxy['username']}\n")
                f.write(f"password={proxy['password']}\n")

        user_profiles.append(profile_path)
        print(f"Profile created: {profile_name} with proxy {proxy['ip']}:{proxy['port']}")

    return user_profiles

if __name__ == "__main__":
    api_key = "YOUR_IP_ROYAL_API_KEY"
    num_profiles = 3  # Define how many profiles you want to create

    # Determine the current working directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Create user profiles
    create_user_profiles(num_profiles, current_directory, api_key)