import requests
import json
import time
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Tambahkan variabel global untuk menyimpan pilihan combo
auto_claim_daily_combo = None
combo_list = []

def load_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def get_headers(token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

def get_token(init_data_raw):
    url = 'https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['authToken']
        elif response.status_code == 403:
            print(Fore.RED + Style.BRIGHT + "\rAkses Ditolak. Status 403", flush=True)
        elif response.status_code == 500:
            print(Fore.RED + Style.BRIGHT + "\rInternal Server Error", flush=True)
        else:
            error_data = response.json()
            if "invalid" in error_data.get("error_code", "").lower():
                print(Fore.RED + Style.BRIGHT + "\rGagal Mendapatkan Token. Data init tidak valid", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"\rGagal Mendapatkan Token. {error_data}", flush=True)
    except requests.exceptions.Timeout:
        print(Fore.RED + Style.BRIGHT + "\rGagal Mendapatkan Token. Request Timeout", flush=True)
    except requests.exceptions.ConnectionError:
        print(Fore.RED + Style.BRIGHT + "\rGagal Mendapatkan Token. Kesalahan Koneksi", flush=True)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\rGagal Mendapatkan Token. Error: {str(e)}", flush=True)
    return None

def authenticate(token):
    url = 'https://api.hamsterkombatgame.io/auth/me-telegram'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

# Debugging untuk melihat apa yang dikirim dalam request
def debug_request(url, headers, data=None):
    print(f"Request URL: {url}")
    print(f"Headers: {headers}")
    if data:
        print(f"Data: {data}")

# Contoh penggunaan fungsi get_token dengan debugging
init_data_raw = "data_init_sample"  # Ganti dengan data yang valid
debug_request('https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp', {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://hamsterkombatgame.io',
    'Referer': 'https://hamsterkombatgame.io/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}, json.dumps({"initDataRaw": init_data_raw}))

token = get_token(init_data_raw)
if token:
    print("Token obtained successfully:", token)
else:
    print("Failed to obtain token.")


def sync_clicker(token):
    url = 'https://api.hamsterkombatgame.io/clicker/sync'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def claim_daily(token):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = requests.post(url, headers=headers, data=data)
    return response
def upgrade(token, upgrade_type):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response


def tap(token, max_taps, available_taps):
    url = 'https://api.hamsterkombatgame.io/clicker/tap'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"count": max_taps, "availableTaps": available_taps, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def list_tasks(token):
    url = 'https://api.hamsterkombatgame.io/clicker/list-tasks'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def exchange(token):
    url = 'https://api.hamsterkombatgame.io/clicker/select-exchange'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"exchangeId": 'okx'})
    response = requests.post(url, headers=headers, data=data)
    return response



def claim_cipher(token, cipher_text):
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-cipher'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"cipher": cipher_text})
    response = requests.post(url, headers=headers, data=data)
    
    # Tambahkan pengecekan status code dan konten respons
    if response.status_code == 200:
        try:
            # Coba parse JSON dan lanjutkan proses
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Gagal mengurai JSON dari respons.", flush=True)
            return None
    elif response.status_code == 400:
        try:
            # Coba parse JSON dan lanjutkan proses
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Gagal mengurai JSON dari respons.", flush=True)
            return None
    elif response.status_code == 500:
        print(Fore.RED + Style.BRIGHT + f"Gagal claim cipher, Internal Server Error", flush=True)
        return response
    else:
        print(Fore.RED + Style.BRIGHT + f"Gagal claim cipher, status code: {response.status_code}", flush=True)
        return None

def check_task(token, task_id):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    response = requests.post(url, headers=headers, data=data)
    return response
def cek_booster(token):
    url = 'https://api.hamsterkombatgame.io/clicker/boosts-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response
def use_booster(token):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": "BoostFullAvailableTaps", "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response


def read_upgrade_list(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]



def get_available_upgrades(token):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            # print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade Minning ] : Berhasil mendapatkan list upgrade.", flush=True)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade Minning ] : Gagal mendapatkan response JSON.", flush=True)
            return []
    else:
        print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Gagal mendapatkan daftar upgrade: Status {response.status_code}", flush=True)
        return []


def buy_upgrade(token, upgrade_id, upgrade_name):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    time.sleep(3)
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade Minning ] : Upgrade {upgrade_name} berhasil dibeli.", flush=True)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade Minning ] : Gagal mengurai JSON saat upgrade.", flush=True)
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Coin tidak cukup wkwkw :V                             ", flush=True)
                return 'insufficient_funds'
            elif error_response.get('error_code') == 'UPGRADE_COOLDOWN':
                cooldown_seconds = error_response.get('cooldownSeconds', 0)
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Upgrade {upgrade_name} masih dalam cooldown. Tersisa {cooldown_seconds} detik.", flush=True)
                return {'cooldown': True, 'cooldown_seconds': cooldown_seconds}
            else:
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Failed upgrade {upgrade_name}: {error_response}", flush=True)
                return {'error': True, 'message': error_response}
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Gagal mendapatkan respons JSON. Status: {response.status_code}", flush=True)
            return {'error': True, 'status_code': response.status_code}
