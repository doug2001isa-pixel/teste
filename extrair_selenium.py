import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- CONFIGURAÇÕES ---
ROOT_URL = "https://gofile.io/d/3JqmRC"
ARQUIVO_SAIDA = "links_visitados.txt"

def visitar_recursivo(driver, url, nivel=0):
    indent = "  " * nivel
    print(f"{indent}📂 Pasta: {url}")
    
    try:
        driver.get(url)
        time.sleep(10) # Tempo para o GoFile carregar os itens
        
        # Coleta todos os links da página
        links = driver.find_elements(By.TAG_NAME, "a")
        
        urls_pastas = []
        urls_videos = []

        for link in links:
            href = link.get_attribute("href")
            if href:
                # Se o link tiver /d/ é pasta, se tiver /v/ é vídeo/arquivo
                if "/d/" in href and href != url and href != ROOT_URL:
                    if href not in urls_pastas:
                        urls_pastas.append(href)
                elif "/v/" in href:
                    if href not in urls_videos:
                        urls_videos.append(href)

        print(f"{indent}🔍 Achei {len(urls_pastas)} pastas e {len(urls_videos)} arquivos.")

        # Visita cada vídeo para renovar o prazo
        for v_url in urls_videos:
            print(f"{indent}  🎥 Visitando: {v_url}")
            driver.execute_script(f"window.open('{v_url}', '_blank');")
            time.sleep(2) # Espera a aba abrir
            driver.switch_to.window(driver.window_handles[-1])
            
            time.sleep(5) # Tempo de "permanência" no vídeo
            
            with open(ARQUIVO_SAIDA, "a") as f:
                f.write(f"{v_url}\n")
                
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # Entra nas subpastas encontrada
        for p_url in urls_pastas:
            visitar_recursivo(driver, p_url, nivel + 1)

    except Exception as e:
        print(f"{indent}⚠️ Erro: {e}")

# --- INÍCIO DO SCRIPT ---
options = Options()
# options.add_argument("--headless") # Mantenha desativado para testar visualmente
driver = webdriver.Chrome(options=options)

try:
    if not os.path.exists(ARQUIVO_SAIDA):
        with open(ARQUIVO_SAIDA, "w") as f:
            f.write("--- LOG DE ACESSOS ---\n")
            
    visitar_recursivo(driver, ROOT_URL)
    print("\n✨ Tudo pronto! O script percorreu as pastas e abriu os vídeos.")
finally:
    driver.quit()
