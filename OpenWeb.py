import os
import sys
import socket
import time
from modules.recon import get_ip, get_geo, get_dns, get_headers
from modules.scan import scan_port, status_code, dir
from modules.osint import info
from modules.report import save_info

# Цвета
red = '\033[35m'
blue = '\033[33m'
ff = '\033[32m'
qq = '\033[0m'
cyan = '\033[36m'
white = '\033[37m'

def clear():
    os.system('clear')

def menu():
    a = f'''  
{white}[1] - scan         {red}/==========*{qq}   
{white}[2] - Recon       {red}/##########//{qq}  
{white}[3] - info       {red}/===========*{qq}   
{white}[4] - Otchet    {red}/$/{qq}{blue}┏━┓┏━┓┏━╸┏┓╻╻ ╻┏━╸┏┓{qq}
{white}[5] - options  {red}/$/{qq} {blue}┃ ┃┣━┛┣╸ ┃┗┫┃╻┃┣╸ ┣┻┓{qq}
{white}[6] - exit    {red}/$/{qq}  {blue}┗━┛╹  ┗━╸╹ ╹┗┻┛┗━╸┗━┛{qq}
'''
    print(a)

def recon():
    clear()
    domain = input(f'{white}Введите домен: {qq}')
    print(f"{cyan}[+] Поиск информации о {domain}...{qq}")
    
    ip = get_ip(domain)
    info = get_geo(ip)
    dns = get_dns(domain)
    headers = get_headers(domain)
    data = {
        'ip': ip,
        'info': info,
        'dns': dns,
        'headers': headers
    }
    save_info(domain, data)
    if ip:
        print(f"\n{ff}IP-адрес:{qq} {white}{ip}{qq}")
        time.sleep(0.4)
        
        if info:
            print(f"\n{cyan}ГЕО-ДАННЫЕ:{qq}")
            for key, value in info.items():
                print(f"  {white}{key}:{qq} {ff}{value}{qq}")
        else: 
            print(f'\n{blue}Не удалось получить геоданные для [{domain}]{qq}')
    else:
        print(f"\n{blue}Не удалось получить IP для [{domain}]{qq}")
        print(f"{red}{'─' * 40}{qq}")
        time.sleep(0.3)
    
    print(f"\n{cyan}DNS-ЗАПИСИ:{qq}")
    for key, value in dns.items():
        val_display = f'{cyan} | {qq}'.join(value) if value else f'{red}не найдено{qq}'
        print(f"  {white}{key}:{qq} {val_display}")
    
    if headers:
        print(f"\n{cyan}ЗАГОЛОВКИ:{qq}")
        for key, value in headers.items():
            print(f"  {white}{key}:{qq} {value}")
    else:
        print(f"\n{blue}Заголовки: не получены{qq}")
    
    print(f"\n{red}{'─' * 40}{qq}")
    input(f"\n{red}Нажмите Enter для возврата...{qq}")
    clear()

def scan():
    clear()
    domain = input(f'{white}[+] Введите домен: ')
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        print('[x] Домен не существует!')
        input(f'\n{red}Нажмите Enter...{qq}')
        clear()
        return
    print(f'{cyan}[+] Сканирование {domain}...{qq}')
    # http stsus
    status = status_code(domain)
    if status:
        print(f'{ff}[+] Status code:{qq} {status}')
    else:
        print(f'{blue}[x] Status code: не получен{qq}')
    # port
    portss = scan_port(domain)
    if portss:
        print(f'{cyan}Порты:{qq}')
        for p,s in portss.items():
            print(f'{p}: {s}')
    else:
        pass
    # dir
    dirss = dir(domain)
    if dirss:
        print(f'{cyan}Директории: {qq}')
        for dd, bb in dirss.items():
            print(f'{dd}: {bb}')
    else:
        pass
    data = {
        "statuscode:": status,
        'ports': portss,
        'dir': dirss
    }
    save_info(domain, data)
    input(f'\n{red}Нажмите Enter...{qq}')
    clear()

def osint():
    clear()
    domain = input(f'{white}[+] Введите домен: ')
    print(f'{cyan}[+] Сканирование {domain}...{qq}')
    info(domain)
    input(f'\n{red}Нажмите Enter...{qq}')
    clear()

def options():
    clear()
    print('Настройки:')
    print('[1] - Удалить отчеты')
    ch = input('> ')
    if ch == '1':
        import shutil
        if os.path.exists('reports'):
            shutil.rmtree('reports')
            print('\n[+] Успешно')
        else:
            print('[x] Папка не найдена')
    input(f'\n{red}Нажмите Enter...{qq}')
    clear()

def report():
    clear()
    print(f'{cyan}[+] Отчёты в разработке{qq}')
    input(f"\n{red}Нажмите Enter...{qq}")
    clear()

def main():
    try:
        while True:
            menu()
            choice = input(f"{white}Выберите пункт: {qq}")
        
            if choice == '2':
                recon()
            elif choice == '1':
                scan()
            elif choice == '6':
                clear()
                print(f"{red}Выход...{qq}")
                sys.exit()
            elif choice == '3':
                osint()
            elif choice == '5':
                options()
            elif choice == '4':
                report()
            else:
                clear()
    except KeyboardInterrupt:
        clear()        
if __name__ == "__main__":
    clear()
    main()