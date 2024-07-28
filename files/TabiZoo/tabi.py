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
    print(Fore.GREEN + Style.BRIGHT + "TABI BOT")
    print(Fore.CYAN + Style.BRIGHT + "Update Link: https://github.com/adearman/tabizoo")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA / BINANCE ID 248613229")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")
 


headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Content-Type': 'application/json',
    'Origin': 'https://app.tabibot.com',
    'Pragma': 'no-cache',
    'Referer': 'https://app.tabibot.com/?tgWebAppStartParam=2Uaidk',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}


def login_tabi(ghalibie):
    url = 'https://app.tabibot.com/api/user/sign-in'
    headers['rawdata'] = ghalibie
    for attempt in range(3):
        response = requests.post(url, headers=headers)
        print(response)
        if response.status_code == 200:
            return response.json()
       
    return None

def cekin_tabi(ghalibie):
    url = 'https://app.tabibot.com/api/user/check-in'
    headers['rawdata'] = ghalibie
    for attempt in range(3):
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    return None


def cek_mining(ghalibie):
    url = 'https://app.tabibot.com/api/mining/info'
    headers['rawdata'] = ghalibie
    for attempt in range(3):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    return None

def claim_mining(ghalibie):
    url = 'https://app.tabibot.com/api/mining/claim'
    headers['rawdata'] = ghalibie
    for attempt in range(3):
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    return None

def upgrade_mining(ghalibie):
    url = 'https://app.tabibot.com/api/user/level-up'
    headers['rawdata'] = ghalibie
    for attempt in range(3):
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    return None
def main():
    ghalibie_upgrade = input("Auto upgrade minning? (y/n): ").strip().upper()
    while True:
        print_welcome_message()
        try:

            with open('query.txt', 'r') as file:
                queries = file.readlines()
            for index, query_data in enumerate(queries, start=1):
                query_data = query_data.strip()
                print(Fore.YELLOW + Style.BRIGHT + f"Try to login akun {index}", end="\r", flush=True)
                ghalibie = login_tabi(query_data)
                print(ghalibie)
                level = ghalibie.get('user', {}).get('level')
                if ghalibie:
                    print(Fore.CYAN + Style.BRIGHT + f"=== [ Akun ke {index} | {ghalibie['user']['name']} ] ===             ", flush=True)
                    print(Fore.YELLOW + Style.BRIGHT + f"[ Coins ] : {int(ghalibie['user']['coins']):,}".replace(',', '.'), flush=True)
                    print(Fore.YELLOW + Style.BRIGHT + f"[ Level ] : {ghalibie['user']['level']}", flush=True)
                    print(Fore.BLUE + Style.BRIGHT + f"[ Invites ] :  {ghalibie['user']['invites']}", flush=True)
                    cekin = ghalibie['user']['hasCheckedIn']
                    if cekin == True:
                        print(Fore.GREEN + Style.BRIGHT + f"[ Check In ] : Already Checkin | Streak {ghalibie['user']['streak']}", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"[ Check In ] : Trying to checkin...", end="\r", flush=True)
                        time.sleep(2)
                        ghalibie_cekin = cekin_tabi(query_data)
                        if ghalibie_cekin:
                            print(Fore.GREEN + Style.BRIGHT + f"[ Check In ] : Success | Streak {ghalibie['user']['streak']}", flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT + f"[ Check In ] : Failed {ghalibie_cekin}                      ", flush=True)
                    print(Fore.RED + Style.BRIGHT + f"[ Mining ] : Trying to check...", end="\r", flush=True)
                    time.sleep(2)
                    mining = cek_mining(query_data)
                    if mining:
                        rate = mining['rate']
                        refrate = mining['referralRate']
                        next = mining['nextClaimTimeInSecond']
                        print(Fore.GREEN + Style.BRIGHT + f"[ Mining ] : Rate: {rate} / hour | Referral Rate: {refrate} / hour", flush=True)
                        if next > 0:
                            hours, remainder = divmod(next, 3600)
                            minutes, seconds = divmod(remainder, 60)
                            print(Fore.RED + Style.BRIGHT + f"[ Mining ] : Next Claim in {int(hours)} jam {int(minutes)} menit {int(seconds)} second", flush=True)
                        elif next == 0 or next <= 0:
                            print(Fore.GREEN + Style.BRIGHT + f"[ Mining ] : Trying to claim...", end="\r" , flush=True)
                            claim_ghalibie = claim_mining(query_data)
                            if claim_ghalibie == True:
                                print(Fore.GREEN + Style.BRIGHT + f"[ Mining ] : Success                ", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"[ Mining ] : Failed", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"[ Mining ] : Failed to get any info", flush=True)
                   
                    
                    if ghalibie_upgrade == 'Y':
                        print(Fore.YELLOW + Style.BRIGHT + f"[ Upgrade ] : Trying to upgrade...", end="\r", flush=True)
                        time.sleep(2)
                        upgrade = upgrade_mining(query_data)
                  
                        if upgrade:
                            after_level = upgrade['level']
                            before_level = level
                            if after_level > before_level:
                                print(Fore.GREEN + Style.BRIGHT + f"[ Upgrade ] : Success                  ", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"[ Upgrade ] : Failed                  ", flush=True)

                else:
                    print(Fore.RED + Style.BRIGHT + f"Akun ke {index} Query Salah", flush=True)
                
        
            print(Fore.BLUE + Style.BRIGHT + f"\n==========SEMUA AKUN TELAH DI PROSES==========\n",  flush=True)    
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


