"""
-> Author: github.com/evilstrix
-> Date:24.11.2024 
"""

__Author__ = "Strix"
__Social__ = "github.com/evilstrix"

try:
    import sys
    from time import sleep
    from typing import List, Dict, Any
    import threading
    import pystyle
    from pystyle import System
    import datetime
    import configparser
    import random
    import os
    import requests
    import time
    from time import sleep
    import colorama
    from colorama import Fore, init
    from fake_useragent import UserAgent
except ImportError:
    os.system('pip install typing')
    os.system('pip install icecream')
    os.system('pip install colorama')
    os.system('pip install requests')
    os.system('pip install configparser')
    os.system('pip install datetime')
    os.system('pip install pystyle')
    os.system('pip install fake_useragent')

def load_proxies() -> List[str]:
    with open("input/proxies.txt", "r", encoding="utf8") as file:
        return file.read().splitlines()

"""
-> TODO: Humanize the accounts after checking them (Ex: changing bio, avatar etc) and genning accs before checking and humanizing them
"""

class Colors:
    c: str = Fore.LIGHTGREEN_EX
    d: str = Fore.LIGHTRED_EX
    a: str = Fore.BLUE
    l: str = Fore.RESET
    lb: str = Fore.LIGHTBLACK_EX

class Utils:
    @staticmethod
    def clear():
        os.system('cls')

    @staticmethod
    def title():
        os.system(f'title Cookie Checker ┃ Made by {__Author__} ┃ {__Social__}')

    timestamp = datetime.datetime.now().strftime(f'{Colors.a}%H{Colors.a}{Colors.l}:{Colors.l}{Colors.a}%M{Colors.a}{Colors.l}:{Colors.l}{Colors.a}%S')

    @staticmethod
    def size():
         System.Size(86, 25)

def load_config(config_file: str) -> Dict[str, Any]:
    config = configparser.ConfigParser()
    config.read(config_file)
    settings = config['settings']
    thread_count = settings.getint('thread_count', 5)
    proxy_mode = settings.get('proxy_mode', 'proxyless')
    return {
        'thread_count': thread_count,
        'proxy_mode': proxy_mode
    }

def load_proxies() -> List[str]:
    with open("input/proxies.txt", "r", encoding="utf8") as file:
        return file.read().splitlines()

banner = f"""
{Colors.a}╔═╗┌┬┐┬─┐┬─┐ ┬
╚═╗ │ ├┬┘│┌┴┬┘
╚═╝ ┴ ┴└─┴┴ └─"""

def generate_headers() -> Dict[str, str]:
    user_agent = UserAgent()
    build_number = "Windows 10"
    headers = {
        'User-Agent': user_agent.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    }

    Utils.clear()
    print(banner)
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Header Info{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}User-Agent:{Colors.c} {user_agent.random[:40]}")
    sleep(2)
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Header Info{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}Build Number:{Colors.c} {build_number[:38]}")
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Header Info{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}Accept-Language:{Colors.c} en-US,en;q=0.9")
    sleep(3)
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Header Info{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}Accept-Encoding:{Colors.c} gzip, deflate, br")
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Header Info{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}Connection:{Colors.c} Keep-alive")
    sleep(2)
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Header Info{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}Upgrade-Insecure-Requests:{Colors.c} 1")
    
    return headers

def check(cookie: str, index: int, headers: Dict[str, str], proxy_mode: str, proxies: List[str], valid_count: int, invalid_count: int) -> (int, int):
    try:
        cookies = {'.ROBLOSECURITY': cookie}

        if proxy_mode == 'proxies':
            proxy = random.choice(proxies)

            if proxy.startswith("http://"):
                proxy_dict = {
                    'http': proxy,
                }
            else:
                print(f"{Colors.d}DBG{Colors.d} {Colors.a}»{Colors.a} Invalid proxy format for HTTP > {proxy}{Colors.d}")
                return valid_count, invalid_count

            r = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookies, headers=headers, proxies=proxy_dict)
        else:
            r = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookies, headers=headers)

        if r.status_code == 200:
            valid_count += 1
            print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.lb}[{Colors.lb}{Colors.a}Cookie{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}{cookie[:59]} Valid (Status 200){Colors.c}")
            with open("input/valids.txt", "a", encoding="utf-8") as file:
                file.write(cookie + "\n")
        else:
            invalid_count += 1
            print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.lb}[{Colors.lb}{Colors.a}Cookie{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.d}{cookie[:59]} Invalid (Status {r.status_code}){Colors.d}")

    except Exception as e:
        print(f"{Colors.d}Error:{Colors.d} {e}")

    return valid_count, invalid_count

def check_batch(batch: List[str], start_index: int, headers: Dict[str, str], proxy_mode: str, proxies: List[str], valid_count: int, invalid_count: int) -> (int, int):
    for i, cookie in enumerate(batch, start=start_index + 1):
        cookie = cookie.strip()
        valid_count, invalid_count = check(cookie, i, headers, proxy_mode, proxies, valid_count, invalid_count)
        sleep(2)
    return valid_count, invalid_count

def checker(cookies: List[str], proxy_mode: str, proxies: List[str], thread_count: int, headers: Dict[str, str]) -> (int, int):
    valid_count = 0
    invalid_count = 0
    threads = []
    cookies_per_thread = len(cookies) // thread_count

    for t in range(thread_count):
        start = t * cookies_per_thread
        end = (t + 1) * cookies_per_thread if t != thread_count - 1 else len(cookies)
        thread = threading.Thread(target=check_batch, args=(cookies[start:end], start, headers, proxy_mode, proxies, valid_count, invalid_count))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return valid_count, invalid_count

def show_results(valid_count: int, invalid_count: int):
    Utils.clear()
    print(banner)
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Valids{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}{valid_count}")
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Invalids{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}{invalid_count}")
    input(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Press{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}Enter to exit")

def main() -> int:
    Utils.clear()
    Utils.title()
    Utils.size()
    print(banner)

    config = load_config("config.ini")
    thread_count = config['thread_count']
    proxy_mode = config['proxy_mode']

    try:
        with open("input/cookies.txt", "r", encoding="utf8") as file:
            cookies = file.read().splitlines()
    except FileNotFoundError:
        return 1

    proxies = []
    if proxy_mode == 'proxies':
        try:
            proxies = load_proxies()
        except FileNotFoundError:
            print(f"{Colors.d}Error: Proxies file not found!{Colors.d}")
            return 1

    headers = generate_headers()

    valid_count, invalid_count = checker(cookies, proxy_mode, proxies, thread_count, headers)

    show_results(valid_count, invalid_count)
    return 0

if __name__ == "__main__":
    main()