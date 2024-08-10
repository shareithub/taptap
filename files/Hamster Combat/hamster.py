import requests
import json
import time
import random
import base64
import os
import glob
import string
import asyncio
import aiohttp
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style
from fake_useragent import UserAgent
from requests_html import HTMLSession
#===========================================================================
#===========================================================================
#konfigurasi BOT
file_akun = 'initdata.txt'
file_vc_balapan = 'voucher_hamster_bike1.txt'
file_vc_clone = 'voucher_hamster_bike1.txt'
file_vc_cube = 'voucher_hamster_bike1.txt'
file_vc_train = 'voucher_hamster_bike1.txt'
url_kombo = 'https://raw.githubusercontent.com/unadavina/hk/main/combo'
# Silahkan Edit dengan Y atau N. kalau Y berarti aktif, kalo n berarti off
# Sesuaikan juga var2 lain sesuai keinginanmu
# Setelah melakukan perubahan, jangan lupa bot.py ditutup dan dibuka kembali
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
auto_upgrade_multitap = "n" # Jika auto_upgrade_multitap = Y, sesuaikan lv_upgrade_multitap
lv_upgrade_multitap = 9
auto_upgrade_energy = "n" # Jika auto_upgrade_energy = Y, sesuaikan lv_upgrade_energy
lv_upgrade_energy = 9
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
auto_upgrade_pph = "n" # Jika auto_upgrade_pph = Y, lv_upgrade_multitap
harga_maksimal = 10000000
tunggu_cooldown = "y" # Tunggu cooldown kartu terbaik. jika Y sesuaikan max_tunggu_cooldown
max_tunggu_cooldown = 300 #dalam detik
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
jeda_antar_akun = "n" # Jika jeda_antar_akun = Y, sesuaikan max_jeda_antar_akun
max_jeda_antar_akun = 15 #dalam detik
#===========================================================================
# Jangan Edit2 script dibawah ini, kalau mau edit2 yang diatas
#=========================================================================== 
session = HTMLSession()
ua = UserAgent()
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
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        " ": "/",
        ".": ".-.-.-",
        ",": "--..--",
        "?": "..--..",
        "'": ".----.",
        "!": "-.-.--",
        "/": "-..-.",
        "(": "-.--.",
        ")": "-.--.-",
        "&": ".-...",
        ":": "---...",
        ";": "-.-.-.",
        "=": "-...-",
        "+": ".-.-.",
        "-": "-....-",
        "_": "..--.-",
        '"': ".-..-.",
        "$": "...-..-",
        "@": ".--.-.",
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
    separasi = '{:,}'.format(int(data))
    return separasi	
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
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': ua.random
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
        'User-Agent': ua.random,
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    res = session.post(url, headers=headers, data=data)
    if res.status_code == 200:
        return res.json()['authToken']
    else:
        error_data = res.json()
        if "invalid" in error_data.get("error_code", "").lower():
            print(Fore.LIGHTRED_EX + "\rFailed Get Token. Invalid init data", flush=True)
        else:
            print(Fore.LIGHTRED_EX + f"\rFailed Get Token. {error_data}", flush=True)
        return None
def authenticate(token):
    url = 'https://api.hamsterkombatgame.io/auth/me-telegram'
    headers = get_headers(token)
    response = session.post(url, headers=headers)
    return response
def sync_clicker(token):
    url = 'https://api.hamsterkombatgame.io/clicker/sync'
    headers = get_headers(token)
    headers['content-type'] = 'application/json;charset=utf-8'
    response = session.post(url, headers=headers)
    return response
def claim_daily(token):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = session.post(url, headers=headers, data=data)
    return response
def upgrade(token, upgrade_type):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data)
    return response
def tap(token, max_taps, available_taps):
    url = 'https://api.hamsterkombatgame.io/clicker/tap'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"count": max_taps, "availableTaps": available_taps, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data)
    return response
def list_tasks(token):
    url = 'https://api.hamsterkombatgame.io/clicker/list-tasks'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json;charset=utf-8'
    response = session.post(url, headers=headers)
    return response
def get_promos(token):
    url = 'https://api.hamsterkombatgame.io/clicker/get-promos'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json;charset=utf-8'
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
#print(f"List Kombo	: {njaluk_kombo("item")}")
#time.sleep(3000)
def start_minigame(token):
    url = 'https://api.hamsterkombatgame.io/clicker/start-keys-minigame'
    headers = get_headers(token)
    response = session.post(url, headers=headers)
    return response
