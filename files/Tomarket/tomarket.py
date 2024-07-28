import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime, timedelta, timezone
import random
import urllib.parse
import base64

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,en-US;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://mini-app.tomarket.ai',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://mini-app.tomarket.ai/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': 'Android',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AG Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.134 Mobile Safari/537.36',
    'x-requested-with': 'org.telegram.messenger.web'
}

 

def load_proxies():
    proxies = []
    try:
        with open('proxy.txt', 'r') as proxy_file:
            proxies = proxy_file.readlines()
    except FileNotFoundError:
        print("Proxy file not found.")
    return [proxy.strip() for proxy in proxies]

proxies = load_proxies()

 

import http.client

 

def get_proxy():
    if proxies:
        proxy = random.choice(proxies)
        user_pass, ip_port = proxy.split('@')
        proxy_username, proxy_password = user_pass.split(':')
        proxy_auth = f"{proxy_username}:{proxy_password}"
        
        return {
            "http": f"http://{proxy_auth}@{ip_port}",
            "https": f"http://{proxy_auth}@{ip_port}",  # Use HTTP for both
        }
    return None


 

def get_access_token(query_data):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/login'
    proxy = get_proxy()
    try:
        data = json.dumps(
            {
                "init_data": query_data,
                "invite_code": "",
            })
        response = requests.post(url, headers=headers, data=data, proxies=proxy)
        response.raise_for_status() 
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Query Anda Salah")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def get_balance(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/balance'
    headers['Authorization'] = token
    proxy = get_proxy()
    try:
        response = requests.post(url, headers=headers, proxies=proxy)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def ghalibie_gacor(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/claim'
    headers['Authorization'] = token
    payload = {"task_id": 41}
    proxy = get_proxy()
    try:
        response = requests.post(url, headers=headers, json=payload,proxies=proxy)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None
    
def claim_daily(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/daily/claim'
    headers['Authorization'] = token
    payload = {"game_id": "fa873d13-d831-4d6f-8aee-9cff7a1d0db1"}
    proxy = get_proxy()

    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxy)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None

def start_farming(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/start'
    headers['Authorization'] = token
    payload = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
    proxy = get_proxy()
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxy)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None
    
def claim_farming(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/claim'
    headers['Authorization'] = token
    payload = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
    proxy = get_proxy()
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxy)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None

def play_game(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/play'
    headers['Authorization'] = token
    payload = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d"}
    proxy = get_proxy()
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxy)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None

def claim_game(token, point):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/claim'
    headers['Authorization'] = token
    payload = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d", "points": point}
    proxy = get_proxy()
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxy)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None


