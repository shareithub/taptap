import http.client
import asyncio
import json
import random
import string
import time
import base64
from datetime import datetime
from urllib.parse import unquote
from utils.headers import headers_set
from utils.queries import QUERY_USER, QUERY_LOGIN, MUTATION_GAME_PROCESS_TAPS_BATCH, QUERY_BOOSTER, QUERY_NEXT_BOSS
from utils.queries import QUERY_TASK_VERIF, QUERY_TASK_COMPLETED, QUERY_GET_TASK, QUERY_TASK_ID, QUERY_GAME_CONFIG

url = "https://api-gw-tg.memefi.club/graphql"
def load_proxies():
    with open('proxy.txt', 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

proxies = load_proxies()

# HANDLE SEMUA ERROR TAROH DISINI BANG SAFE_POST
def safe_post(url, headers, json_payload):
    retries = 5
    timeout = 5  # Timeout in seconds for each connection attempt
    for attempt in range(retries):
        try:
            if proxies:
                proxy = random.choice(proxies)
                if '@' in proxy:
                    user_pass, proxy_ip = proxy.split('@')
                    proxy_auth = base64.b64encode(user_pass.encode()).decode()
                else:
                    proxy_ip = proxy
                    proxy_auth = None

                conn = http.client.HTTPSConnection(proxy_ip, timeout=timeout)
                if proxy_auth:
                    conn.set_tunnel(url, 443, headers={"Proxy-Authorization": f"Basic {proxy_auth}"})
                else:
                    conn.set_tunnel(url, 443)
            else:
                conn = http.client.HTTPSConnection(url, timeout=timeout)
            
            payload = json.dumps(json_payload)
            conn.request("POST", "/graphql", payload, headers)
            res = conn.getresponse()
            response_data = res.read().decode("utf-8")
            if res.status == 200:
                return json.loads(response_data)  # Return the JSON response if successful
            else:
                print(f"❌ Gagal dengan status {res.status}, mencoba lagi ")
        except (http.client.HTTPException, TimeoutError) as e:
            print(f"❌ Error: {e}, mencoba lagi ")
        if attempt < retries - 1:  # Jika ini bukan percobaan terakhir, tunggu sebelum mencoba lagi
            time.sleep(10)
        else:
            print("❌ Gagal setelah beberapa percobaan. Memulai ulang...")
            return None
    return None

def generate_random_nonce(length=52):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Mendapatkan akses token
def fetch(account_line):
    with open('query_id.txt', 'r') as file:
        lines = file.readlines()
        raw_data = lines[account_line - 1].strip()

    tg_web_data = unquote(unquote(raw_data))
    query_id = tg_web_data.split('query_id=', maxsplit=1)[1].split('&user', maxsplit=1)[0]
    user_data = tg_web_data.split('user=', maxsplit=1)[1].split('&auth_date', maxsplit=1)[0]
    auth_date = tg_web_data.split('auth_date=', maxsplit=1)[1].split('&hash', maxsplit=1)[0]
    hash_ = tg_web_data.split('hash=', maxsplit=1)[1].split('&', maxsplit=1)[0]

    user_data_dict = json.loads(unquote(user_data))

    url = 'api-gw-tg.memefi.club'
    headers = headers_set.copy()  # Use headers from utils/headers.py
    data = {
        "operationName": "MutationTelegramUserLogin",
        "variables": {
            "webAppData": {
                "auth_date": int(auth_date),
                "hash": hash_,
                "query_id": query_id,
                "checkDataString": f"auth_date={auth_date}\nquery_id={query_id}\nuser={unquote(user_data)}",
                "user": {
                    "id": user_data_dict["id"],
                    "allows_write_to_pm": user_data_dict["allows_write_to_pm"],
                    "first_name": user_data_dict["first_name"],
                    "last_name": user_data_dict["last_name"],
                    "username": user_data_dict.get("username", "Username gak diset"),
                    "language_code": user_data_dict["language_code"],
                    "version": "7.2",
                    "platform": "ios",
                    "is_premium": user_data_dict.get("is_premium", False)
                }
            }
        },
        "query": "mutation MutationTelegramUserLogin($webAppData: TelegramWebAppDataInput!) {\n  telegramUserLogin(webAppData: $webAppData) {\n    access_token\n    __typename\n  }\n}"
    }

    conn = http.client.HTTPSConnection(url)
    payload = json.dumps(data)
    conn.request("POST", "/graphql", payload, headers)
    res = conn.getresponse()
    response_data = res.read().decode("utf-8")

    if res.status == 200:
        try:
            json_response = json.loads(response_data)
            if 'errors' in json_response:
                return None
            else:
                access_token = json_response['data']['telegramUserLogin']['access_token']
                return access_token
        except json.JSONDecodeError:
            print("Failed to decode JSON response")
            return None
    else:
        return None

# Cek akses token
def cek_user(index):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy()  # Membuat salinan headers_set agar tidak mengubah variabel global
    headers['Authorization'] = f'Bearer {access_token}'

    json_payload = {
        "operationName": "QueryTelegramUserMe",
        "variables": {},
        "query": QUERY_USER
    }

    response = safe_post(url, headers, json_payload)
    if response and 'errors' not in response:
        user_data = response['data']['telegramUserMe']
        return user_data  # Mengembalikan hasil response
    else:
        print(f"❌ Gagal dengan status {response}")
        return None  # Mengembalikan None jika terjadi error

def activate_energy_recharge_booster(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy()  # Membuat salinan headers_set agar tidak mengubah variabel global
    headers['Authorization'] = f'Bearer {access_token}'

    recharge_booster_payload = {
        "operationName": "telegramGameActivateBooster",
        "variables": {"boosterType": "Recharge"},
        "query": QUERY_BOOSTER
    }

    response = safe_post(url, headers, recharge_booster_payload)
    if response and 'data' in response and response['data'] and 'telegramGameActivateBooster' in response['data']:
        new_energy = response['data']['telegramGameActivateBooster']['currentEnergy']
        print(f"\n🔋 Energi terisi. Energi saat ini: {new_energy}")
    else:
        print("❌ Gagal mengaktifkan Recharge Booster: Data tidak lengkap atau tidak ada.")

def activate_booster(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"
    print("\r🚀 Mengaktifkan Turbo Boost ... ", end="", flush=True)

    headers = headers_set.copy()  # Membuat salinan headers_set agar tidak mengubah variabel global
    headers['Authorization'] = f'Bearer {access_token}'

    recharge_booster_payload = {
        "operationName": "telegramGameActivateBooster",
        "variables": {"boosterType": "Turbo"},
        "query": QUERY_BOOSTER
    }

    response = safe_post(url, headers, recharge_booster_payload)
    if response and 'data' in response:
        current_health = response['data']['telegramGameActivateBooster']['currentBoss']['currentHealth']
        current_level = response['data']['telegramGameActivateBooster']['currentBoss']['level']
        if current_health == 0:
            print("\nBos telah dikalahkan, mengatur bos berikutnya...")
            set_next_boss(index, headers)
        else:
            if god_mode == 'y':
                total_hit = 500000000
            else:
                total_hit = 500000
            tap_payload = {
                "operationName": "MutationGameProcessTapsBatch",
                "variables": {
                    "payload": {
                        "nonce": generate_random_nonce(),
                        "tapsCount": total_hit
                    }
                },
                "query": MUTATION_GAME_PROCESS_TAPS_BATCH
            }
            for _ in range(50):
                tap_result = submit_taps(index, tap_payload)
                if tap_result is not None:
                    if 'data' in tap_result and 'telegramGameProcessTapsBatch' in tap_result['data']:
                        tap_data = tap_result['data']['telegramGameProcessTapsBatch']
                        if tap_data['currentBoss']['currentHealth'] == 0:
                            print("\nBos telah dikalahkan, mengatur bos berikutnya...")
                            set_next_boss(index, headers)
                            print(f"\rTapped ✅ Coin: {tap_data['coinsAmount']}, Monster ⚔️: {tap_data['currentBoss']['currentHealth']} - {tap_data['currentBoss']['maxHealth']}    ")
                else:
                    print(f"❌ Gagal dengan status {tap_result}, mencoba lagi...")
    else:
        print(f"❌ Gagal dengan status {response}, mencoba lagi...")

def submit_taps(index, json_payload):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy()
    headers['Authorization'] = f'Bearer {access_token}'

    response = safe_post(url, headers, json_payload)
    if response:
        return response  # Pastikan mengembalikan data yang sudah diurai
    else:
        print(f"❌ Gagal dengan status {response}, mencoba lagi...")
        return None  # Mengembalikan None jika terjadi error

def set_next_boss(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy()  # Membuat salinan headers_set agar tidak mengubah variabel global
    headers['Authorization'] = f'Bearer {access_token}'
    boss_payload = {
        "operationName": "telegramGameSetNextBoss",
        "variables": {},
        "query": QUERY_NEXT_BOSS
    }

    response = safe_post(url, headers, boss_payload)
    if response and 'data' in response:
        print("✅ Berhasil ganti bos.", flush=True)
    else:
        print("❌ Gagal ganti bos.", flush=True)

# cek stat
def cek_stat(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"

    headers = headers_set.copy()  # Membuat salinan headers_set agar tidak mengubah variabel global
    headers['Authorization'] = f'Bearer {access_token}'

    json_payload = {
        "operationName": "QUERY_GAME_CONFIG",
        "variables": {},
        "query": QUERY_GAME_CONFIG
    }

    response = safe_post(url, headers, json_payload)
    if response and 'errors' not in response:
        user_data = response['data']['telegramGameGetConfig']
        return user_data
    else:
        print(f"❌ Gagal dengan status {response}")
        return None  # Mengembalikan None jika terjadi error

def check_and_complete_tasks(index, headers):
    access_token = fetch(index + 1)
    headers = headers_set.copy()  # Membuat salinan headers_set agar tidak mengubah variabel global
    headers['Authorization'] = f'Bearer {access_token}'
    task_list_payload = {
        "operationName": "GetTasksList",
        "variables": {"campaignId": "50ef967e-dd9b-4bd8-9a19-5d79d7925454"},
        "query": QUERY_GET_TASK
    }

    response = safe_post(url, headers, task_list_payload)
    if response and 'errors' not in response:
        tasks = response
    else:
        print(f"❌ Gagal dengan status {response}")
        return False

    all_completed = all(task['status'] == 'Completed' for task in tasks['data']['campaignTasks'])
    if all_completed:
        print(f"\r[ Akun {index + 1} ] Semua tugas telah selesai. ✅            ", flush=True)
        return True

    print(f"\n[ Akun {index + 1} ]\nList Task:\n")
    for task in tasks['data']['campaignTasks']:
        print(f"{task['name']} | {task['status']}")

        if task['name'] == "Follow telegram channel" and task['status'] == "Pending":
            print(f"⏩ Skipping task: {task['name']}")
            continue  # Skip task jika nama task adalah "Follow telegram channel" dan statusnya "Pending"

        if task['status'] == "Pending":
            print(f"\🔍 Viewing task: {task['name']}", end="", flush=True)

            view_task_payload = {"operationName": "GetTaskById", "variables": {"taskId": task['id']}, "query": "fragment FragmentCampaignTask on CampaignTaskOutput {\n  id\n  name\n  description\n  status\n  type\n  position\n  buttonText\n  coinsRewardAmount\n  link\n  userTaskId\n  isRequired\n  iconUrl\n  __typename\n}\n\nquery GetTaskById($taskId: String!) {\n  campaignTaskGetConfig(taskId: $taskId) {\n    ...FragmentCampaignTask\n    __typename\n  }\n}"}
            print(view_task_payload)
            view_response = safe_post(url, headers, view_task_payload)
            if 'errors' in view_response:
                print(f"\r❌ Gagal mendapatkan detail task: {task['name']}")
                print(view_response)
            else:
                task_details = view_response['data']['campaignTaskGetConfig']
                print(f"\r🔍 Detail Task: {task_details['name']}", end="", flush=True)

  

            print(f"\r🔍 Verifikasi task: {task['name']}                                                                ", end="", flush=True)
            verify_task_payload = {
                "operationName": "CampaignTaskToVerification",
                "variables": {"userTaskId": task['userTaskId']},
                "query": QUERY_TASK_VERIF
            }
            verify_response = safe_post(url, headers, verify_task_payload)
            if 'errors' not in verify_response:
                print(f"\r✅ {task['name']} | Moved to Verification", flush=True)
            else:
                print(f"\r❌ {task['name']} | Failed to move to Verification", flush=True)
                print(verify_response)

         

    # Cek ulang task setelah memindahkan ke verification
    updated_tasks = safe_post(url, headers, task_list_payload)
    print("\nUpdated Task List After Verification:\n")
    for task in updated_tasks['data']['campaignTasks']:
        print(f"{task['name']} | {task['status']}")
        if task['status'] == "Verification":
            print(f"\r🔥 Menyelesaikan task: {task['name']}", end="", flush=True)
            complete_task_payload = {
                "operationName": "CampaignTaskCompleted",
                "variables": {"userTaskId": task['userTaskId']},
                "query": QUERY_TASK_COMPLETED
            }
            complete_response = safe_post(url, headers, complete_task_payload)
            if 'errors' not in complete_response:
                print(f"\r✅ {task['name']} | Completed                         ", flush=True)
            else:
                print(f"\r❌ {task['name']} | Failed to complete            ", flush=True)

   

    return False

def main():
    print("Starting Memefi bot...")
    print("\r Mendapatkan list akun valid...", end="", flush=True)
  
    while True:
        with open('query_id.txt', 'r') as file:
            lines = file.readlines()

        # Kumpulkan informasi akun terlebih dahulu
        accounts = []
        for index, line in enumerate(lines):
            result = cek_user(index)
            if result is not None:
                first_name = result.get('firstName', 'Unknown')
                last_name = result.get('lastName', 'Unknown')
                league = result.get('league', 'Unknown')
                accounts.append((index, result, first_name, last_name, league))
            else:
                print(f"❌ Akun {index + 1}: Token tidak valid atau terjadi kesalahan")

        # Menampilkan daftar akun
        print("\rList akun:                                   ", flush=True)
        for index, _, first_name, last_name, league in accounts:
            print(f"✅ [ Akun {first_name} {last_name} ] | League 🏆 {league}")

        # Setelah menampilkan semua akun, mulai memeriksa tugas
        for index, result, first_name, last_name, league in accounts:
            print(f"\r[ Akun {index + 1} ] {first_name} {last_name} memeriksa task...", end="", flush=True)
            headers = {'Authorization': f'Bearer {result}'}
            if cek_task_enable == 'y':
                check_and_complete_tasks(index, headers)
            else:
                print(f"\r\n[ Akun {index + 1} ] {first_name} {last_name} Cek task skipped\n", flush=True)
            stat_result = cek_stat(index, headers)

            if stat_result is not None:
                user_data = stat_result
                output = (
                    f"[ Akun {index + 1} - {first_name} {last_name} ]\n"
                    f"Coin 🪙  {user_data['coinsAmount']:,} 🔋 {user_data['currentEnergy']} - {user_data['maxEnergy']}\n"
                    f"Level 🔫 {user_data['weaponLevel']} 🔋 {user_data['energyLimitLevel']} ⚡ {user_data['energyRechargeLevel']} 🤖 {user_data['tapBotLevel']}\n"
                    f"Boss 👾 {user_data['currentBoss']['level']} ❤️ {user_data['currentBoss']['currentHealth']} - {user_data['currentBoss']['maxHealth']}\n"
                    f"Free 🚀 {user_data['freeBoosts']['currentTurboAmount']} 🔋 {user_data['freeBoosts']['currentRefillEnergyAmount']}\n"
                )
                print(output, end="", flush=True)
                level_bos = user_data['currentBoss']['level']
                darah_bos = user_data['currentBoss']['currentHealth']

                if darah_bos == 0:
                    print("\nBos telah dikalahkan, mengatur bos berikutnya...", flush=True)
                    set_next_boss(index, headers)
                print("\rTapping 👆", end="", flush=True)

                energy_sekarang = user_data['currentEnergy']
                energy_used = energy_sekarang - 100
                damage = user_data['weaponLevel'] + 1
                total_tap = energy_used // damage

                if energy_sekarang < 0.25 * user_data['maxEnergy']:
                    if auto_booster == 'y':
                        if user_data['freeBoosts']['currentRefillEnergyAmount'] > 0:
                            print("\r🪫 Energy Habis, mengaktifkan Recharge Booster... \n", end="", flush=True)
                            activate_energy_recharge_booster(index, headers)
                            continue  # Lanjutkan tapping setelah recharge
                        else:
                            print("\r🪫 Energy Habis, tidak ada booster tersedia. Beralih ke akun berikutnya.\n", flush=True)
                            continue  # Beralih ke akun berikutnya
                    else:
                        print("\r🪫 Energy Habis, auto booster disable. Beralih ke akun berikutnya.\n", flush=True)
                        continue  # Beralih ke akun berikutnya

                tap_payload = {
                    "operationName": "MutationGameProcessTapsBatch",
                    "variables": {
                        "payload": {
                            "nonce": generate_random_nonce(),
                            "tapsCount": total_tap
                        }
                    },
                    "query": MUTATION_GAME_PROCESS_TAPS_BATCH
                }
                tap_result = submit_taps(index, tap_payload)
                if tap_result is not None:
                    print(f"\rTapped ✅\n ")
                else:
                    print(f"❌ Gagal dengan status {tap_result}, mencoba lagi...")

                if auto_claim_combo == 'y':
                    claim_combo(index, headers)
                if turbo_booster == 'y':
                    if user_data['freeBoosts']['currentTurboAmount'] > 0:
                        activate_booster(index, headers)

        print("=== [ SEMUA AKUN TELAH DI PROSES ] ===")

        animate_energy_recharge(15)

# Jalankan fungsi main() dan simpan hasilnya


def claim_combo(index, headers):
    access_token = fetch(index + 1)
    url = "api-gw-tg.memefi.club"
    headers = headers_set.copy()  # Membuat salinan headers_set agar tidak mengubah variabel global
    headers['Authorization'] = f'Bearer {access_token}'

    nonce = generate_random_nonce()
    taps_count = random.randint(5, 10)  # Contoh: tapsCount dinamis antara 5 dan 10
    claim_combo_payload = {
        "operationName": "MutationGameProcessTapsBatch",
        "variables": {
            "payload": {
                "nonce": nonce,
                "tapsCount": taps_count,
                "vector": vector
            }
        },
        "query": """
        mutation MutationGameProcessTapsBatch($payload: TelegramGameTapsBatchInput!) {
          telegramGameProcessTapsBatch(payload: $payload) {
            ...FragmentBossFightConfig
            __typename
          }
        }

        fragment FragmentBossFightConfig on TelegramGameConfigOutput {
          _id
          coinsAmount
          currentEnergy
          maxEnergy
          weaponLevel
          zonesCount
          tapsReward
          energyLimitLevel
          energyRechargeLevel
          tapBotLevel
          currentBoss {
            _id
            level
            currentHealth
            maxHealth
            __typename
          }
          freeBoosts {
            _id
            currentTurboAmount
            maxTurboAmount
            turboLastActivatedAt
            turboAmountLastRechargeDate
            currentRefillEnergyAmount
            maxRefillEnergyAmount
            refillEnergyLastActivatedAt
            refillEnergyAmountLastRechargeDate
            __typename
          }
          bonusLeaderDamageEndAt
          bonusLeaderDamageStartAt
          bonusLeaderDamageMultiplier
          nonce
          __typename
        }
        """
    }

    response = safe_post(url, headers, claim_combo_payload)
    if response and 'data' in response and 'telegramGameProcessTapsBatch' in response['data']:
        game_data = response['data']['telegramGameProcessTapsBatch']
        if game_data['tapsReward'] is None:
            print("❌ Combo sudah pernah diklaim: Tidak ada reward yang tersedia.")
        else:
            print(f"✅ Combo diklaim dengan sukses: Reward taps {game_data['tapsReward']}")
    else:
        print("❌ Gagal mengklaim combo: Data tidak lengkap atau tidak ada.")

def animate_energy_recharge(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\r🪫 Mengisi ulang energi {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    print("\r🔋 Pengisian energi selesai.                            ", flush=True)

cek_task_enable = 'n'
while True:
    auto_booster = input("Use Energy Booster (default n) ? (y/n): ").strip().lower()
    if auto_booster in ['y', 'n', '']:
        auto_booster = auto_booster or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

while True:
    turbo_booster = input("Use Turbo Booster (default n) ? (y/n): ").strip().lower()
    if turbo_booster in ['y', 'n', '']:
        turbo_booster = turbo_booster or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

if turbo_booster == 'y':
    while True:
        god_mode = input("Activate God Mode (1x tap monster dead) ? (y/n): ").strip().lower()
        if god_mode in ['y', 'n', '']:
            god_mode = god_mode or 'n'
            break
        else:
            print("Masukkan 'y' atau 'n'.")

while True:
    auto_claim_combo = input("Auto claim daily combo (default n) ? (y/n): ").strip().lower()
    if auto_claim_combo in ['y', 'n', '']:
        auto_claim_combo = auto_claim_combo or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

if auto_claim_combo == 'y':
    while True:
        combo_input = input("Masukkan combo (misal: 1,3,2,4,4,3,2,1): ").strip()
        if combo_input:
            vector = combo_input
            break
        else:
            print("Masukkan combo yang valid.")

# Jalankan fungsi main() dan simpan hasilnya
main()