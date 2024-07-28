import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime, timedelta, timezone

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "PinkTrade BOT")
    print(Fore.CYAN + Style.BRIGHT + "Update Link: https://github.com/adearman/pinktrade")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA / BINANCE ID 248613229")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")
 


headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://bot.pinktrade.fi',
    'Pragma': 'no-cache',
    'Referer': 'https://bot.pinktrade.fi/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AG Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.165 Mobile'
}


def cek_balance(ghalibie):
    url = 'https://bot-api.pinktrade.fi/pinktrade/api/v1/airdrop'
    headers['Authorization'] = ghalibie
    for attempt in range(3):
        response = requests.get(url, headers=headers)
        # print(response.json())
        if response.status_code == 200:
            return response.json()
    return None

def claim_balance(ghalibie):
    url = 'https://bot-api.pinktrade.fi/pinktrade/api/v1/airdrop/claim-mint-reward'
    headers['Authorization'] = ghalibie
    for attempt in range(3):
        response = requests.post(url, headers=headers)
        # print(response.json())
        if response.status_code == 200:
            return response.json()
    return None
def upgrade_astronaut(ghalibie,level):
    url = f'https://bot-api.pinktrade.fi/pinktrade/api/v1/airdrop/upgrade-option?type=astronaut&level={level}'
    headers['Authorization'] = ghalibie
    for attempt in range(3):
        response = requests.get(url, headers=headers)
        # print(response.json())
        if response.status_code == 200:
            return response.json()
    return None

def get_tasks(ghalibie):
    url = 'https://bot-api.pinktrade.fi/pinktrade/api/v1/airdrop/tasks?type=TASK2'
    headers['Authorization'] = ghalibie
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []


def claim_task(ghalibie, task_id):
    url = f'https://bot-api.pinktrade.fi/pinktrade/api/v1/airdrop/claim-task?task_id={task_id}'
    headers['Authorization'] = ghalibie
    response = requests.post(url, headers=headers)
    return response

def clear_tasks(ghalibie):
    tasks = get_tasks(ghalibie)
    for task in tasks:
        if task['title'] not in ["Invite 5 friends", "Invite 20 friends", "Invite 100 friends", "Invite 1000 friends", "Add $PINK to your Telegram name"]:
            print(Fore.YELLOW + Style.BRIGHT + f"Task     :  Clearing {task['title']}", end="\r", flush=True)
            response = claim_task(ghalibie, task['id'])
            if response.status_code == 201:
                print(Fore.GREEN + Style.BRIGHT + f"Task     : {task['title']} Done!         ", flush=True)
            elif response.status_code == 400:
                print(Fore.RED + Style.BRIGHT + f"Task     : {task['title']} Already Done        ", flush=True)

def join_squad(ghalibie, squad_id=73):
    url = f'https://bot-api.pinktrade.fi/pinktrade/api/v1/airdrop/join-squad-pool?squad_id={squad_id}'
    headers['Authorization'] = ghalibie
    response = requests.get(url, headers=headers)
    return response

