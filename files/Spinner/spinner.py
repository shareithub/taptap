import requests
import json
from datetime import datetime, timedelta, timezone
import time  # Tambahkan import time
from colorama import Fore, Style  # Tambahkan import colorama
import os  # Tambahkan import os
import sys
import threading
def read_tokens():
    with open('initdata.txt', 'r') as file:
        return file.read().strip().split('\n')  # Membaca beberapa token

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "SpinnerCoin BOT")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://github.com/adearman/spinnercoin")
    print(Fore.GREEN + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie\n")
    print(Fore.GREEN + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA\n\n")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_data(token):
    url = 'https://back.timboo.pro/api/init-data'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token
    }

    response = requests.post(url, headers=headers, json=data)
    # print(response.json())
    if response.status_code == 200:
        data = response.json()
        user = data.get('initData', {}).get('user', {})
        spinners = data.get('initData', {}).get('spinners', [  ])
        name = user.get('name')
        level = spinners[ 0 ].get('level') if spinners else None
        repair = spinners[ 0 ].get('endRepairTime') if spinners else None
        balance = user.get('balance')
        spinners = data.get('initData', {}).get('spinners', [])
        rarity = spinners[0].get('rarity', {}).get('name') if spinners else None
        print(Fore.GREEN + f"[ Nama ]: {name}" + Style.RESET_ALL)
        print(Fore.GREEN + f"[ Saldo ]: {balance}" + Style.RESET_ALL)
        print(Fore.GREEN + f"[ Level ]: {level}" + Style.RESET_ALL)  # Warna hijau untuk data yang berhasil diambil
        print(Fore.GREEN + f"[ Rarity ]: {rarity}" + Style.RESET_ALL)  # Warna hijau untuk data yang berhasil diambil
        return data
    else:
        print(Fore.RED + "Gaada tokennya ganteng" + Style.RESET_ALL)  # Warna merah jika gagal mengambil data
        return None

def click_spinner(token, repair):
    url = 'https://back.timboo.pro/api/upd-data'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token,
        "data": {
            "clicks": 15,
            "isClose": None
        }
    }

    while True:
        response = requests.post(url, headers=headers, json=data)
        # print(response.json())
        if response.status_code == 200:
            print(Fore.GREEN + "[ Tap ]: Tapping..." + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "[ Tap ]: Tapping selesai..." + Style.RESET_ALL)
            break

    if repair:
        end_time = datetime.strptime(repair, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        remaining_time = end_time - datetime.now(timezone.utc)
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        repair = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        print(f"{Fore.YELLOW}[ Repair ]: Tunggu {repair} lagi..." + Style.RESET_ALL)

def multi_thread_click_spinner(token, repair, num_threads=100):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=click_spinner, args=(token, repair))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


def repair_spinner(token):
    url = 'https://back.timboo.pro/api/repair-spinner'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + "[ Repair ]: Repair spinner sukses..." + Style.RESET_ALL)  # Warna hijau jika repair spinner sukses
    else:
        print(Fore.RED + "[ Repair ]: Repair spinner gagal..." + Style.RESET_ALL)  # Warna merah jika repair spinner gagal

def check_requirement(token, id_tugas):
    url = 'https://api.timboo.pro/check_requirement'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token,
        "requirementId": id_tugas
    }

    response = requests.post(url, headers=headers, json=data)
    time.sleep(2)
    
    try:
        result = response.json()
    except json.JSONDecodeError:
        if response.status_code == 500:
            print(Fore.RED + f"[ Clear Task ]: Internal Server Error. Code {response}" + Style.RESET_ALL)
            return
        else:
            print(Fore.RED + f"[ Clear Task ]: Failed to decode JSON {response}" + Style.RESET_ALL)
        return

    # ... existing code ...
    if response.status_code == 200:
        if result.get('message') == "it's impossible to do the requirement 2 times":
            print(Fore.YELLOW + "[ Clear Task ]: Already Claimed" + Style.RESET_ALL)  # Warna kuning jika task bisa dilakukan 2 kali

        elif not result.get('reward') and not result.get('success'):
            print(Fore.RED + f"[ Clear Task ]: Tidak ada reward. {result.get('message')}" + Style.RESET_ALL)  # Warna merah jika reward gagal
        else:
            print(Fore.GREEN + f"[ Clear Task ]: Sukses clear task | Reward {result.get('reward')} Poin" + Style.RESET_ALL)  # Warna hijau jika reward berhasil
    else:
        print(Fore.RED + f"[ Clear Task ]: Failed to check requirement. {result.get('message')}")

