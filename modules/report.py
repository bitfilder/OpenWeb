import os
from datetime import datetime

def save_info(domain, data):
    os.makedirs('reports', exist_ok=True)
    filename = f'reports/{domain}_{datetime.now().strftime('%Y%m%d_%H:%M:%S')}.txt'
    with open(filename, 'w') as f:
        f.write('\n[Report Openweb]\n')
        f.write(f'Domain: {domain}')
        f.write(f'Date: {datetime.now().strftime('%Y%m%d_%H:%M:%S')}\n')

        for key, value in data.items():
            if isinstance(value, dict):
                f.write(f'\n{key.upper()}:\n')
                for k, v in value.items():
                    f.write(f'  {k}: {v}\n')
            elif isinstance(value, list):
                f.write(f'\n{key.upper()} ({len(value)}):\n')
                for item in value[:20]:
                    f.write(f'  {item}\n')
            else:
                f.write(f'{key.upper()}: {value}\n')
    flename = f'reports/{domain}_{datetime.now().strftime('%Y%m%d_%H:%M:%S')}.txt'
    print(f'[+] Данные сохранены в файл {flename}') 