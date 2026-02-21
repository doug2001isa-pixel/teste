import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth

def run():
    with sync_playwright() as p:
        # Inicializa o navegador em modo headless
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Aplica stealth para evitar detecção
        stealth(page)

        try:
            print("Acessando Gofile...")
            page.goto("https://gofile.io/d/3JqmRC", wait_until="networkidle", timeout=90000)
            
            # Tempo para o JavaScript carregar os itens
            time.sleep(10)

            # Localiza os arquivos/pastas
            items = page.locator(".contentItem")
            count = items.count()
            
            if count == 0:
                print("Nenhum item encontrado. Verifique o link ou seletor.")
                page.screenshot(path="sem_itens.png")
                return

            print(f"Sucesso: {count} itens encontrados.")

            for i in range(count):
                try:
                    # Seleciona o item atual do loop
                    item = items.nth(i)
                    item.scroll_into_view_if_needed()
                    
                    nome = item.inner_text().split('\n')[0]
                    print(f"[{i+1}/{count}] Abrindo: {nome}")
                    
                    item.click()
                    time.sleep(7) # Espera o carregamento do player/pasta

                    # Verifica se existe um elemento de vídeo
                    video_locator = page.locator("video")
                    if video_locator.count() > 0:
                        print(" -> Vídeo detectado. Reproduzindo por 5 segundos...")
                        # Tenta dar play via JS para garantir execução
                        page.evaluate("if(document.querySelector('video')) { document.querySelector('video').play(); }")
                        time.sleep(5)
                    else:
                        print(" -> Não é um vídeo ou demorou a carregar.")

                    # Tenta fechar o que abriu para voltar à lista
                    page.keyboard.press("Escape")
                    time.sleep(2)

                except Exception as e_item:
                    print(f"Erro ao processar item {i}: {e_item}")
                    page.keyboard.press("Escape")
                    continue

        except Exception as e_fatal:
            print(f"Erro Crítico: {e_fatal}")
            page.screenshot(path="erro_fatal.png")
        
        finally:
            print("Fechando navegador...")
            browser.close()

if __name__ == "__main__":
    run()
