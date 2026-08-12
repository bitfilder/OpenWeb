import socket
import dns.resolver
import httpx

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None 

def get_geo(ip):
    if ip:
        url = f'http://ip-api.com/json/{ip}'
        r = httpx.get(url)
        a = r.json()
        ret = {
            'city': a.get('city'),
            'country': a.get('country'),
            'isp': a.get('isp'),
            'region': a.get('regionName'),
            'timezone': a.get('timezone')
        }
        return ret 
    else:
        return None

def get_dns(domain):
    records = {'A': [], 'MX': [], 'NS': [], 'TXT': []}
    e = ['A', 'MX', 'NS', 'TXT']
    for a in e:
        try:
            anser = dns.resolver.resolve(domain, a)
            for r in anser:
                if a == 'MX':
                    records[a].append(str(r.exchange))
                elif a == 'TXT':
                    for txt in r.strings:
                        records[a].append(txt.decode())
                else:
                    records[a].append(str(r))
        except:
            pass
    return records

def get_headers(domain):
    try:
        r = httpx.get(f'https://{domain}', timeout=5)
        return dict(r.headers)
    except:
        try:
            r = httpx.get(f'http://{domain}', timeout=5)
            return dict(r.headers)
        except:
            return None