import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def run():
    with sync_playwright() as p:
        # Lançando o navegador com stealth para evitar bloqueios
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        stealth_sync(page) # Aplica técnicas de camuflagem

        try:
            print("Acessando Gofile...")
            page.goto("https://gofile.io/d/3JqmRC", wait_until="networkidle", timeout=60000)
            
            # Aguarda o carregamento inicial
            time.sleep(5)

            # Seleciona todos os itens da lista (pastas e arquivos)
            # O Gofile usa a classe .contentItem para os cards
            items_locator = page.locator(".contentItem")
            count = items_locator.count()
            
            if count == 0:
                print("Nenhum item encontrado. Verificando se há bloqueio...")
                page.screenshot(path="debug.png")
                return

            print(f"Encontrados {count} itens para processar.")

            for i in range(count):
                try:
                    # Re-localiza o item para evitar erro de elemento desatualizado
                    item = items_locator.nth(i)
                    item_name = item.inner_text().split('\n')[0]
                    print(f"Abrindo: {item_name}")
                    
                    item.click()
                    time.sleep(4) # Espera o carregamento do conteúdo

                    # Verifica se existe um elemento de vídeo na página
                    video_element = page.locator("video")
                    if video_element.count() > 0:
                        print(f"-> Vídeo detectado. Reproduzindo por 5 segundos...")
                        # Tenta dar play via JavaScript para garantir
                        page.evaluate("document.querySelector('video').play()")
                        time.sleep(5)
                        
                        # Se o vídeo abriu em uma "página" nova ou modal, tentamos fechar/voltar
                        # No Gofile, geralmente clicar no 'X' ou voltar funciona
                        page.keyboard.press("Escape")
                    else:
                        print("-> Não é um vídeo ou pasta vazia. Voltando...")
                        # Se for uma pasta, talvez você queira entrar nela (aqui ele apenas clica)
                    
                    time.sleep(1)
                except Exception as e:
                    print(f"Erro ao processar item {i}: {e}")
                    continue

        except Exception as e:
            print(f"Erro fatal: {e}")
            page.screenshot(path="fatal_error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
