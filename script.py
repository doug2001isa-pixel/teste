import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Usando um User-Agent de navegador real para tentar burlar bloqueios
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("Acessando Gofile...")
            page.goto("https://gofile.io/d/3JqmRC", wait_until="networkidle")
            
            # Espera um pouco para o JS renderizar
            time.sleep(5)

            # Tenta encontrar os links de arquivos/pastas pelo padrão de ID ou link
            # O Gofile costuma listar arquivos dentro de uma div com id 'filesContent'
            items = page.locator('a[href*="/d/"], .contentItem').all()
            
            if not items:
                print("Nenhum item encontrado. Tirando print para debug...")
                page.screenshot(path="error_screen.png")
                return

            print(f"Encontrados {len(items)} itens.")

            for index, item in enumerate(items):
                try:
                    # Scroll até o elemento
                    item.scroll_into_view_if_needed()
                    name = item.inner_text().split('\n')[0]
                    print(f"[{index}] Verificando: {name}")
                    
                    # Clica no item
                    item.click()
                    time.sleep(3)

                    # Verifica se abriu um vídeo
                    video = page.locator("video")
                    if video.