def get_available_upgrades_combo(token):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Berhasil mendapatkan list upgrade.", flush=True)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo ] : Gagal mendapatkan response JSON.", flush=True)
            return []
    else:
        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal mendapatkan daftar upgrade: Status {response.status_code}", flush=True)
        return []


def buy_upgrade_combo(token, upgrade_id):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Combo {upgrade_id} berhasil dibeli.", flush=True)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo ] : Gagal mengurai JSON saat upgrade.", flush=True)
        return response
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Coin tidak cukup.", flush=True)
                return 'insufficient_funds'
            else:
                # print(f"error saat beli combo: {error_response}")
                # print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Error: {error_response.get('error_message', 'No error message provided')}", flush=True)
                return error_response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal mendapatkan respons JSON. Status: {response.status_code}", flush=True)
            return None

def auto_upgrade_passive_earn(token, max_price):
    upgrade_list = read_upgrade_list('upgrade_list.txt')
    insufficient_funds = False
    cooldown_upgrades = {}  # Dictionary untuk menyimpan waktu cooldown yang tersisa untuk setiap upgrade

    while not insufficient_funds:
        available_upgrades = get_available_upgrades(token)
        best_upgrade = None
        best_value = 0

        current_time = time.time()

        for upgrade in available_upgrades:
            if upgrade['id'] in upgrade_list and upgrade['isAvailable'] and not upgrade['isExpired']:
                # Periksa apakah upgrade sedang dalam cooldown dan apakah cooldown sudah berakhir
                if upgrade['id'] in cooldown_upgrades and current_time < cooldown_upgrades[upgrade['id']]:
                    continue  # Skip upgrade ini karena masih dalam cooldown

                price = upgrade['price']
                # Skip upgrade jika harga lebih dari max_price
                if price > max_price:
                    print(Fore.YELLOW + Style.BRIGHT + f"[ Upgrade Minning ] : Upgrade {upgrade['name']} dilewati karena harga terlalu tinggi: {price}")
                    continue

                profit_per_hour = upgrade['profitPerHour']
                value = profit_per_hour / price  # Menghitung nilai per dolar yang diinvestasikan

                if value > best_value:
                    best_value = value
                    best_upgrade = upgrade

        if best_upgrade:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade Minning ] : Mencoba upgrade: {best_upgrade['name']} Profit : {best_upgrade['profitPerHour']} Harga : {best_upgrade['price']}", flush=True)
            result = buy_upgrade(token, best_upgrade['id'], best_upgrade['name'])
            if result == 'insufficient_funds':
                print(Fore.RED + Style.BRIGHT + "[ Upgrade Minning ] : Coin tidak cukup.")
                insufficient_funds = True
            elif isinstance(result, dict) and 'cooldown' in result:
                cooldown_seconds = result['cooldown_seconds']
                cooldown_end_time = current_time + cooldown_seconds
                cooldown_upgrades[best_upgrade['id']] = cooldown_end_time
                print(Fore.YELLOW + Style.BRIGHT + f"[ Upgrade Minning ] : Upgrade {best_upgrade['name']} masih dalam cooldown. Tersisa {cooldown_seconds // 60} menit {cooldown_seconds % 60} detik.")
            elif isinstance(result, dict) and 'error' in result:
                print(Fore.RED + Style.BRIGHT + f"[ Upgrade Minning ] : Gagal upgrade dengan error: {result.get('message', 'No error message provided')}")
        else:
            print(Fore.YELLOW + Style.BRIGHT + "[ Upgrade Minning ] : Tidak ada upgrade yang memenuhi kriteria saat ini.")
            break  # Keluar dari loop jika tidak ada upgrade yang tersedia