def klaim_MiniGame(token,jeda,iduser):
	prefix_acak = '0' + str(jeda) + str(random.randint(10000000000, 99999999999))[:10]
	cipher = f'{prefix_acak}|{iduser}'
	base64_cipher = base64.b64encode(cipher.encode()).decode()
	url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame'
	headers = get_headers(token)
	headers['accept'] = 'application/json'
	headers['content-type'] = 'application/json'
	data = json.dumps({"cipher": base64_cipher})
	response = session.post(url, headers=headers, data=data)
    # Tambahkan pengecekan status code dan konten respons
	if response.status_code == 200:
		try:
			# Coba parse JSON dan lanjutkan proses
			return response
		except json.JSONDecodeError:
			print(Fore.LIGHTRED_EX + "Gagal mengurai JSON dari respons.", flush=True)
			return None
	elif response.status_code == 400:
		try:
			# Coba parse JSON dan lanjutkan proses
			return response
		except json.JSONDecodeError:
			print(Fore.LIGHTRED_EX + "Gagal mengurai JSON dari respons.", flush=True)
			return None
	elif response.status_code == 500:
		print(Fore.LIGHTRED_EX + f"Gagal claim MiniGame, Internal Server Error", flush=True)
		return response
	else:
		print(Fore.LIGHTRED_EX + f"Gagal claim MiniGame, status code: {response.status_code}", flush=True)
		return None
def njaluk_ip(token):
	url = 'https://api.hamsterkombatgame.io/ip'
	headers = get_headers(token)
#	headers['Access-Control-Request-Headers'] = 'authorization'
#	headers['Access-Control-Request-Method'] = 'GET'
	response = session.post(url, headers=headers)
    # Tambahkan pengecekan status code dan konten respons
	if response.status_code == 200:
		try:
			# Coba parse JSON dan lanjutkan proses
			return response
		except json.JSONDecodeError:
			print(Fore.LIGHTRED_EX + "Gagal mengurai JSON dari respons.", flush=True)
			return None
	elif response.status_code == 400:
		try:
			# Coba parse JSON dan lanjutkan proses
			return response
		except json.JSONDecodeError:
			print(Fore.LIGHTRED_EX + "Gagal mengurai JSON dari respons.", flush=True)
			return None
	elif response.status_code == 500:
		print(Fore.LIGHTRED_EX + f"Gagal claim MiniGame, Internal Server Error", flush=True)
		return response
	else:
		print(Fore.LIGHTRED_EX + f"Gagal claim MiniGame, status code: {response.status_code}", flush=True)
		return None
def GetAccountConfigRequest(token):
    url = 'https://api.hamsterkombatgame.io/clicker/config'
    headers = get_headers(token)
    headers['content-type'] = 'application/json;charset=utf-8'
    response = session.post(url, headers=headers)
    return response
def exchange(token):
    url = 'https://api.hamsterkombatgame.io/clicker/select-exchange'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json;charset=utf-8'
    data = json.dumps({"exchangeId": 'binance'})
    response = session.post(url, headers=headers, data=data)
    return response


def gass_balapan(token,pocer):
    url = 'https://api.hamsterkombatgame.io/clicker/apply-promo'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"promoCode": pocer})
    response = session.post(url, headers=headers, data=data)
    return response
def claim_cipher(token, MorseHarian):
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-cipher'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"cipher": MorseHarian})
    response = session.post(url, headers=headers, data=data)
    # Tambahkan pengecekan status code dan konten respons
    if response.status_code == 200:
        try:
            # Coba parse JSON dan lanjutkan proses
            return response
        except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "Gagal mengurai JSON dari respons.", flush=True)
            return None
    elif response.status_code == 400:
        try:
            # Coba parse JSON dan lanjutkan proses
            return response
        except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "Gagal mengurai JSON dari respons.", flush=True)
            return None
    elif response.status_code == 500:
        print(Fore.LIGHTRED_EX + f"Gagal claim cipher, Internal Server Error", flush=True)
        return response
    else:
        print(Fore.LIGHTRED_EX + f"Gagal claim cipher, status code: {response.status_code}", flush=True)
        return None
def check_task(token, task_id):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    response = session.post(url, headers=headers, data=data)
    return response
