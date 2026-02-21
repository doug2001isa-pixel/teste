import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth

def run():
    with sync_playwright() as p:
        # Lançando o navegador
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Aplicando o stealth para evitar detecção
        stealth(page)

        try:
            print("Acessando Gofile...")
            # Aumentei o timeout para dar tempo da página carregar tudo
            page.goto("https://gofile.io/d/3JqmRC", wait_until="networkidle", timeout=90000)
            
            # Pequena pausa para garantir que os elementos dinâmicos apareçam
            time.sleep(10)

            # O Gofile costuma usar o seletir .contentItem para arquivos e pastas
            items = page.locator(".contentItem")
            count = items.count()
            
            if count == 0:
                print("Atenção: Nenhum item (.contentItem) encontrado.")
                page.screenshot(path="sem_itens.png")
                # Tentativa secundária: procurar por links de download/diretório
                items = page.locator('a[href*="/d/"]')
                count = items.count()
                print(f"Tentativa secundária encontrou {count} links.")

            for i in range(count):
                try:
                    item = items.nth(i)
                    # Força a visibilidade
                    item.scroll_into_view_if_needed()
                    
                    text = item.inner_text().split('\n')[0]
                    print(f"[{i+1}/{count}] Interagindo com: {text}")
                    
                    # Clica e aguarda a transição
                    item.click()
                    time.sleep(5) 

                    # Verifica se um vídeo foi carregado
                    video = page.locator("video")
                    if video.count() > 0:
                        print(" -> Vídeo detectado! Reproduzindo por 5 segundos...")
                        # Tenta dar o play caso não seja automático
                        page.evaluate("if(document.querySelector('video')) { document.querySelector('video').play(); }")
                        time.sleep(5)
                        # Aperta ESC para fechar o player ou volta
                        page.keyboard.press("Escape")
                        time.sleep(2)
                    else:
                        print(" -> Não é vídeo ou pasta. Voltando...")
                        # Se o