def check_and_upgrade(token, upgrade_id, required_level):
    upgrades = get_available_upgrades_combo(token)
    if upgrades:
        for upgrade in upgrades:
      
            if upgrade['id'] == upgrade_id and upgrade['level'] < required_level + 1:
                print(Fore.CYAN + Style.BRIGHT + f"[ Daily Combo ] : Upgrading {upgrade_id}", flush=True)
                req_level_total = required_level +1
                for _ in range(req_level_total - upgrade['level']):
                    result = buy_upgrade_combo(token, upgrade_id)
                    # print("buying..")
                    if isinstance(result, dict) and 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                        # print("ada error")
                        needed_upgrade = result['error_message'].split(':')[-1].strip().split()
                        needed_upgrade_id = needed_upgrade[1]
                        needed_upgrade_level = int(needed_upgrade[-1])
                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ Daily Combo ] : Mencoba membeli {needed_upgrade_id} level {needed_upgrade_level}", flush=True)
                        if check_and_upgrade(token, needed_upgrade_id, needed_upgrade_level):
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Berhasil upgrade {needed_upgrade_id} ke level {needed_upgrade_level}. Mencoba kembali upgrade {upgrade_id}.", flush=True)
                            continue  # Setelah berhasil, coba lagi upgrade asli
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal upgrade {needed_upgrade_id} ke level {needed_upgrade_level}", flush=True)
                            return False
                    elif result == 'insufficient_funds':
                        print("coin")
                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Coin tidak cukup untuk upgrade {upgrade_id}", flush=True)
                        return False
                    elif result.status_code != 200:
                        print(f"error response : {result}")
                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal upgrade {upgrade_id} dengan error: {result}", flush=True)
                        return False
                print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Upgrade {upgrade_id} berhasil dilakukan ke level {required_level}", flush=True)
                return True
    # print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Upgrade {upgrade_id} berhasil dilakukan ke level {required_level}", flush=True)
    return False
import requests

def claim_daily_combo(token):
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-combo'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(Fore.GREEN + Style.BRIGHT + "\r[ Daily Combo ] : Berhasil mengklaim daily combo.                                          ", flush=True)
        return response.json()
    else:
        error_response = response.json()
        if error_response.get('error_code') == 'DAILY_COMBO_DOUBLE_CLAIMED':
            print(Fore.YELLOW + Style.BRIGHT + "\r[ Daily Combo ] : Claimed          ", flush=True)
        else:
            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Faile. {response}", flush=True)
        return error_response
    
def check_combo_purchased(token):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        purchased_combos = data.get('dailyCombo', {}).get('upgradeIds', [])
        return purchased_combos
    else:
        print(Fore.RED + Style.BRIGHT + f"Gagal mendapatkan status combo. Status: {response.status_code}", flush=True)
        return None

# MAIN CODE
cek_task_dict = {}
claimed_ciphers = set()