def main():
    ghalibie_upgrade = input("Auto upgrade astronaut? (y/n): ").strip().lower()
    max_level = 0  # Initialize max_level
    if ghalibie_upgrade == 'y':
        max_level = int(input("Max level astronaut: "))
    auto_clear_task = input("Auto clear task? (y/n): ").strip().lower()
    print_welcome_message()
    while True:
        try:
            with open('query.txt', 'r') as file:
                queries = file.readlines()
            for index, query_data in enumerate(queries, start=1):
                query_data = query_data.strip()
                print(Fore.YELLOW + Style.BRIGHT + f"Checking account {index}", end="\r", flush=True)
                ghalibie = cek_balance(query_data)
                # print(ghalibie)
                if ghalibie is not None:
                    totalearn = ghalibie['totalEarn']
                    totalreff = ghalibie['totalRef']
                    nextclaim = int(ghalibie['nextClaimTime'])  
                    astrolevel = ghalibie['astronauntSize']['level']
                    astrotoken = ghalibie['astronauntSize']['maxToken']
                    spaceshiplevel = ghalibie['spaceshipSize']['level']
                    spaceshiptime = ghalibie['spaceshipSize']['maxTime']
                    username = ghalibie.get('username', 'no username')
                    
                    # Check for squadPool
                    squad_pool = ghalibie.get('squadPool', None)
                    if squad_pool:
                        squad_title = squad_pool['title']
                        squad_total_earn = squad_pool['totalEarn']
                        totalUser = squad_pool['totalUser']
                    else:
                        print(Fore.YELLOW + Style.BRIGHT + "No Squad found, joining squad...", flush=True)
                        join_response = join_squad(query_data)
                        if join_response.status_code == 200:
                            print(Fore.GREEN + Style.BRIGHT + "Successfully joined squad!", flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT + "Failed to join squad.", flush=True)
                        squad_title = "No Squad"
                        totalUser = "0"
                        squad_total_earn = "N/A"

                    current_time = int(time.time())
                    remaining_time = nextclaim - current_time
                    
                    # Convert nextclaim timestamp to hours, minutes, and seconds
                    if remaining_time > 0:
                        nextclaim_hours = remaining_time // 3600
                        nextclaim_minutes = (remaining_time % 3600) // 60
                        nextclaim_seconds = remaining_time % 60
                        nextclaim_formatted = f"{nextclaim_hours} Jam {nextclaim_minutes} Menit {nextclaim_seconds} Detik"
                    else:
                        nextclaim_formatted = "Need Claim"

                    print(Fore.CYAN + Style.BRIGHT + f"=== Akun ke {index} | {username} ===             ", flush=True)
                    if auto_clear_task == 'y':
                        clear_tasks(query_data)
               
                    print(Fore.CYAN + Style.BRIGHT + f"Squad           : {Fore.MAGENTA+Style.BRIGHT}{squad_title} {Fore.CYAN+Style.BRIGHT}| {totalUser} Member | Total Earn: {squad_total_earn}", flush=True)
                    print(Fore.YELLOW + Style.BRIGHT + f"Balance         : {int(totalearn):,}".replace(',', '.'), flush=True)
                    print(Fore.YELLOW + Style.BRIGHT + f"Referral        : {int(totalreff):,} | Invited {ghalibie['inviteCnt']}", flush=True)
                    print(Fore.GREEN + Style.BRIGHT + f"Astronaut       : {astrotoken} $PINK / hour | Level {astrolevel}", flush=True)
                    print(Fore.GREEN + Style.BRIGHT + f"Spaceship       : Claim Every {spaceshiptime} hour | Level {spaceshiplevel}", flush=True)
                    if nextclaim_formatted == 'Need Claim':
                        print(Fore.GREEN + Style.BRIGHT + f"Claim           : Claiming...", end="\r", flush=True)
                        claim_balance(query_data)
                        print(Fore.GREEN + Style.BRIGHT + f"Claim           : Claimed!        ", end="\r", flush=True)
                    else:
                        print(Fore.GREEN + Style.BRIGHT + f"Claim           : {nextclaim_formatted}", flush=True)
                    
                    if ghalibie_upgrade == 'y':
                        print(Fore.GREEN + Style.BRIGHT + f"Astronaut       : Upgrading...", end="\r", flush=True)
                        while astrolevel < max_level:
                            upgrade_level = astrolevel + 1
                            upgrade_cek = upgrade_astronaut(query_data, upgrade_level)
                            if upgrade_cek is not None:
                                astrolevel = upgrade_level  # Update the current level
                                print(Fore.GREEN + Style.BRIGHT + f"Astronaut       : Upgraded to Level {upgrade_level}", end="\r", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"Astronaut       : Failed to upgrade               ", flush=True)
                                break
                        print(Fore.YELLOW + Style.BRIGHT + f"Astronaut       : Already At Level {astrolevel}", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"Invalid Query. Account {index} Gagal", flush=True)

                    
            print(Fore.GREEN + Style.BRIGHT + f"\n==========SEMUA AKUN TELAH DI PROSES==========\n",  flush=True)    
            animated_loading(1800)   
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(5)
def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rMenunggu waktu claim berikutnya {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    print("\rMenunggu waktu claim berikutnya selesai.                            ", flush=True)     
if __name__ == "__main__":
    main()