def cek_booster(token):
    url = 'https://api.hamsterkombatgame.io/clicker/boosts-for-buy'
    headers = get_headers(token)
    response = session.post(url, headers=headers)
    return response
def use_booster(token,idboost):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": idboost, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data)
    return response
def read_upgrade_list(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]
def get_available_upgrades(token):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    headers['content-type'] = 'application/json;charset=utf-8'
    response = session.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            # print(Fore.LIGHTGREEN_EX + f"\r[ uPGRADE	] : Berhasil mendapatkan list upgrade.", flush=True)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "\r[ uPGRADE	] : Gagal mendapatkan response JSON.", flush=True)
            return []
    else:
        print(Fore.LIGHTRED_EX + f"\r[ uPGRADE	] : Gagal mendapatkan daftar upgrade: Status {response.status_code}", flush=True)
        return []
def buy_upgrade(token, upgrade_id, upgrade_name):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-upgrade'
    headers = get_headers(token)
    headers['content-type'] = 'application/json;charset=utf-8'
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    time.sleep(3)
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.LIGHTGREEN_EX + f"\r[ uPGRADE	] : Berhasil diupgrade...", flush=True)
        except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "\r[ uPGRADE	] : Gagal mengurai JSON saat upgrade.", flush=True)
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                return 'insufficient_funds'
            elif error_response.get('error_code') == 'UPGRADE_COOLDOWN':
                cooldown_seconds = error_response.get('cooldownSeconds', 0)
                menit, detik = divmod(cooldown_seconds, 60)
                jam, menit = divmod(menit, 60)
                jam = str(jam).zfill(2)
                menit = str(menit).zfill(2)
                detik = str(detik).zfill(2)
                print(Fore.BLUE + f"\r[ uPGRADE	] : {upgrade_name} COOLDOWN: {jam} Jam {menit} Menit {detik} Detik.", flush=True)
                return {'cooldown': True, 'cooldown_seconds': cooldown_seconds}
            else:
                print(Fore.LIGHTRED_EX + f"\r[ uPGRADE	] : Failed upgrade {upgrade_name}: {error_response}", flush=True)
                return {'error': True, 'message': error_response}
        except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + f"\r[ uPGRADE	] : Gagal mendapatkan respons JSON. Status: {response.status_code}", flush=True)
            return {'error': True, 'status_code': response.status_code}
def get_available_upgrades_combo(token):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    headers['content-type'] = 'application/json;charset=utf-8'
    response = session.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            print(Fore.LIGHTGREEN_EX + f"\r[ kOMBO hARIAN	] : Berhasil mendapatkan list upgrade.", flush=True)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "\r[ kOMBO hARIAN	] : Gagal mendapatkan response JSON.", flush=True)
            return []
    else:
        print(Fore.LIGHTRED_EX + f"\r[ kOMBO hARIAN	] : Gagal mendapatkan daftar upgrade: Status {response.status_code}", flush=True)
        return []
def buy_upgrade_combo(token, upgrade_id):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-upgrade'
    headers = get_headers(token)
    headers['content-type'] = 'application/json;charset=utf-8'
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.LIGHTGREEN_EX + f"\r[ kOMBO hARIAN	] : Kombo {upgrade_id} berhasil dibeli.", flush=True)
        except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "\r[ kOMBO hARIAN	] : Gagal mengurai JSON saat upgrade.", flush=True)
        return response
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.LIGHTRED_EX + f"\r[ kOMBO hARIAN	] : Koin ora cukup.", flush=True)
                return 'insufficient_funds'
            else:
                # print(f"error saat beli combo: {error_response}")
                # print(Fore.LIGHTRED_EX + f"\r[ kOMBO hARIAN	] : Error: {error_response.get('error_message', 'No error message provided')}", flush=True)
                return error_response
        except json.JSONDecodeError:
            print(Fore.LIGHTRED_EX + f"\r[ kOMBO hARIAN	] : Gagal mendapatkan respons JSON. Status: {response.status_code}", flush=True)
            return None
def auto_upgrade_pph_earn(token, harga_maksimal):
    #upgrade_list = read_upgrade_list('upgrade_list.txt')
    data = get_available_upgrades(token)
    upgrade_list = []
    for item in data:
        su = item.get('id')
        upgrade_list.append(su)
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
                if upgrade['id'] in coold