combo_upgraded = {}
def main():
    global cek_task_dict, claimed_ciphers, auto_claim_daily_combo, combo_list, combo_upgraded
    
    print_welcome_message()
    print(Fore.GREEN + Style.BRIGHT + "Starting Hamster Kombat....\n\n")
    init_data = load_tokens('initdata.txt')
    token_cycle = cycle(init_data)

    
    token_dict = {}  # Dictionary to store successful tokens
    while True:
        init_data_raw = next(token_cycle)
        token = token_dict.get(init_data_raw)
        
        if token:
            print(Fore.GREEN + Style.BRIGHT + f"\n\n\rMenggunakan token yang sudah ada...", end="", flush=True)
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\n\n\rMendapatkan token...              ", end="", flush=True)

            token = get_token(init_data_raw)
            # print(token)
            if token:
                token_dict[init_data_raw] = token
                print(Fore.GREEN + Style.BRIGHT + f"\n\n\rBerhasil mendapatkan token    ", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"\n\n\rBeralih ke akun selanjutnya\n\n", flush=True)
                continue  # Lanjutkan ke iterasi berikutnya jika gagal mendapatkan token

         # Inisialisasi status combo_upgraded untuk token ini jika belum ada
        if init_data_raw not in combo_upgraded:
            combo_upgraded[init_data_raw] = False

        response = authenticate(token)
   
        ## TOKEN AMAN
        if response.status_code == 200:

            user_data = response.json()
            username = user_data.get('telegramUser', {}).get('username', 'Username Kosong')
            firstname = user_data.get('telegramUser', {}).get('firstName', 'Kosong')
            lastname = user_data.get('telegramUser', {}).get('lastName', 'Kosong')
            
            print(Fore.GREEN + Style.BRIGHT + f"\r\n======[{Fore.WHITE + Style.BRIGHT} {username} | {firstname} {lastname} {Fore.GREEN + Style.BRIGHT}]======")

            # Sync Clicker
            print(Fore.GREEN + f"\rGetting info user...", end="", flush=True)
            response = sync_clicker(token)
            if response.status_code == 200:
                clicker_data = response.json()['clickerUser']
                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Level ] : {clicker_data['level']}          ", flush=True)
                print(Fore.YELLOW + Style.BRIGHT + f"[ Total Earned ] : {int(clicker_data['totalCoins'])}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Coin ] : {int(clicker_data['balanceCoins'])}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Energy ] : {clicker_data['availableTaps']}")
                boosts = clicker_data['boosts']
                boost_max_taps_level = boosts.get('BoostMaxTaps', {}).get('level', 0)
                boost_earn_per_tap_level = boosts.get('BoostEarnPerTap', {}).get('level', 0)
                
                print(Fore.CYAN + Style.BRIGHT + f"[ Level Energy ] : {boost_max_taps_level}")
                print(Fore.CYAN + Style.BRIGHT + f"[ Level Tap ] : {boost_earn_per_tap_level}")
                print(Fore.CYAN + Style.BRIGHT + f"[ Exchange ] : {clicker_data['exchangeId']}")
                # print(clicker_data['exchangeId'])
                if clicker_data['exchangeId'] == None:
                    print(Fore.GREEN + '\rSeting exchange to OKX..',end="", flush=True)
                    exchange_set = exchange(token)

                    if exchange_set.status_code == 200:
                        print(Fore.GREEN + Style.BRIGHT +'\rSukses set exchange ke OKX', flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT +'\rGagal set exchange', flush=True)
                print(Fore.CYAN + Style.BRIGHT + f"[ Passive Earn ] : {clicker_data['earnPassivePerHour']}\n")
                
                
                print(Fore.GREEN + f"\r[ Tap Status ] : Tapping ...", end="", flush=True)



                response = tap(token, clicker_data['maxTaps'], clicker_data['availableTaps'])
                if response.status_code == 200:
                    print(Fore.GREEN + Style.BRIGHT + "\r[ Tap Status ] : Tapped            ", flush=True)
                    print(Fore.CYAN + Style.BRIGHT + f"\r[ Booster ] : Checking booster...", end="", flush=True)
                    response = cek_booster(token)
                    if response.status_code == 200:
                        booster_info = response.json()['boostsForBuy']
                        for boost in booster_info:
                            if boost['id'] == 'BoostFullAvailableTaps':
                                stock = boost['maxLevel'] - boost['level'] 
                                cooldown = boost['cooldownSeconds'] // 60
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Booster ] : Stock {stock} | Cooldown {cooldown} menit    ", flush=True)
                        if cooldown == 0:
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Boosted ] : Activing Booster..", end="", flush=True)
                            response = use_booster(token)
                            if response.status_code == 200:
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Boosted ] : Booster Activated", flush=True)   
                            elif response.status_code == 400:
                                error_info = response.json()
                                if error_info.get('error_code') == 'BOOST_COOLDOWN':
                                    cooldown_seconds = int(error_info.get('error_message').split()[-2])
                                    cooldown_minutes = cooldown_seconds // 60
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Boosted ] : Booster dalam cooldown {cooldown_minutes} menit", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Boosted ] : Gagal mengaktifkan booster", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"\r[ Boosted ] : Failed to activate booster", flush=True)

                        

                    else:
                        print(Fore.RED + Style.BRIGHT + "\r[ Booster ] : Tap Status : Gagal Tap           ", flush=True)

                
                else:
                    print(Fore.RED + Style.BRIGHT + "\r[ Tap Status ] : Gagal Tap           ", flush=True)
                    # continue 
                print(Fore.GREEN + f"\r[ Checkin Daily ] : Checking...", end="", flush=True)

                time.sleep(1)
                # Check Task
                response = claim_daily(token)
                if response.status_code == 200:
                    daily_response = response.json()['task']
                    if daily_response['isCompleted']:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Checkin Daily ] Days {daily_response['days']} | Completed", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Checkin Daily ] Days {daily_response['days']} | Belum saat nya claim daily", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Checkin Daily ] Gagal cek daily {response.status_code}", flush=True)
                
                if ask_cipher == 'y':
                    if token not in claimed_ciphers:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Claim Cipher ] : Claiming cipher...", end="", flush=True)
                        response = claim_cipher(token, cipher_text)
                        try:
                            if response.status_code == 200:
                                bonuscoins = response.json()['dailyCipher']['bonusCoins']
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Claim Cipher ] : Berhasil claim cipher | {bonuscoins} bonus coin", flush=True)
                                claimed_ciphers.add(token)
                            else:
                                error_info = response.json()
                                if error_info.get('error_code') == 'DAILY_CIPHER_DOUBLE_CLAIMED':
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Cipher already claimed", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Gagal claim cipher dengan error: {error_info.get('error_message', 'No error message')}", flush=True)
                        except json.JSONDecodeError:
                            print(Fore.RED + Style.BRIGHT + "\r[ Claim Cipher ] : Gagal mengurai JSON dari respons.", flush=True)
                        except Exception as e:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Terjadi error: {str(e)}", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Cipher sudah pernah di-claim sebelumnya.", flush=True)
                # daily combo
                if auto_claim_daily_combo == 'y' and not combo_upgraded[init_data_raw]:
                    cek = claim_daily_combo(token)
                    if cek.get('error_code') != 'DAILY_COMBO_DOUBLE_CLAIMED':
                        purchased_combos = check_combo_purchased(token)
                        if purchased_combos is None:
                            print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo ] : Gagal mendapatkan status combo, akan mencoba lagi dengan akun berikutnya.", flush=True)
                        else:
                            for combo in combo_list:
                                if combo in purchased_combos:
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : {combo} sudah dibeli.", flush=True)
                                else:
                                    print(Fore.GREEN + f"\r[ Daily Combo ] : Buying {combo}", flush=True)
                                    result = buy_upgrade_combo(token, combo)
                                    if result == 'insufficient_funds':
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal membeli {combo} coin tidak cukup", flush=True)
                                    elif 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                                        #print(upgrade_details = result['error_message'])
                                        upgrade_details = result['error_message'].split(':')[-1].strip().split()
                                        upgrade_key = upgrade_details[1]
                                        upgrade_level = int(upgrade_details[-1])
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal beli {combo} membutuhkan {upgrade_key} level {upgrade_level}", flush=True)    
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Mencoba membeli {upgrade_key} level {upgrade_level}", flush=True)    
                                        result = check_and_upgrade(token, upgrade_key, upgrade_level)
                            combo_upgraded[init_data_raw] = True
                            required_combos = set(combo_list)
                            purchased_combos = set(check_combo_purchased(token))
                            if purchased_combos == required_combos:
                                print(Fore.GREEN + Style.BRIGHT + "\r[ Daily Combo ] : Semua combo telah dibeli, mencoba mengklaim daily combo.                 ", end="" ,flush=True)
                                claim_daily_combo(token)
                            else:
                                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Daily Combo ] : Gagal. Combo yang belum dibeli: {required_combos - purchased_combos}               " , flush=True)
                                combo_upgraded[init_data_raw] = False
                                # Tambahkan loop untuk mencoba lagi
                                continue

                    
                
                # Upgrade 
                # if auto_upgrade_energy == 'y':
                #     print(Fore.GREEN + f"\r[ Upgrade ] : Upgrading Energy....", end="", flush=True)
                #     upgrade_response = upgrade(token, "BoostMaxTaps")
                #     if upgrade_response.status_code == 200:
                #         level_boostmaxtaps = upgrade_response.json()['clickerUser']['boosts']['BoostMaxTaps']['level']
                #         print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade ] : Energy Upgrade to level {level_boostmaxtaps}", flush=True)
                #     else:
                #         print(Fore.RED + Style.BRIGHT + "\r[ Upgrade ] : Failed to upgrade energy", flush=True)
                # if auto_upgrade_multitap == 'y':
                #     print(Fore.GREEN + f"\r[ Upgrade ] : Upgrading MultiTap....", end="", flush=True)
                #     upgrade_response = upgrade(token, "BoostEarnPerTap")
                #     if upgrade_response.status_code == 200:
                #         level_boostearnpertap = upgrade_response.json()['clickerUser']['boosts']['BoostEarnPerTap']['level']
                #         print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade ] : MultiTap Upgrade to level {level_boostearnpertap}", flush=True)
                #     else:
                #         print(Fore.RED + Style.BRIGHT + "\r[ Upgrade ] : Failed to upgrade multitap", flush=True)
            
                # List Tasks
                print(Fore.GREEN + f"\r[ List Task ] : Checking...", end="", flush=True)
                if cek_task_list == 'y':
                    if token not in cek_task_dict:  # Pastikan token ada dalam dictionary
                        cek_task_dict[token] = False  # Inisialisasi jika belum ada
                    if not cek_task_dict[token]:  # Cek status cek_task untuk token ini
                        response = list_tasks(token)
                        cek_task_dict[token] = True  # Set status cek_task menjadi True setelah dicek
                        if response.status_code == 200:
                            tasks = response.json()['tasks']
                            all_completed = all(task['isCompleted'] or task['id'] == 'invite_friends' for task in tasks)
                            if all_completed:
                                print(Fore.GREEN + Style.BRIGHT + "\r[ List Task ] : Semua task sudah diclaim\n", flush=True)
                            else:
                                for task in tasks:
                                    if not task['isCompleted']:
                                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ List Task ] : Claiming {task['id']}...", end="", flush=True)
                                        response = check_task(token, task['id'])
                                        if response.status_code == 200 and response.json()['task']['isCompleted']:
                                            print(Fore.GREEN + Style.BRIGHT + f"\r[ List Task ] : Claimed {task['id']}\n", flush=True)
                                        else:
                                            print(Fore.RED + Style.BRIGHT + f"\r[ List Task ] : Gagal Claim {task['id']}\n", flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ List Task ] : Gagal mendapatkan list task {response.status_code}\n", flush=True)
                else:
                    print(Fore.GREEN + f"\r[ List Task ] : Skipped...", end="", flush=True)   
                # else:
                    # print(Fore.GREEN + Style.BRIGHT + "\r[ List Task ] : Sudah di cek dan claimed", flush=True)
                    
                # cek upgrade
                
                if auto_upgrade_passive == 'y':
                    print(Fore.GREEN + f"\r[ Upgrade Minning ] : Checking...", end="", flush=True)
                    auto_upgrade_passive_earn(token, max_price)
                    
            else:


                print(Fore.RED + Style.BRIGHT + f"\r Gagal mendapatkan info user {response.status_code}", flush=True)



        ## TOKEN MATI        
        elif response.status_code == 401:
            error_data = response.json()
            if error_data.get("error_code") == "NotFound_Session":
                print(Fore.RED + Style.BRIGHT + f"=== [ Token Invalid {token} ] ===")
                token_dict.pop(init_data_raw, None)  # Remove invalid token
                token = None  # Set token ke None untuk mendapatkan token baru di iterasi berikutnya
            else:
                print(Fore.RED + Style.BRIGHT + "Authentication failed with unknown error")
        else:
            print(Fore.RED + Style.BRIGHT + f"Error with status code: {response.status_code}")
            token = None  # Set token ke None jika terjadi error lain
            
        time.sleep(1)



