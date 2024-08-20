import requests
import os
import time
from colorama import Fore, Style
import json
from datetime import datetime
import urllib.parse
import random

# Function to parse user data from data.txt
def parse_user_data(file_path):
    user_data_list = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if "user=" in line:
                user_data_encoded = line.split('user=')[1].split('&')[0]
                user_data_json = urllib.parse.unquote(user_data_encoded)
                user_data = json.loads(user_data_json)
                user_data_list.append((line.strip(), user_data))
    return user_data_list
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://tgapp.matchain.io',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://tgapp.matchain.io/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

def get_token(line, user_data):
    payload = {
        "uid": user_data["id"],
        "first_name": user_data["first_name"],
        "last_name": user_data["last_name"],
        "username": user_data.get("username", ""),
        "tg_login_params": line
    }
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/user/login'
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Query Anda Salah")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def get_profile(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/user/profile'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def get_farming_reward(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None
    
def claim_farming_reward(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def start_farming(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/farming'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None
    
def get_ref_reward(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/invite/balance'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def claim_ref_reward(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/invite/claim'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def get_task(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/list'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def complete_task(user_data,task_name, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/complete'
    headers['Authorization'] = token
    payload = {
            "uid": user_data["id"],
            "type": task_name
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None
def claim_task(user_data,task_name, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/claim'
    headers['Authorization'] = token
    payload = {
            "uid": user_data["id"],
            "type": task_name
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def check_tiket(token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/rule'
    headers['Authorization'] = token

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def play_game(token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/play'
    headers['Authorization'] = token
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None
def claim_game(game_id,point, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/claim'
    headers['Authorization'] = token
    payload = {
        "game_id": game_id,
        "point": point
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def check_boost_status(token):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/daily/task/status"
    headers['Authorization'] = token
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None
    
def purchase_boost(token, uid):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/daily/task/purchase"
    headers['Authorization'] = token
    payload = {"uid": uid,"type":"game"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None


def calculate_default_score(rule):
    big_fire_count = 0
    small_fire_count = 0
    magnifier_count = 0
    bomb_count = 0
    total_score = 0

    for level in rule:
        for key, objects in level.items():
            for obj in objects:
                if obj['objectType'] == 'bigFire':
                    big_fire_count += 1
                    total_score += obj['score']
                elif obj['objectType'] == 'smallFire':
                    small_fire_count += 1
                    total_score += obj['score']
                elif obj['objectType'] == 'magnifier':
                    magnifier_count += 1
                elif obj['objectType'] == 'bomb':
                    bomb_count += 1

    return big_fire_count, small_fire_count, magnifier_count, bomb_count, total_score

def check_quiz(token):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/daily/quiz/progress"
    headers['Authorization'] = token
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request Error: {e}")
        return None
    
def submit_quiz(token, selected_item):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/daily/quiz/submit"
    headers['Authorization'] = token
    payload = {"answer_result": selected_item}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request Error: {e}")
        return None

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rMenunggu waktu claim berikutnya {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    print("\rMenunggu waktu claim berikutnya selesai.                            ", flush=True)

start_time = datetime.now()

user_data_list = parse_user_data('data.txt')

def format_balance(balance):
    if balance < 1000:
        return str(balance)
    return f"{balance // 1000}"

def convert_ts(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

# Function to clear the terminal screen
def clear_terminal():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux, Mac, etc.
        os.system('clear')

def main():
    claim_reff_balance = input("Claim reff balance? (y/n): ").strip().upper()
    auto_clear_task = input("Auto clear and claim Task? (y/n): ").strip().upper()
    buy_booster = input("Buy booster if available? (y/n): ").strip().upper()
    auto_play_game = input("Auto play game? (y/n): ").strip().upper()

    if auto_play_game == "Y":
        print(Fore.YELLOW + Style.BRIGHT + f"Select Score: ")
        print(Fore.YELLOW + Style.BRIGHT + f"1. Default Score")
        print(Fore.YELLOW + Style.BRIGHT + f"2. Max Score")
        print(Fore.YELLOW + Style.BRIGHT + f"3. Random Score")
        while True:
            try:
                select_score = int(input(Fore.YELLOW + Style.BRIGHT + "Masukan pilihan anda (1/2/3): "))
                if 1 <= select_score <= 3:
                    break
                else:
                    print(Fore.RED + Style.BRIGHT + "Masukan harus antara 1 dan 3.")
            except ValueError:
                print(Fore.RED + Style.BRIGHT + "Masukan harus berupa angka.")
       
    while True:
        try:
            clear_terminal()
            print_welcome_message()
            for line, user_data in user_data_list:
                print(Fore.CYAN + Style.BRIGHT + f"Getting token", end="\r", flush=True)
                time.sleep(1)
                get_token_response = get_token(line, user_data)

                if get_token_response is not None:
                    print(Fore.GREEN + Style.BRIGHT + f"Berhasil mendapatkan token!", end="\r", flush=True)
                    token = get_token_response['data'].get('token')
                    nickname = get_token_response['data']['user'].get('nickname', 'Unknown')
                    print(Fore.CYAN + Style.BRIGHT + f"============= [ Akun {nickname} ] =============", flush=True)

                    time.sleep(2)
                    answer_result = []
                    quizlist = check_quiz(token)
                    if quizlist and quizlist.get('msg', 'Available') == 'Available':
                        for quiz in quizlist.get('data', []):
                            quiz_title = quiz.get('title', 'Unknown')
                            print(Fore.YELLOW + Style.BRIGHT + f"[ Quiz ]: Finding Answer for {quiz_title}")
                            quiz_id = quiz.get('Id', 'Unknown')
                            answer = ''
                            for answer in quiz.get('items', []):
                                if answer.get('is_correct', False):
                                    # example {"quiz_id":20,"selected_item":"B","correct_item":"B"}
                                    print(Fore.GREEN + Style.BRIGHT + f"[ Quiz ]: Answer found : {answer['number']}")
                                    answer_result.append({"quiz_id": quiz_id, "selected_item": answer['number'], "correct_item": answer['number']})
                                    break
                    elif quizlist and quizlist.get('msg', 'Available') == 'Already answered today':
                        print(Fore.YELLOW + Style.BRIGHT + f"[ Quiz ]: Sudah menjawab quiz hari ini")
                    else:
                        print(Fore.RED + Style.BRIGHT + f"[ Quiz ]: Gagal mendapatkan informasi quiz")

                    time.sleep(2)
                    if answer_result:
                        submit_quiz_response = submit_quiz(token, answer_result)
                        if submit_quiz_response and submit_quiz_response.get('msg', 'NOTOK') == 'OK':
                            print(Fore.GREEN + Style.BRIGHT + f"[ Quiz ]: Quiz berhasil dijawab")
                        else:
                            print(Fore.RED + Style.BRIGHT + f"[ Quiz ]: Gagal menjawab quiz")
                    else:
                        print(Fore.YELLOW + Style.BRIGHT + f"[ Quiz ]: Tidak ada quiz yang ditemukan")

                    profil = get_profile(user_data, token)
                    if profil is None or 'data' not in profil:
                        print(Fore.RED + Style.BRIGHT + f"[ Profile ]: Gagal mendapatkan data {nickname}!")
                        time.sleep(5)
                        continue
                    else:
                        balance = profil['data'].get('Balance', 0)
                        invite_count = profil['data'].get('invite_count', 0)
                        balance_view = format_balance(balance)
                        print(Fore.CYAN + Style.BRIGHT + f"[ Balance ]: {balance_view}")
                        print(Fore.CYAN + Style.BRIGHT + f"[ Total Invite ]: {invite_count}")

                    farming_balance = get_farming_reward(user_data, token)
                    if farming_balance is None or 'data' not in farming_balance:
                        print(Fore.RED + Style.BRIGHT + f"[ Farming ]: Gagal mendapatkan data {nickname}!")
                    else:
                        claim_balance = int(format_balance(farming_balance['data']['reward']))  # Convert to integer
                        claim_in = farming_balance.get('data', {}).get('next_claim_timestamp')
                        ts = datetime.now().timestamp() * 1000
                        time_remaining = max(0, claim_in - ts)

                        second = int(time_remaining / 1000)
                        hours, minutes, seconds = convert_ts(second)
                        print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Reward {claim_balance} Point")
                        print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Claim time {hours} Jam {minutes} Menit")

                        if claim_balance > 0 and time_remaining == 0:
                            print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Claiming {claim_balance} Point", end="\r", flush=True)
                            claim_farming = claim_farming_reward(user_data, token)
                            if claim_farming:
                                print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Claimed {claim_balance} Point              ", flush=True)
                                print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Starting Farming..", end="\r", flush=True)
                                start_farming_response = start_farming(user_data, token)
                                if start_farming_response:
                                    print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Farming started!           ", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"[ Farming ]: Failed to start farming!           ", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"[ Farming ]: Gagal claiming")
                        elif claim_balance == 0 and time_remaining == 0:
                            print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Starting Farming..", end="\r", flush=True)
                            start_farming_response = start_farming(user_data, token)
                            if start_farming_response:
                                print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Farming started!           ", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"[ Farming ]: Failed to start farming!           ", flush=True)
                        else:
                            print(Fore.YELLOW + Style.BRIGHT + f"[ Farming ]: Still Farming         ")

                        if claim_reff_balance == 'Y':
                            print(Fore.YELLOW + Style.BRIGHT + f"[ Reff Balance ]: Checking..", end="\r", flush=True)
                            time.sleep(2)
                            cek_reff_balance = get_ref_reward(user_data, token)
                            
                            if cek_reff_balance is None or 'data' not in cek_reff_balance:
                                print(Fore.RED + Style.BRIGHT + f"[ Reff Balance ]: Gagal mendapatkan data {nickname}!", flush=True)
                            else:
                                saldo = cek_reff_balance['data'].get('balance', 0)
                                saldo_view = format_balance(saldo)
                                print(Fore.GREEN + Style.BRIGHT + f"[ Reff Balance ]: Reward {saldo_view} Point          ", flush=True)
                                
                                if int(saldo_view) > 0:
                                    claim_reff = claim_ref_reward(user_data, token)
                                    if claim_reff:
                                        saldo_claim = claim_reff.get('data')
                                        saldo_claim_view = format_balance(saldo_claim)
                                        print(Fore.GREEN + Style.BRIGHT + f"[ Reff Balance ]: Claimed {saldo_claim_view} Point            ", flush=True)
                                    else:
                                        print(Fore.RED + Style.BRIGHT + f"[ Reff Balance ]: Failed to claim reff balance!          ", flush=True)
                        else:
                            print(Fore.YELLOW + Style.BRIGHT + f"[ Reff Balance ]: Skipping Claim Reff Balance", flush=True)

                        if auto_clear_task == "Y":
                            print(Fore.GREEN + Style.BRIGHT + f"[ Task ]: Checking..", end="\r", flush=True)
                            get_task_list = get_task(user_data, token)
                            if get_task_list:
                                task_list = get_task_list.get('data', {})
                                task_normal = task_list.get('Tasks', [])
                                all_tasks_completed = True
                                # task_extra = task_list.get('Extra Tasks', [])
                                for task in task_normal:
                                    if not task['complete']:
                                        all_tasks_completed = False
                                        print(Fore.GREEN  + f"[ Task ]: Finishing task {task['name']}", end="\r" , flush=True)
                                        time.sleep(1)
                                        complete_task_result = complete_task(user_data,task['name'],token)   
                                        if complete_task_result:
                                            result = complete_task_result.get('data', False)
                                            if result:
                                                print(Fore.GREEN + Style.BRIGHT + f"[ Task ]: Claiming task {task['name']}               ", flush=True)
                                                time.sleep(1)
                                                claim_task_result = claim_task(user_data,task['name'],token)
                                                if claim_task_result:
                                                    print(f"{Fore.GREEN+Style.BRIGHT}[ Task ]: Complete and Claimed {task['name']}               " , flush=True)
                                                else:
                                                    print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Failed to claim task {task['name']}                  ", flush=True)
                                            else:
                                                 print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Failed to claim task {task['name']}                  ", flush=True)
                                        else:
                                            print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Failed to finishing {task['name']}            ", flush=True)

                                # Jika semua task sudah selesai
                                if all_tasks_completed:
                                    print(f"{Fore.GREEN+Style.BRIGHT}[ Task ]: All Tasks Completed              ", flush=True)
                                # for extra in task_extra:
                                #     if not extra['complete']:
                                #         print(Fore.GREEN + Style.BRIGHT + f"[ Task ]: Finishing task {extra['name']}", end="\r" , flush=True)
                                #         time.sleep(1)
                                #         complete_task_result = complete_task(user_data,extra['name'],token)   
                                #         if complete_task_result:
                                #             result = complete_task_result.get('data', False)
                                #             if result:
                                #                 print(Fore.GREEN + Style.BRIGHT + f"[ Task ]: Claiming task {extra['name']}               ", flush=True)
                                #                 time.sleep(1)
                                #                 claim_task_result = claim_task(user_data,extra['name'],token)
                                #                 if claim_task_result:
                                #                     print(f"{Fore.GREEN+Style.BRIGHT}[ Task ]: Complete and Claimed {extra['name']}               " , flush=True)
                                #                 else:
                                #                     print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Failed to claim task {extra['name']}                  ", flush=True)
                                #             else:
                                #                  print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Failed to claim task {extra['name']}                  ", flush=True)
                                #         else:
                                #             print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Failed to finishing {extra['name']}            ", flush=True)
                            else:
                                print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Failed Get List Task          ", flush=True)
                        else:
                            print(Fore.YELLOW + Style.BRIGHT + f"[ Task ]: Skipping Auto Clear and Claim Task", flush=True)

                        if buy_booster == 'Y':
                            print(Fore.YELLOW + Style.BRIGHT + f"[ Booster ]: Checking booster status..", end="\r", flush=True)
                            time.sleep(2)
                            booster_status = check_boost_status(token)
                            
                            if booster_status:
                                for booster in booster_status.get('data', []):
                                    if booster['name'] == 'Game Booster' and booster['current_count'] < booster['task_count']:
                                        print(Fore.YELLOW + Style.BRIGHT + f"[ Booster ]: Purchasing Booster..", end="\r", flush=True)
                                        time.sleep(2)
                                        purchase_booster = purchase_boost(token, booster['uid'])
                                        if purchase_booster:
                                            print(Fore.GREEN + Style.BRIGHT + f"[ Booster ]: Booster Purchased!           ", flush=True)
                                        else:
                                            print(Fore.RED + Style.BRIGHT + f"[ Booster ]: Failed to purchase booster!           ", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"[ Booster ]: Failed to check booster status!          ", flush=True)
                        else:
                            print(Fore.YELLOW + Style.BRIGHT + f"[ Booster ]: Skipping Booster Purchase", flush=True)


                        print(Fore.GREEN + Style.BRIGHT + f"[ Game ]: Checking ticket..", end="\r", flush=True)
                        time.sleep(2)
                        tiket_response = check_tiket(token)
                        
                        if tiket_response:
                            total_tiket = tiket_response.get('data', {}).get('game_count')
                            print(Fore.CYAN + Style.BRIGHT + f"[ Game ]: {total_tiket} Ticket            " , flush=True)

                            if auto_play_game == "Y":
                                while total_tiket > 0:
                                    print(Fore.YELLOW + Style.BRIGHT + f"[ Game ]: Playing game..", end="\r", flush=True)
                                    time.sleep(2)
                                    get_game_id = play_game(token)

                                    if get_game_id:
                                        game_id = get_game_id.get('data', {}).get('game_id')
                                        if game_id:
                                            if select_score == 1: # default score
                                                print(Fore.YELLOW + Style.BRIGHT + f"[ Game ]: Default Score Selected       ", flush=True)
                                                rule = tiket_response.get('data', {}).get('rule', [])
                                                big_fire_count, small_fire_count, magnifier_count, bomb_count, total_score = calculate_default_score(rule)
                                                print(f"[ Game ]: You Get {big_fire_count} Big Fire | {small_fire_count} Small Fire | {magnifier_count} Magnifier")
                                                print(f"[ Game ]: You Avoid {bomb_count} bomb")
                                                max_score = total_score
                                            elif select_score == 2: # max score
                                                print(Fore.YELLOW + Style.BRIGHT + f"[ Game ]: Max Score Selected       ", flush=True)
                                                max_score = 100
                                            else: # random score
                                                print(Fore.YELLOW + Style.BRIGHT + f"[ Game ]: Random Score Selected       ", flush=True)
                                                max_score = random.randint(100, 170)
                                            game_result = claim_game(game_id, max_score, token)
                                            
                                            if game_result.get('code') == 200:
                                                 print(Fore.GREEN + Style.BRIGHT + f"[ Game ]: Game Berhasil dimainkan | Score: {max_score} Point     ", flush=True)
                                                #  print(f"[ Game ] Score: {game_result.get('data', {}).get('score')} Point")
                                                 time.sleep(2)
                                            else:
                                                 print(Fore.RED + Style.BRIGHT + f"[ Game ]: Game Gagal dimainkan    ", flush=True)
                                                 time.sleep(2)

                                            cek_sisa_tiket = check_tiket(token)
                                            total_tiket = cek_sisa_tiket.get('data', {}).get('game_count')  # Update total_tiket
                                            if total_tiket > 0:
                                                 print(Fore.CYAN + Style.BRIGHT + f"[ Game ]: Masih ada {total_tiket} Ticket      " , flush=True)
                                                 print(Fore.CYAN + Style.BRIGHT + f"[ Game ]: Memainkan Game Ulang" , end="\r", flush=True)
                                                 time.sleep(2)
                                                 continue
                                            else:
                                                 print(Fore.CYAN + Style.BRIGHT + f"[ Game ]: Tidak ada lagi Ticket        " , flush=True)
                                                 break
                                    else:
                                        print(Fore.RED + Style.BRIGHT + f"[ Game ]: Failed to play game            ", flush=True)
                            else:
                                print(Fore.YELLOW + Style.BRIGHT + f"[ Game ]: Skipping Auto Play Game", flush=True)
                        else:
                            print(f"{Fore.RED+Style.BRIGHT}[ Game ]: Failed Get Tiket            ", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"Gagal login ke akun {get_token_response}")
                    time.sleep(2)
                    continue

            print(Fore.BLUE + Style.BRIGHT + f"\n==========SEMUA AKUN TELAH DIPROSES==========\n", flush=True)
            animated_loading(300)
        except Exception as e:
            time.sleep(5)
            print(f"An error occurred: {str(e)}")

def print_welcome_message():
    print(Fore.RED + Style.BRIGHT + "█▀▀ " + Fore.YELLOW + "█░█ " + Fore.RED + "▄▀█ " + Fore.YELLOW + "█░░ " + Fore.RED + "█ " + Fore.YELLOW + "█▄▄ " + Fore.RED + "█ " + Fore.YELLOW + "█▀▀")
    print(Fore.YELLOW + "█▄█ " + Fore.RED + "█▀█ " + Fore.YELLOW + "█▀█ " + Fore.RED + "█▄▄ " + Fore.YELLOW + "█ " + Fore.RED + "█▄█ " + Fore.YELLOW + "█ " + Fore.RED + "██▄")
    print(Fore.CYAN + Style.BRIGHT + "\nMatchQuest BOT")
    print(Fore.CYAN + Style.BRIGHT + "Update Link: https://github.com/adearmanwijaya/")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.YELLOW + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA / BINANCE ID 248613229")
    print(Fore.YELLOW + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")

if __name__ == "__main__":
    main()
