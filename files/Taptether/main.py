import os
import requests
import time
import json
from colorama import init, Fore, Style
import random
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import keyboard  # Add this import

init(autoreset=True)

# Function to get random color
def get_random_color():
    colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return random.choice(colors)

# Read and parse the query.txt file
with open('query.txt', 'r') as file:
    lines = file.readlines()

# Extract authorization data from each line
authorizations = [line.strip() for line in lines]

def format_balance(balance):
    value = float(balance) / 1000000
    return "{:.8f}".format(value)

def fetch_user_data(auth, index):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7',
        'access-control-allow-origin': '*',
        'authorization': auth,
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://tap-tether.org/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AG Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.134 Mobile Safari/537.36',
        'x-requested-with': 'org.telegram.messenger.web'
    }
    
    response = requests.get('https://tap-tether.org/server/login', headers=headers)
    
    if response.status_code == 200:
        data = response.json()['userData']
        first_name = data['firstName']
        balance = format_balance(data['balance'])
        balance_gold = format_balance(data['balanceGold'])
        remaining_clicks = data['remainingClicks']
        
        result = (
            f"{get_random_color()}{first_name}{Style.RESET_ALL} | "
            f"USDT: {Fore.GREEN}{balance}{Style.RESET_ALL} | "
            f"Balance: {Fore.YELLOW}{balance_gold}{Style.RESET_ALL} | "
            f"Remaining Clicks: {get_random_color()}{remaining_clicks}{Style.RESET_ALL}"
        )
        
        return result, data['lastUpdateClicksTime']
    return None, None

def perform_clicks(auth, last_click_time):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7',
        'access-control-allow-origin': '*',
        'authorization': auth,
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://tap-tether.org/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AG Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.134 Mobile Safari/537.36',
        'x-requested-with': 'org.telegram.messenger.web'
    }
    
    url = f'https://tap-tether.org/server/clicks?clicks=1000&lastClickTime={last_click_time}'
    response = requests.get(url, headers=headers)
    
    return response.status_code == 200

def fetch_and_print_user_data(auth, index):
    while True:
        try:
            time.sleep(10)
            result, last_click_time = fetch_user_data(auth, index)
            
            if result:
                perform_clicks(auth, last_click_time)
                return result
            else:
                return Fore.RED + f"Failed to fetch data for Akun {index + 1}"
        
        except Exception as e:
            return Fore.RED + f"Error fetching data for Akun {index + 1}: {e}"

while True:
    if keyboard.is_pressed('q'):  # Check if 'q' is pressed
        print("Exiting...")
        break
    
    results = []
    
    # Use ThreadPoolExecutor to make requests concurrently
    with ThreadPoolExecutor(max_workers=len(authorizations)) as executor:
        futures = [executor.submit(fetch_and_print_user_data, auth, index) for index, auth in enumerate(authorizations)]
        for future in futures:
            result = future.result()  # Wait for all threads to complete
            if result:
                results.append(result)
    
    if results:
        # Clear the previous output
        print("\033c", end="")  # ANSI escape code to clear the screen
        # Print all results at once
        print("\n".join(results), end="\r", flush=True)
    
    # time.sleep(1)  # Adjust sleep time as needed