# while True:
#     auto_upgrade_energy = input("Upgrade Energy (default n) ? (y/n): ").strip().lower()
#     if auto_upgrade_energy in ['y', 'n', '']:
#         auto_upgrade_energy = auto_upgrade_energy or 'n'
#         break
#     else:
#         print("Masukkan 'y' atau 'n'.")

# while True:
#     auto_upgrade_multitap = input("Upgrade Multitap (default n) ? (y/n): ").strip().lower()
#     if auto_upgrade_multitap in ['y', 'n', '']:
#         auto_upgrade_multitap = auto_upgrade_multitap or 'n'
#         break
#     else:
#         print("Masukkan 'y' atau 'n'.")
while True:
    auto_upgrade_passive = input("Auto Upgrade Mining (Passive Earn)? (default n) (y/n): ").strip().lower()
    if auto_upgrade_passive in ['y', 'n', '']:
        auto_upgrade_passive = auto_upgrade_passive or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

if auto_upgrade_passive == 'y':
    while True:
        max_price = input("Masukkan harga maksimum upgrade ? (contoh 1500000): ")
        if max_price:
            max_price = int(max_price)
            break
        else:
            print("Masukkan harga maksimum upgrade blok!.")

while True:
    cek_task_list = input("Enable Cek Task? (default n) (y/n): ").strip().lower()
    if cek_task_list in ['y', 'n', '']:
        cek_task_list = cek_task_list or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

while True:
    ask_cipher = input("Auto Claim Cipher Daily / Sandi Harian? (default n) (y/n): ").strip().lower()
    if ask_cipher in ['y', 'n', '']:
        ask_cipher = ask_cipher or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

if ask_cipher == 'y':
    while True:
        cipher_text = input("Masukkan cipher nya / sandi harian : ")
        if cipher_text:
            break
        else:
            print("Masukkan sandi harian blok!.")
auto_claim_daily_combo = input("Auto Claim Daily Combo? (default n) (y/n): ").strip().lower() or 'n'
if auto_claim_daily_combo == 'y':
    for i in range(1, 4):  # Asumsi ada 3 combo
        combo = input(f"Masukkan id combo {i}: ")
        combo_list.append(combo)
def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Hamster Kombat BOT!")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://github.com/adearman/hamsterkombat")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")

if __name__ == "__main__":
    main()