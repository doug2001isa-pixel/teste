import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Acessando Gofile...")
        page.goto("https://gofile.io/d/3JqmRC")
        
        # Espera o carregamento dos itens
        page.wait_for_selector(".contentItem", timeout=20000)
        
        # Encontra todos os itens (pastas e arquivos)
        items = page.query_selector_all(".contentItem")
        
        for item in items:
            # Verifica se é pasta ou vídeo (simplificado pela lógica de clique)
            item_name = item.inner_text()
            print(f"Processando: {item_name}")
            
            try:
                item.click()
                time.sleep(2) # Espera abrir
                
                # Se houver um elemento de vídeo na tela
                video = page.query_selector("video")
                if video:
                    print(f"Vídeo detectado. Reproduzindo por 5 segundos...")
                    time.sleep(5)
                
                # Volta para a listagem se necessário
                # page.go_back() 
            except Exception as e:
                print(f"Erro ao interagir com {item_name}: {e}")

        browser.close()

if __name__ == "__main__":
    run()
