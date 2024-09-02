import requests
import json
import time
import random
import base64
from requests_html import HTMLSession
from colorama import init, Fore

# ===================================================================
# ===================================================================
# Configuration for BOT
file_akun = 'initdata.txt'
url_kombo = 'https://raw.githubusercontent.com/unadavina/hk/main/combo'
auto_cek_task_list = "n"
auto_absen = "y"
auto_morse = "y"
auto_klaim_kombo = "n"
auto_balap_sepeda = "n"
auto_game_clone = "n"
auto_game_cube = "n"
auto_game_train = "n"
max_harga_kartu = 5000000
auto_minigame = "y"
auto_upgrade_multitap = "n" # Adjust lv_upgrade_multitap if auto_upgrade_multitap = Y
lv_upgrade_multitap = 9
auto_upgrade_energy = "n" # Adjust lv_upgrade_energy if auto_upgrade_energy = Y
lv_upgrade_energy = 9
auto_upgrade_pph = "n"
harga_maksimal = 10000000
tunggu_cooldown = "y"
max_tunggu_cooldown = 300 # In seconds
jeda_antar_akun = "n"
max_jeda_antar_akun = 15 # In seconds
# ===================================================================
# Do not edit the script below
# ===================================================================

session = HTMLSession()

# Initialize colorama
init(autoreset=True)

def DailyCipherDecode(cipher):
    cipher = cipher[:3] + cipher[4:]
    cipher = cipher.encode("ascii")
    cipher = base64.b64decode(cipher)
    cipher = cipher.decode("ascii")
    return cipher

def TextToMorseCode(text):
    morse_code = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
        "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
        "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.", " ": "/", ".": ".-.-.-", ",": "--..--",
        "?": "..--..", "'": ".----.", "!": "-.-.--", "/": "-..-.", "(": "-.--.",
        ")": "-.--.-", "&": ".-...", ":": "---...", ";": "-.-.-.", "=": "-...-",
        "+": ".-.-.", "-": "-....-", "_": "..--.-", '"': ".-..-.", "$": "...-..-",
        "@": ".--.-."
    }
    text = text.upper()
    morse = ""
    for char in text:
        if char in morse_code:
            morse += morse_code[char] + " "
    return morse

def countdown(t):
    while t:
        menit, detik = divmod(t, 60)
        menit = str(menit).zfill(2)
        detik = str(detik).zfill(2)
        print(Fore.LIGHTCYAN_EX + f"-------------->     Tunggu dulu {menit}:{detik} detik", flush=True, end="\r")
        time.sleep(1)
        t -= 1
    print("                                        ", flush=True, end="\r") 

def separator(data):
    return '{:,}'.format(int(data))

