import requests
import json
import threading
import time
from colorama import Fore, Style, init

init(autoreset=True)
def display_banner():
    print(Fore.CYAN + """
███████╗ ██████╗ ██╗      ██╗      ██████╗ ██╗    ██╗  
██╔════╝██╔═══██╗██║      ██║     ██╔═══██╗██║    ██║    
█████╗  ██║   ██║██║      ██║     ██║   ██║██║ █╗ ██║  
██╔══╝  ██║   ██║██║      ██║     ██║   ██║██║███╗██║   
██║     ╚██████╔╝███████╗ ███████╗╚██████╔╝╚███╔███╔╝    
╚═╝      ╚═════╝ ╚══════╝ ╚══════╝ ╚═════╝  ╚══╝╚══╝    

[Please  /\_/\[0m
[Follow ( o.o )[0m
[Me      > ^ <[0m
[Hey   /        \[0m
[Real (  (    )  )[0m
[Cat   \__||__/[0m

██╗  ██╗███████╗██╗   ██╗██████╗ ███████╗ █████╗ ██╗     
██║  ██║██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║     
███████║█████╗   ╚████╔╝ ██████╔╝█████╗  ███████║██║     
██╔══██║██╔══╝    ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██║██║     
██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║███████╗
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
    """)
    print(Fore.YELLOW + "=" * 65)
    print(Fore.GREEN + "✨ HeyReal Follower Bot - Premium Version ✨")
    print(Fore.YELLOW + "=" * 65)
    print(Fore.WHITE + "Created by: Dwi Bakti N Dev")
    print(Fore.WHITE + "Version: 2.0 | Status: Active")
    print(Fore.YELLOW + "=" * 65)

def load_tokens():
    try:
        with open('Token/Api.txt', 'r') as file:
            tokens = [token.strip() for token in file.readlines() if token.strip()]
        print(Fore.GREEN + f"[✓] Successfully loaded {len(tokens)} tokens")
        return tokens
    except FileNotFoundError:
        print(Fore.RED + "[✗] tokens.txt file not found!")
        return []

def get_user_input():
    print(Fore.CYAN + "\n" + "▬" * 50)
    print(Fore.WHITE + "📊 CONFIGURATION SETUP")
    print(Fore.CYAN + "▬" * 50)
    
    while True:
        try:
            num_threads = int(input(Fore.MAGENTA + "[?] Amount of threads to use: " + Fore.WHITE))
            if num_threads > 0:
                break
            else:
                print(Fore.RED + "[!] Please enter a positive number")
        except ValueError:
            print(Fore.RED + "[!] Please enter a valid number")
    
    uid = input(Fore.MAGENTA + "[?] Enter User ID: " + Fore.WHITE)
    
    print(Fore.CYAN + "▬" * 50)
    return num_threads, uid
display_banner()
tokens = load_tokens()

if not tokens:
    exit()

num_threads, uid = get_user_input()

url = "https://api.heyreal.ai/api/followUpdate"

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "nl,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "basic-params": '{"buildVersion":"1","deviceId":"Mozilla50WindowsNT100Win64x64AppleWebKit53736KHTMLlikeGeckoChrome130000Safari53736Edg130000","lang":"nl","deviceName":"Netscape","os":"Windows","osVersion":"","platform":"web"}',
    "content-length": "30",
    "content-type": "application/json",
    "origin": "https://heyreal.ai",
    "priority": "u=1, i",
    "referer": "https://heyreal.ai/",
    "sec-ch-ua": '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "traceid": "4QhUJipSkh8IePSanejixoxVT630Hz4i",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}

payload = {
    "uid": uid,
    "status": 1
}

success_count = 0
fail_count = 0
start_time = time.time()

def print_stats():
    elapsed_time = time.time() - start_time
    print(Fore.CYAN + "\n" + "▬" * 50)
    print(Fore.WHITE + "📈 REAL-TIME STATISTICS")
    print(Fore.CYAN + "▬" * 50)
    print(Fore.GREEN + f"✓ Successful: {success_count}")
    print(Fore.RED + f"✗ Failed: {fail_count}")
    print(Fore.BLUE + f"⏱️ Elapsed Time: {elapsed_time:.2f} seconds")
    print(Fore.YELLOW + f"🚀 Rate: {success_count/elapsed_time:.2f} follows/sec" if elapsed_time > 0 else "🚀 Rate: Calculating...")
    print(Fore.CYAN + "▬" * 50)

def __send__(token, follower_number):
    global success_count, fail_count
    headers_copy = headers.copy()
    headers_copy["access-token"] = token.strip()
    
    try:
        response = requests.post(url, headers=headers_copy, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            success_count += 1
            print(Fore.GREEN + f"[✓] Follower #{follower_number:04d} | Token: {token[:15]}... | Status: SUCCESS")
        else:
            fail_count += 1
            print(Fore.RED + f"[✗] Follower #{follower_number:04d} | Token: {token[:15]}... | Status: FAILED ({response.status_code})")
    except Exception as e:
        fail_count += 1
        print(Fore.RED + f"[✗] Follower #{follower_number:04d} | Token: {token[:15]}... | Error: {str(e)}")

def __loop__(thread_id):
    follower_number = 1
    print(Fore.MAGENTA + f"[~] Thread {thread_id} started")
    
    while True:
        for token in tokens:
            __send__(token, follower_number)
            follower_number += 1
        
            if follower_number % 10 == 0:
                print_stats()
            
            time.sleep(0.1)

def __main__():
    print(Fore.CYAN + "\n" + "▬" * 50)
    print(Fore.GREEN + "🚀 STARTING FOLLOW BOT...")
    print(Fore.CYAN + "▬" * 50)
    print(Fore.WHITE + f"📊 Threads: {num_threads}")
    print(Fore.WHITE + f"🔑 Tokens: {len(tokens)}")
    print(Fore.WHITE + f"🎯 Target UID: {uid}")
    print(Fore.CYAN + "▬" * 50)
    
    time.sleep(2) 
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=__loop__, args=(i+1,))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    try:
        while True:
            time.sleep(5)
            print_stats()
    except KeyboardInterrupt:
        print(Fore.RED + "\n" + "▬" * 50)
        print(Fore.RED + "🛑 BOT STOPPED BY USER")
        print(Fore.RED + "▬" * 50)
        print_stats()

if __name__ == "__main__":
    __main__()