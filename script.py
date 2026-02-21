import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync  # Mudança aqui

def run():
    with sync_playwright() as p:
        # Lançando o navegador
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Agora chamando a função correta para modo síncrono
        stealth_sync(page) 

        try:
            print("Acessando Gofile...")
            page.goto("https://gofile.io/d/3JqmRC", wait_until="networkidle", timeout=90000)
            
            # Espera o carregamento inicial
            time.sleep(10)

            # O Gofile usa a classe .contentItem para arquivos e pastas
            items_locator = page.locator(".contentItem")
            count = items_locator.count()
            
            if count == 0:
                print("Aviso: Nenhum item encontrado. Verifique o link.")
                page.screenshot(path="debug_vazio.png")
                return

            print(f"Sucesso: {count} itens encontrados para processar.")

            for i in range(count):
                try:
                    item = items_locator.nth(i)
                    item.scroll_into_view_if_needed()
                    
                    nome = item.inner_text().split('\n')[0]
                    print(f"[{i+1}/{count}] Abrindo: {nome}")
                    
                    item.click()
                    time.sleep(7) 

                    # Verifica se o elemento de vídeo apareceu
                    video = page.locator("video")
                    if video.count() > 0:
                        print(" -> Vídeo detectado. Reproduzindo...")
                        # Tenta dar play via JS
                        page.evaluate("if(document.querySelector('video')) { document.querySelector('video').play(); }")
                        time.sleep(5)
                    else:
                        print(" -> Não é vídeo ou ainda está carregando.")

                    # Aperta ESC para voltar/fechar
                    page.keyboard.press("Escape")
                    time.sleep(2)

                except Exception as e_item:
                    print(f"Erro no item {i}: {e_item}")
                    page.keyboard.press("Escape")
                    continue

        except Exception as e_fatal:
            print(f"Erro Crítico: {e_fatal}")
            page.screenshot(path="erro_fatal.png")
        
        finally:
            print("Processo finalizado.")
            browser.close()

if __name__ == "__main__":
    run()