def auto_upgrade(token, spinner_id):
    url = 'https://back.timboo.pro/api/upgrade-spinner'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token,
        "spinnerId": spinner_id
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + "[ Upgrade ]: " + result.get("message", "No message received") + Style.RESET_ALL)  # Warna hijau jika upgrade berhasil
    else:
        print(Fore.RED + "[ Upgrade ]: Failed to upgrade spinner" + Style.RESET_ALL)  # Warna merah jika upgrade gagal

def def_rocket(token, spinner_id):
    url = 'https://back.timboo.pro/api/rocket-activate'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    
    data = {
        "initData": token,
        "spinnerId": spinner_id
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + "[ Rocket ]: Roket Berhasil diaktifkan!" + Style.RESET_ALL)  # Warna hijau jika roket aktif
    else:
        print(Fore.RED + "[ Rocket ]: Tidak ada roket!" + Style.RESET_ALL)  # Warna merah jika gagal aktikan roket

def claim_daily(token):
    url = 'https://api.timboo.pro/open_box'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    
    data = {
        "initData": token,
        "boxId": 8
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + f"[ Claim Daily ]: Claim daily berhasil! Reward: {result.get('reward_text')}" + Style.RESET_ALL)  # Warna hijau jika claim daily berhasil
    else:
        print(Fore.RED + "[ Claim Daily ]: Tidak ada claim daily" + Style.RESET_ALL)  # Warna merah jika claim daily gagal

def def_fullhp(token, spinner_id):
    url = 'https://back.timboo.pro/api/fullhp-activate'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    
    data = {
        "initData": token,
        "spinnerId": spinner_id
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + "[ FullHP ]: " + result.get("message", "No message received") + Style.RESET_ALL)  # Warna hijau jika full hp berhasil
    elif response.status_code == 400:
        print(Fore.RED + "[ FullHP ]: Full HP tidak ada" + Style.RESET_ALL)  # Warna merah jika full hp tidak ada
    else:
        print(Fore.RED + "[ FullHP ]: Gagal mengaktifkan Full HP" + Style.RESET_ALL)  # Warna merah jika gagal mengaktifkan full hp

def main():
    print_welcome_message()
    # Tambahkan pertanyaan untuk auto upgrade
    auto_upgrade_spinner = input("Auto upgrade? y / n (default n): ").strip().lower()
    # Tambahkan pertanyaan untuk mengaktifkan roket
    activate_rocket = input("Gunakan Roket? y / n (default n): ").strip().lower()
    # Tambahkan pertanyaan untuk mengaktifkan full hp
    activate_fullhp = input("Gunakan Bonus HP? y / n (default n): ").strip().lower()
    # Tambahkan pertanyaan untuk auto claim reward
    auto_claim_reward = input("Auto clear task? y / n (default n): ").strip().lower()
    # Tambahkan pertanyaan untuk auto claim daily reward
    auto_claim_daily = input("Auto claim daily reward? y / n (default n): ").strip().lower()
    
    while True:
        tokens = read_tokens()  # Membaca semua token dari file
        for index, token in enumerate(tokens):
            print(f"{Fore.CYAN+Style.BRIGHT}============== [  Akun ke-{index + 1}  ] ==============" + Style.RESET_ALL)  # Mencetak nama akun
            data = get_data(token)
            if data:
                spinners = data.get('initData', {}).get('spinners', [  ])
                if spinners:
                    spinner_id = spinners[ 0 ].get('id')
                    if auto_upgrade_spinner == 'y':
                        auto_upgrade(token, spinner_id)  # Panggil fungsi auto_upgrade jika jawaban 'y'
                repair = spinners[ 0 ].get('endRepairTime') if spinners else None
                repair_spinner(token)
                
                if activate_fullhp == 'y':
                    def_fullhp(token, spinner_id)  # Panggil fungsi def_fullhp jika jawaban 'y'
                if activate_rocket == 'y':
                    def_rocket(token, spinner_id)
                    multi_thread_click_spinner(token, repair)  # Start multi-threaded click_spinner after rocket activation
                else:
                    click_spinner(token, repair)
                if auto_claim_daily == 'y':
                    claim_daily(token)  # Panggil fungsi claim_daily jika jawaban 'y'
                if auto_claim_reward == 'y':
                    for i in range(1, 110):
                        check_requirement(token, i)  # Panggil fungsi check_requirement jika jawaban 'y'

                click_spinner(token, repair)
                
        for i in range(360, 0, -1):
            sys.stdout.write(f"\r{Fore.CYAN+Style.BRIGHT}============ Selesai, tunggu {i} detik.. ============")
            sys.stdout.flush()
            time.sleep(1)
        print()  # Cetak baris baru setelah hitungan mundur selesai

        # Membersihkan konsol setelah hitungan mundur
        clear_console()
        time.sleep(5)  # Tambahkan delay selama 60 detik sebelum mengulang loop  # Tambahkan delay selama 60 detik sebelum mengulang loop

if __name__ == "__main__":
    main()