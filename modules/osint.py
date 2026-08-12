import re
import httpx
from urllib.parse import urljoin

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"

def get_link(domain):
    try:
        r = httpx.get(f'https://{domain}')
    except:
        try:
            r = httpx.get(f'http://{domain}')
        except:
            return []
    raw_links = re.findall(r'href="([^"]+)"', r.text)

    full_link = []
    for link in raw_links:
        full = urljoin(f'https://{domain}', link)
        full_link.append(full)

    filtered_links = []
    for link in full_link:
        if link.startswith('#') or link.startswith('mailto:') or link.startswith('javascript:'):
            continue
        if link.endswith(('.pdf', '.jpg', '.png', '.gif', '.mp4', '.zip')):
            continue
        filtered_links.append(link)
    
    uni = list(set(filtered_links))
    return uni

def get_email(domain):
    try:
        r = httpx.get(f'https://{domain}')
    except:
        try:
            r = httpx.get(f'http://{domain}')
        except:
            return []
    raw = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', r.text)
    ddos = list(set(raw))
    return ddos 

def soc(domain):
    socials = {
        'YouTube': f'https://youtube.com@{domain}',
        'Telegram': f'https://t.me{domain}',
        'VK': f'https://vk.com{domain}'
    }
    found = {}
    for name, url in socials.items():
        try:
            r = httpx.get(url, timeout=3)
            if r.status_code == 200:
                found[name] = url
        except:
            pass
    return found

def info(domain):
    links = get_link(domain)
    email = get_email(domain)
    fsociety = soc(domain)
    
    # url
    print(f"{BOLD}{YELLOW}Найдено веб-ссылок (показ топ-10):{RESET}")
    if links:
        for link in links[:10]:
            if link:
                print(f"  {GREEN}[+]{RESET} {link}")
            else:
                print(f"  {RED}[x] Не удалось получить данные для ссылки{RESET}")
    else:
        print(f"  {RED}[x] Полезные ссылки на сайте не обнаружены{RESET}")
    #email 
    print(f"\n{BOLD}{YELLOW}Обнаруженные Email-адреса:{RESET}")
    if email:
        for emails in email:
            if emails:
                print(f"  {GREEN}[+]{RESET} {emails}")
            else:
                print(f"  {RED}[x] Ошибка парсинга email данных{RESET}")
    else:
        print(f"  {RED}[x] Контактные email-адреса не найдены{RESET}")
        
    # soc
    print(f"\n{BOLD}{YELLOW}Активность в соцсетях ({len(fsociety)}):{RESET}")
    if fsociety:
        for n, m in fsociety.items():
            if m:
                print(f"  {GREEN}[+]{RESET} {BOLD}{n}{RESET}: {m}")
            else:
                print(f"  {RED}[x] Не удалось связаться с платформой{RESET}")
    else:
        print(f"  {RED}[x] Связанные социальные сети не обнаружены{RESET}")
        
    print(f"\n{BOLD}{MAGENTA}=================================================={RESET}\n")
