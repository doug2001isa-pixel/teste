import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth

def run():
    with sync_playwright() as p:
        # Inicializa o navegador
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Aplica o stealth para evitar bloqueios do Gofile/Cloudflare
        stealth(page)

        try:
            print("Acessando Gofile...")
            # Timeout de 90s para garantir que a página carregue no servidor do GitHub
            page.goto("https://gofile.io/d/3JqmRC", wait_until="networkidle", timeout=90000)
            
            # Aguarda o carregamento dos elementos dinâmicos
            time.sleep(10)

            # Localiza os itens (pastas e arquivos)
            items = page.locator(".contentItem")
            count = items.count()
            
            if count == 0:
                print("Nenhum item encontrado. Salvando screenshot de debug...")
                page.screenshot(path="debug_no_items.png")
                return

            print(f"Total de itens encontrados: {count}")

            # Loop para interagir com cada item
            for i in range(count):
                try:
                    # Seleciona o item atual
                    current_item = items.nth(i)
                    current_item.scroll_into_view_if_needed()
                    
                    nome = current_item.inner_text().split('\n')[0]
                    print(f"[{i+1}/{count}] Abrindo: {nome}")
                    
                    # Clica e espera o carregamento
                    current_item.click()
                    time.sleep(5)

                    # Verifica se é um vídeo
                    video_locator = page.locator("video")
                    if video_locator.count() > 0:
                        print(f" -> Vídeo detectado. Reproduzindo...")
                        # Força o play via JavaScript
                        page.evaluate("document.querySelector('video').play().catch(e => console.log('Auto-play blocked'))")
                        time.sleep(5) # "Assiste" por 5 segundos
                        
                        # Fecha o player ou volta para a lista
                        page.keyboard.press("Escape")
                    else:
                        print(" -> Item aberto (não é vídeo ou requer clique extra).")
                        page.keyboard.press("Escape")
                    
                    time.sleep(2) # Pausa entre itens

                except Exception as e_interno