def load_tokens(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

def get_headers(token: str) -> dict:
    return {
        'Accept': '*/*',
        'Authorization': f'Bearer {token}',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'User-Agent': 'Mozilla/5.0'
    }

def get_token(init_data_raw):
    url = 'https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    res = session.post(url, headers=headers, data=data)
    if res.status_code == 200:
        return res.json()['authToken']
    else:
        print(Fore.LIGHTRED_EX + "\rFailed Get Token. Invalid init data", flush=True)
        return None

def authenticate(token):
    url = 'https://api.hamsterkombatgame.io/auth/me-telegram'
    headers = get_headers(token)
    response = session.post(url, headers=headers)
    return response

def sync_clicker(token):
    url = 'https://api.hamsterkombatgame.io/clicker/sync'
    headers = get_headers(token)
    headers['Content-Type'] = 'application/json'
    response = session.post(url, headers=headers)
    return response

def claim_daily(token):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers = get_headers(token)
    headers['Content-Type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = session.post(url, headers=headers, data=data)
    return response

def upgrade(token, upgrade_type):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['Content-Type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data)
    return response

def tap(token, max_taps, available_taps):
    url = 'https://api.hamsterkombatgame.io/clicker/tap'
    headers = get_headers(token)
    headers['Content-Type'] = 'application/json'
    data = json.dumps({"count": max_taps, "availableTaps": available_taps, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data)
    return response

def list_tasks(token):
    url = 'https://api.hamsterkombatgame.io/clicker/list-tasks'
    headers = get_headers(token)
    headers['Content-Type'] = 'application/json'
    response = session.post(url, headers=headers)
    return response

def get_promos(token):
    url = 'https://api.hamsterkombatgame.io/clicker/get-promos'
    headers = get_headers(token)
    headers['Content-Type'] = 'application/json'
    response = session.post(url, headers=headers)
    return response

def njaluk_kombo(item):
    url = url_kombo
    njaluk = requests.get(url)
    KomboSaiki = njaluk.text
    ListKombo = KomboSaiki.split()
    if item == "item":
        List_Kombo = [ListKombo[0], ListKombo[1], ListKombo[2]]
    else:
        List_Kombo = ListKombo[4]
    return List_Kombo

def start_minigame(token):
    url = 'https://api.hamsterkombatgame.io/clicker/start-keys-minigame'
    headers = get_headers(token)
    response = session.post(url, headers=headers)
    return response

def klaim_MiniGame(token, jeda, iduser):
    prefix_acak = '0' + str(jeda) + str(random.randint(10000000000, 99999999999))[:10]
    cipher = f'{prefix_acak}|{iduser}'
    base64_cipher = base64.b64encode(cipher.encode()).decode()
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame'
    headers = get_headers(token)
    headers['Content-Type'] = 'application/json'
    data = json.dumps({"cipher": base64_cipher})
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response
    else:
        print(Fore.LIGHTRED_EX + f"Gagal claim MiniGame, status code: {response.status_code}", flush=True)
        return None

def njaluk_ip(token):
    url = 'https://api.hamsterkombatgame.io/ip'
    headers = get_headers(token)
    response = session.post(url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        print(Fore.LIGHTRED_EX + f"Gagal claim IP, status code: {response.status_code}", flush=True)
        return None

def GetAccountConfigRequest(token):
    url = 'https://api.hamsterkombatgame.io/clicker/get-account-config'
    headers = get_headers(token)
    headers['Content-Type'] = 'application/json'
    response = session.post(url, headers=headers)
    return response

def PerformActions(token, mode=""):
    if auto_cek_task_list.lower() == "y":
        response = list_tasks(token)
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                print(f"Task ID: {task['id']}, Status: {task['status']}")
        else:
            print(Fore.LIGHTRED_EX + f"Gagal mendapatkan daftar tugas, status code: {response.status_code}", flush=True)

    if auto_absen.lower() == "y":
        response = claim_daily(token)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Klaim daily berhasil", flush=True)
        else:
            print(Fore.LIGHTRED_EX + f"Gagal klaim daily, status code: {response.status_code}", flush=True)

    if auto_morse.lower() == "y":
        print(Fore.LIGHTCYAN_EX + "----- MULAI KODE MORSE -----", flush=True)
        morse_code = TextToMorseCode("HELLO WORLD")
        print(Fore.LIGHTCYAN_EX + morse_code)

    if auto_klaim_kombo.lower() == "y":
        list_kombo = njaluk_kombo("item")
        for kombo in list_kombo:
            print(Fore.LIGHTCYAN_EX + f"Klaim kombo: {kombo}")

    if auto_balap_sepeda.lower() == "y":
        # Implement the balap sepeda logic here
        pass

    if auto_game_clone.lower() == "y":
        # Implement the game clone logic here
        pass

    if auto_game_cube.lower() == "y":
        # Implement the game cube logic here
        pass

    if auto_game_train.lower() == "y":
        # Implement the game train logic here
        pass

    if auto_minigame.lower() == "y":
        response = start_minigame(token)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "MiniGame started", flush=True)
        else:
            print(Fore.LIGHTRED_EX + f"Gagal memulai MiniGame, status code: {response.status_code}", flush=True)
    
    if auto_upgrade_multitap.lower() == "y":
        response = upgrade(token, "multitap")
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Upgrade multitap berhasil", flush=True)
        else:
            print(Fore.LIGHTRED_EX + f"Gagal upgrade multitap, status code: {response.status_code}", flush=True)

    if auto_upgrade_energy.lower() == "y":
        response = upgrade(token, "energy")
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Upgrade energy berhasil", flush=True)
        else:
            print(Fore.LIGHTRED_EX + f"Gagal upgrade energy, status code: {response.status_code}", flush=True)

    if auto_upgrade_pph.lower() == "y":
        response = upgrade(token, "pph")
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Upgrade pph berhasil", flush=True)
        else:
            print(Fore.LIGHTRED_EX + f"Gagal upgrade pph, status code: {response.status_code}", flush=True)

def main():
    tokens = load_tokens(file_akun)
    if tokens:
        for token in tokens:
            auth_response = authenticate(token)
            if auth_response.status_code == 200:
                token = auth_response.json()['authToken']
                PerformActions(token)
                if auto_minigame.lower() == "y":
                    response = klaim_MiniGame(token, 10, 1)
                    if response:
                        print(Fore.LIGHTGREEN_EX + "Klaim MiniGame berhasil")
                    else:
                        print(Fore.LIGHTRED_EX + "Gagal klaim MiniGame")
                if auto_klaim_kombo.lower() == "y":
                    response = njaluk_ip(token)
                    if response:
                        print(Fore.LIGHTGREEN_EX + "IP klaim berhasil")
                    else:
                        print(Fore.LIGHTRED_EX + "Gagal klaim IP")
            else:
                print(Fore.LIGHTRED_EX + f"Authentication failed for token, status code: {auth_response.status_code}", flush=True)

if __name__ == "__main__":
    main()
