import requests
import random
import time

SITES = [
    "https://seu-site-1.com",
    "https://seu-site-2.com"
]

def rodar():
    random.shuffle(SITES)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0'}
    
    for url in SITES:
        try:
            res = requests.get(url, headers=headers, timeout=20)
            print(f"Status {res.status_code} para {url}")
            time.sleep(random.uniform(2, 10)) # Pausa entre acessos
        except Exception as e:
            print(f"Falha em {url}: {e}")

if __name__ == "__main__":
    rodar()
