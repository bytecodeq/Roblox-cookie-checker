"""
-> Author: github.com/evilstrix
-> Date: 24.11.2024 
"""

__Author__ = "Strix"
__Social__ = "github.com/evilstrix"

try:
    import asyncio
    import aiohttp
    import random
    import os
    import datetime
    import configparser
    from typing import List, Dict, Any
    from fake_useragent import UserAgent
    import pystyle
    from pystyle import Center, System
except ImportError:
    os.system('pip install asyncio')
    os.system('pip install aiohttp')
    os.system('pip install random')
    os.system('pip install requests')
    os.system('pip install configparser')
    os.system('pip install datetime')
    os.system('pip install fake_useragent')

"""
-> TODO: Humanize the accounts after checking them (Ex: changing bio, avatar etc) and genning accs before checking and humanizing them
"""

"""
 --- Configs and utility classes ---
"""
class Colors:
    c: str = "\033[32m"  # green
    d: str = "\033[31m"  # red
    a: str = "\033[34m"  # blue
    l: str = "\033[0m"   # reset
    lb: str = "\033[90m"  # gray

class Utils:
    @staticmethod
    def clear():
        os.system('clear||cls')

    @staticmethod
    def title():
        os.system(f'title Cookie Checker ┃ Made by Strix ┃ github.com/evilstrix')

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

"""
 --- Headers and Banner ---
"""
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
    print(Center.XCenter(banner))
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

"""
 --- Cookie Checking function ---
"""
valid_count = 0
invalid_count = 0
count_lock = asyncio.Lock()

async def check(cookie: str, headers: Dict[str, str], proxy_mode: str, proxies: List[str]) -> None:
    global valid_count, invalid_count
    try:
        cookies = {'.ROBLOSECURITY': cookie}

        async with aiohttp.ClientSession() as session:
            if proxy_mode == 'proxies':
                proxy = random.choice(proxies)
                try:
                    async with session.get("https://users.roblox.com/v1/users/authenticated", cookies=cookies, headers=headers, proxy=proxy) as r:
                        await handle_response(r, cookie)
                except Exception as e:
                    print(f"{Colors.d}Error with proxy: {e}{Colors.d}")
            else:
                try:
                    async with session.get("https://users.roblox.com/v1/users/authenticated", cookies=cookies, headers=headers) as r:
                        await handle_response(r, cookie)
                except Exception as e:
                    print(f"{Colors.d}Error: {e}{Colors.d}")

    except Exception as e:
        print(f"{Colors.d}Error: {e}{Colors.d}")

async def handle_response(r: aiohttp.ClientResponse, cookie: str) -> None:
    global valid_count, invalid_count
    async with count_lock:
        if r.status == 200:
            valid_count += 1
            print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.lb}[{Colors.lb}{Colors.a}Cookie{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}{cookie[:59]} Valid (Status 200){Colors.c}")
            with open(f"output/valids.txt", "a", encoding="utf-8") as file:
                file.write(cookie + "\n")
        else:
            invalid_count += 1
            print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.lb}[{Colors.lb}{Colors.a}Cookie{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.d}{cookie[:59]} Invalid (Status {r.status}){Colors.d}")

"""
 --- Main Checking function ---
"""
async def check_batch(batch: List[str], headers: Dict[str, str], proxy_mode: str, proxies: List[str]) -> None:
    tasks = []
    for cookie in batch:
        cookie = cookie.strip()
        tasks.append(check(cookie, headers, proxy_mode, proxies))
    await asyncio.gather(*tasks)

async def checker(cookies: List[str], proxy_mode: str, proxies: List[str], thread_count: int, headers: Dict[str, str]) -> None:
    global valid_count, invalid_count
    batch_size = len(cookies) // thread_count
    tasks = []
    for t in range(thread_count):
        start = t * batch_size
        end = (t + 1) * batch_size if t != thread_count - 1 else len(cookies)
        batch = cookies[start:end]
        tasks.append(check_batch(batch, headers, proxy_mode, proxies))

    await asyncio.gather(*tasks)

"""
 --- Results function ---
"""
def show_results() -> None:
    Utils.clear()
    print(banner)
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Valids{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}{valid_count}")
    print(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Invalids{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}{invalid_count}")
    input(f"{Colors.lb}DBG{Colors.lb} {Colors.a}»{Colors.a} {Colors.a}{Colors.lb}[{Colors.lb}{Colors.a}Press{Colors.a}{Colors.lb}]{Colors.lb} {Colors.lb}->{Colors.lb} {Colors.c}Enter to exit")

"""
 --- Main Function ---
"""
async def main() -> int:
    global valid_count, invalid_count
    Utils.clear()
    Utils.title()
    Utils.size()
    print(Center.XCenter(banner))

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
            return 1

    headers = generate_headers()

    await checker(cookies, proxy_mode, proxies, thread_count, headers)

    show_results()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