def main():
    tokens = []
    try:
        with open('tokens.txt', 'r') as token_file:
            tokens = token_file.readlines()
    except FileNotFoundError:
        pass
    while True:
        print_welcome_message()
        try:
            with open('query.txt', 'r') as file:
                queries = file.readlines()
 
            for i, query_data in enumerate(queries):
                query_data = query_data.strip()
                if i < len(tokens):
                    token = tokens[i].strip()
                else:
                    print(f"{Fore.YELLOW+Style.BRIGHT}Getting access token..", end="\r", flush=True)
                    auth_response, auth_status = get_access_token(query_data)
           
                    
                    if auth_status == 200:
                        if auth_response['status'] == 200:
                            token = auth_response['data']['access_token']
                            tokens.append(token)
                            with open('tokens.txt', 'a') as token_file:
                                token_file.write(token + '\n')
                        else:
                            print(f"{Fore.RED+Style.BRIGHT}Login Failed {Style.RESET_ALL}           ", flush=True)
                            tokens.append(f'GAGAL AKUN NOMOR {i+1}')
                            with open('tokens.txt', 'a') as token_file:
                                token_file.write(f'GAGAL AKUN NOMOR {i+1} {query_data}')
                            continue
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}Login Failed {Style.RESET_ALL}           ", flush=True)
                        tokens.append(f'GAGAL AKUN NOMOR {i+1}')
                        with open('tokens.txt', 'a') as token_file:
                            token_file.write(f'GAGAL AKUN NOMOR {i+1} {query_data}')
                        continue
                print(f"{Fore.YELLOW+Style.BRIGHT}Checking account..", end="\r", flush=True)
                
                user_data = query_data.split('&')[0].split('=')[1]
                user_info = urllib.parse.unquote(user_data)
                user_info = user_info.replace('%22', '"').replace('%2C', ',').replace('%3A', ':').replace('%24', '$').replace('%23', '#')
                try:
                    user_info = json.loads(user_info)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse user info: {e}")
                    continue
                firstname = user_info.get('first_name', 'Unknown')
                lastname = user_info.get('last_name', '')
                print(Fore.CYAN + Style.BRIGHT + f"===== [ Akun {i+1} - {firstname} {lastname} ] =====             ", flush=True)
                print(f"{Fore.YELLOW+Style.BRIGHT}Getting balance..", end="\r", flush=True)
                proxy = get_proxy()
                if proxy:
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Proxy ]: {proxy['http']} {Style.RESET_ALL}", flush=True)
                else:
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Proxy ]: No Proxy {Style.RESET_ALL}          ", flush=True)
                balance_response = get_balance(token)
                if balance_response is not None:
                    balance = float(balance_response['data'].get('available_balance'))
                    balance = f"{balance:,.0f}".replace(",", ".")  # Format balance with dots as thousand separators
                    tiket = balance_response['data'].get('play_passes')
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Balance ]: {balance} {Style.RESET_ALL}           ", flush=True)
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Tiket ]: {tiket} {Style.RESET_ALL}           ", flush=True)
                    print(f"{Fore.YELLOW+Style.BRIGHT}[ Combo ]: Claiming.. {Style.RESET_ALL}", end="\r" ,flush=True)
                    time.sleep(2)
                    combo = ghalibie_gacor(token)
                    if combo['status'] == 0:
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Combo ]: Claimed!         {Style.RESET_ALL}", flush=True)
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}[ Combo ]: Failed to claim. {combo} {Style.RESET_ALL}", flush=True)
                    print(f"{Fore.YELLOW+Style.BRIGHT}[ Daily ]: Claiming.. {Style.RESET_ALL}", end="\r" ,flush=True)
                    time.sleep(2)
                    daily, daily_status_code = claim_daily(token)
                    if daily_status_code == 400:
                        if daily['message'] == 'already_check':
                            day = daily['data']['check_counter']
                            point = daily['data']['today_points']
                            print(f"{Fore.GREEN+Style.BRIGHT}[ Daily ]: Day {day} Already checkin | {point} Point{Style.RESET_ALL}", flush=True)
                        else:
                            print(f"{Fore.RED+Style.BRIGHT}[ Daily ]: Gagal {daily} {Style.RESET_ALL}", flush=True)
                    elif daily_status_code == 200:
                        day = daily['data']['check_counter']
                        point = daily['data']['today_points']
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Daily ]: Day {day} Claimed | {point} Point{Style.RESET_ALL}", flush=True)
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}[ Daily ]: Gagal {daily} {Style.RESET_ALL}", flush=True)

                    print(f"{Fore.YELLOW+Style.BRIGHT}[ Farming ]: Checking.. {Style.RESET_ALL}", end="\r", flush=True)
                    time.sleep(2)
                    farming, farming_status_code = start_farming(token)
                    if farming_status_code == 200:
                        end_time = datetime.fromtimestamp(farming['data']['end_at'])
                        remaining_time = end_time - datetime.now()
                        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                        minutes, _ = divmod(remainder, 60)
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Farming ]: Started. Claim in: {int(hours)} jam {int(minutes)} menit {Style.RESET_ALL}", flush=True)
                        if datetime.now() > end_time:
                                print(f"{Fore.YELLOW+Style.BRIGHT}[ Farming ]: Claiming.. {Style.RESET_ALL}", end="\r", flush=True)
                                claim_response, claim_status_code = claim_farming(token)
                                if claim_status_code == 200:
                                    poin = claim_response["data"]["claim_this_time"]
                                    print(f"{Fore.GREEN+Style.BRIGHT}[ Farming ]: Success Claim Farming! Reward: {poin} {Style.RESET_ALL}       ", flush=True)
                                    print(f"{Fore.YELLOW+Style.BRIGHT}[ Farming ]: Starting.. {Style.RESET_ALL}", end="\r", flush=True)
                                    time.sleep(2)
                                    farming, farming_status_code = start_farming(token)
                                    if farming_status_code == 200:
                                        end_time = datetime.fromtimestamp(farming['data']['end_at'])
                                        remaining_time = end_time - datetime.now()
                                        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                                        minutes, _ = divmod(remainder, 60)
                                        print(f"{Fore.GREEN+Style.BRIGHT}[ Farming ]: Started. Claim in: {int(hours)} jam {int(minutes)} menit {Style.RESET_ALL}", flush=True)

                                else:
                                    print(f"{Fore.RED+Style.BRIGHT}Failed to claim farming: {claim_response} {Style.RESET_ALL}          ", flush=True)
                    elif farming_status_code == 500:
                        if farming['message'] == 'game already started':
                            end_time = datetime.fromtimestamp(farming['data']['end_at'])
                            remaining_time = end_time - datetime.now()
                            hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                            minutes, _ = divmod(remainder, 60)
                            print(f"{Fore.CYAN+Style.BRIGHT}[ Farming ]: Already Started. Claim in: {int(hours)} jam {int(minutes)} menit {Style.RESET_ALL}", flush=True)
                            
                            # Check if current time is past end_time
                            if datetime.now() > end_time:
                                print(f"{Fore.YELLOW+Style.BRIGHT}[ Farming ]: Claiming.. {Style.RESET_ALL}", end="\r", flush=True)
                                claim_response, claim_status_code = claim_farming(token)
                                if claim_status_code == 200:
                                    poin = claim_response["data"]["claim_this_time"]
                                    print(f"{Fore.GREEN+Style.BRIGHT}Success claim farming! Reward: {poin} {Style.RESET_ALL}", flush=True)
                                    print(f"{Fore.YELLOW+Style.BRIGHT}[ Farming ]: Starting.. {Style.RESET_ALL}", end="\r", flush=True)
                                    time.sleep(2)
                                    farming, farming_status_code = start_farming(token)
                                    if farming_status_code == 200:
                                        end_time = datetime.fromtimestamp(farming['data']['end_at'])
                                        remaining_time = end_time - datetime.now()
                                        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                                        minutes, _ = divmod(remainder, 60)
                                        print(f"{Fore.GREEN+Style.BRIGHT}[ Farming ]: Started. Claim in: {int(hours)} jam {int(minutes)} menit {Style.RESET_ALL}", flush=True)


                                else:
                                    print(f"{Fore.RED+Style.BRIGHT}Failed to claim farming: {claim_response} {Style.RESET_ALL}", flush=True)
                        else:
                            print(f"{Fore.GREEN+Style.BRIGHT}[ Farming ]: Error. {farming} {Style.RESET_ALL}", flush=True)
                    else:
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Farming ]: Error {farming} {Style.RESET_ALL}", flush=True)
                    
                    while tiket > 0:
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Game ]: Starting Game..", end="\r", flush=True)
                        play, play_status = play_game(token)
                        if play_status != 200:
                            print(f"{Fore.RED+Style.BRIGHT}[ Game ]: Failed to start game!       {Style.RESET_ALL}", flush=True)
                        else:
                            print(f"{Fore.GREEN+Style.BRIGHT}[ Game ]: Game Started! {Style.RESET_ALL}                      ", flush=True)
                            for _ in range(30):
                                print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE])+Style.BRIGHT}[ Game ]: Playing game, waktu sisa {30 - _} detik {Style.RESET_ALL}", end="\r", flush=True)
                                time.sleep(1)
                            print(f"{Fore.YELLOW+Style.BRIGHT}[ Game ]: Game Berakhir! Claiming..                                       ", end="\r", flush=True)
                            point = random.randint(400, 600)
                            claim, claim_status = claim_game(token, point)
                            if claim_status != 200:
                                print(f"{Fore.RED+Style.BRIGHT}[ Game ]: Failed to claim game points! {Style.RESET_ALL}", flush=True)
                            else:
                                print(f"{Fore.GREEN+Style.BRIGHT}[ Game ]: Success. Mendapatkan {point} Poin {Style.RESET_ALL}                    ", flush=True)

                            tiket -= 1
            print(Fore.BLUE + Style.BRIGHT + f"\n==========SEMUA AKUN TELAH DI PROSES==========\n",  flush=True)    
            for _ in range(1800):
                minutes, seconds = divmod(1800 - _, 60)
                print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE])+Style.BRIGHT}==== [ Semua akun telah diproses, Looping berikutnya {minutes} menit {seconds} detik ] ===={Style.RESET_ALL}", end="\r", flush=True)
                time.sleep(1)         
        except Exception as e:
            time.sleep(5)
            print(f"An error occurred: {str(e)}")
            continue  # Add this line to skip to the next account
       

from datetime import datetime, timedelta, timezone
start_time = datetime.now()
def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Tomarket BOT")
    print(Fore.CYAN + Style.BRIGHT + "Update Link: https://github.com/adearman/tomarket")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n")
    current_time = datetime.now()
    up_time = current_time - start_time
    days, remainder = divmod(up_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(Fore.CYAN + Style.BRIGHT + f"Up time bot: {int(days)} hari, {int(hours)} jam, {int(minutes)} menit, {int(seconds)} detik\n\n")

if __name__ == "__main__":
    main()