import socket
import httpx

def status_code(domain):
    for protocol in ['https', 'http']:
        try:
            code = httpx.get(f'{protocol}://{domain}', timeout=2)
            return code.status_code
        except:
            pass
    return None

def scan_port(domain):
    port = [80, 443, 22, 21, 3306, 8080, 25, 53, 143, 23]
    result = {}

    for ports in port:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((domain, ports)) == 0:
                result[ports] = "[+] open"
            else:
                result[ports] = "[x] closed"
            sock.close()
        except:
            result[port] = '[!] Error'
    return result

def dir(domain):
    dirc = ['/admin', '/login', '/backup', '/config', '/phpadmin']
    based = {}
    for vvv in dirc:
        for protocol in ['https', 'http']:
            try:
                a = httpx.get(f"{protocol}://{domain}{vvv}", timeout=1)
                cv = a.status_code
                if cv == 200:
                    based[vvv] = '[+]'
                else:
                    based[vvv] = '[x]'
            except:
                pass
    return based