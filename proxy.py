import requests

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

if __name__ == "__main__":
    # Step 1: Get the current IP address without a proxy
    print("Fetching public IP without proxy...")
    current_ip = get_public_ip()
    print(f"Current IP: {current_ip}\n")

    # Step 2: Get the IP address using the IP Royal proxy
    print("Fetching public IP using IP Royal proxy...")
    proxy_ip = get_public_ip(proxies=proxies)
    print(f"Proxy IP: {proxy_ip}")