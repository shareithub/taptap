import requests
import json
import time
from colorama import Fore, Style, init
# Function to get token from query
def get_token(query):
    url = f"https://api.djdog.io/telegram/login?{query}"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://djdog.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data['data']
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                print(Fore.RED + Style.BRIGHT + f"Gagal Login. Failed to resolve host: {e}           ", end="\r" , flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"Gagal Login {e}           ", end="\r" , flush=True)
            time.sleep(2)  # Wait for 5 seconds before retrying

# Function to get task list
def get_task_list(token):
    url = 'https://api.djdog.io/task/list'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'cache-control': 'no-cache',
        'origin': 'https://djdog.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching task list: {e}")
            time.sleep(2)  # Wait for 5 seconds before retrying

# Function to finish task
def finish_task(task_id, token):
    url = f'https://api.djdog.io/task/finish?taskIds={task_id}'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'cache-control': 'no-cache',
        'content-length': '0',
        'origin': 'https://djdog.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    while True:
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(Fore.RED + Style.BRIGHT + f"[ Task ]: Gagal Finishing task {e}           ", end="\r" , flush=True)
            time.sleep(2)  # Wait for 5 seconds before retrying

# Function to level up max
def level_up_max(token, max):
    url = 'https://api.djdog.io/pet/levelUp/'+max
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'cache-control': 'no-cache',
        'content-length': '0',
        'origin': 'https://djdog.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    while True:
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(Fore.RED + Style.BRIGHT + f"[ Pet ]: Gagal Level up {e}           ", end="\r" , flush=True)
            time.sleep(2)  # Wait for 5 seconds before retrying

def tap_tap(token,total):
    url = 'https://api.djdog.io/pet/collect?clicks='+total
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'cache-control': 'no-cache',
        'content-length': '0',
        'origin': 'https://djdog.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    while True:
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(Fore.RED + Style.BRIGHT + f"[ Tap ]: Gagal Tap {e}           ", end="\r" , flush=True)
            time.sleep(2)  # Wait for 5 seconds before retrying

# Function to get info
def get_info(token):
    url = 'https://api.djdog.io/pet/barAmount'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'cache-control': 'no-cache',
        'origin': 'https://djdog.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(Fore.RED + Style.BRIGHT + f"[ Info ]: Gagal Mendapatkan info {e}           ", end="\r" , flush=True)
            time.sleep(2)  # Wait for 5 seconds before retrying

def get_box(token):
    url = 'https://api.djdog.io/pet/boxMall'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'cache-control': 'no-cache',
        'origin': 'https://djdog.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(Fore.RED + Style.BRIGHT + f"[ Info ]: Gagal Mendapatkan box {e}           ", end="\r" , flush=True)
            time.sleep(2)  # Wait for 5 seconds before retrying


# Main function to process each account
def process_account(query):
    print(Fore.YELLOW + Style.BRIGHT + f"Try to login..", end="\r" , flush=True)
    data = get_token(query)
    if data is None:
        return
    telegram_id = data['telegramId']
    telegram_username = data.get('telegramUsername', 'Tidak ada Username')
    access_token = data['accessToken']

    print(Fore.CYAN + Style.BRIGHT + f"===== [ {telegram_username} ]======"  , flush=True)
    print(Fore.CYAN + Style.BRIGHT + f"[ ID Tele ]: {telegram_id}"  , flush=True)
   
    print(Fore.YELLOW + Style.BRIGHT + f"Getting info..", end="\r" , flush=True)
    time.sleep(2)
    info = get_info(access_token)
    if info is None:
        return
    level_pet = info['data']['level']

    print(Fore.YELLOW + Style.BRIGHT + f"[ Balance ]: {info['data']['goldAmount']}  $HIT         "  , flush=True)
    print(Fore.BLUE + Style.BRIGHT + f"[ Level ]: {level_pet}" , flush=True)
    print(Fore.YELLOW + Style.BRIGHT + f"[ Bar Amount ]: {info['data']['availableAmount']} - {info['data']['barGoldLimit']}" , flush=True)
    total_tap = str(info['data']['availableAmount'])
    print(Fore.YELLOW + Style.BRIGHT + f"Tapping..", end="\r" , flush=True)
    tapping = tap_tap(access_token,total_tap)
    if tapping is None:
        return
    print(Fore.GREEN + Style.BRIGHT + f"[ Tap ]: Tapping sukses | {total_tap} Tap"  , flush=True)
    print(Fore.YELLOW + Style.BRIGHT + f"Getting box..", end="\r" , flush=True)
    time.sleep(2)
    box = get_box(access_token)
    if box is None:
        return
    box_amount = box.get('data', {}).get('boxAmount', 0)
    print(Fore.BLUE + Style.BRIGHT + f"[ Box ]: {box_amount} Box Terbeli"  , flush=True)
    price_levelup = box.get('data', {}).get('levelUpAmount', 0)
    gold_amount = box.get('data', {}).get('goldAmount', 0)
    print(Fore.YELLOW + Style.BRIGHT + f"Getting task..", end="\r" , flush=True)
    time.sleep(2)
    task_list = get_task_list(access_token)
    if task_list is None:
        return
    for task in task_list['data']['taskDetails']:
        if 50 <= task['taskId'] <= 54:
            status = "Complete" if task['finished'] else "Belum Terpenuhi"
            color = Fore.GREEN if task['finished'] else Fore.RED
            print(color + Style.BRIGHT + f"[ Task ]: ID {task['taskId']} | Membutuhkan {task['inviteNum']} invite | Status: {status}        ", flush=True)
        else:
            print(Fore.YELLOW + Style.BRIGHT + f"[ Task ]: ID {task['taskId']} | Reward {task['reward']}        "  , flush=True)
            time.sleep(2)
            task_finish = finish_task(task['taskId'], access_token)
            if task_finish is None:
                return
            elif task_finish['returnDesc'] == 'success':
                print(Fore.GREEN + Style.BRIGHT + f"[ Task ]: ID {task['taskId']} | Reward {task['reward']} Claimed"  , flush=True)

    print(Fore.YELLOW + Style.BRIGHT + f"Leveling up..", end="\r" , flush=True)
    time.sleep(2)
    if level_pet >= 41:
        if gold_amount < price_levelup:
            kurang_amount = price_levelup - gold_amount
            print(Fore.RED + Style.BRIGHT + f"[ Pet ]: Kurang {kurang_amount} $HIT untuk level up"  , flush=True)
        else:
            levelup = level_up_max(access_token,"0")
            if levelup is None:
                return
            print(Fore.GREEN + Style.BRIGHT + f"[ Pet ]: Level up sukses                               "  , flush=True)
    else:
        levelup = level_up_max(access_token,"1")
        if levelup is None:
            return
        print(Fore.GREEN + Style.BRIGHT + f"[ Pet ]: Level up sukses                               "  , flush=True)
# Read the queries from data.txt
with open('data.txt', 'r') as file:
    queries = file.readlines()

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rMenunggu waktu claim berikutnya {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    print("\rMenunggu waktu claim berikutnya selesai.                            ", flush=True)    


def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "DejenDog BOT")
    print(Fore.CYAN + Style.BRIGHT + "Update Link: https://github.com/adearman/dejendog")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")
 
print_welcome_message()
while True:
    try:
        # Process each account
        for query in queries:
            process_account(query.strip())
        animated_loading(120)
    except KeyboardInterrupt:
        print("\nProses dihentikan paksa oleh anda king taptap.")
        break
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        time.sleep(5)
        