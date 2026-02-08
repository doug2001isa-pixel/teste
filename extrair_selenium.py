import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
ROOT_URL = "https://gofile.io/d/3JqmRC"
ARQUIVO_SAIDA = "videos_processados.txt"

def explorar_gofile(driver, url, nivel=0):
    indent = "  " * nivel
    print(f"{indent}📂 Pasta: {url}")
    try:
        driver.get(url)
        
        # Espera o carregamento inicial do GoFile
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "content"))
            )
        except:
            print(f"{indent}⚠️ Conteúdo demorou muito para carregar ou pasta vazia.")

        # Scroll para carregar elementos dinâmicos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # 1. Capturar Pastas
        links = driver.find_elements(By.TAG_NAME, "a")
        urls_pastas = []
        for l in links:
            try:
                href = l.get_attribute("href")
                if href and "/d/" in href and href.strip("/") != url.strip("/") and href != ROOT_URL:
                    if href not in urls_pastas: urls_pastas.append(href)
            except: continue

        # 2. Capturar Vídeos (Botão Play)
        try:
            botoes = driver.find_elements(By.XPATH, "//button[contains(., 'Play')] | //i[contains(@class, 'fa-play')]/..")
        except:
            botoes = []

        print(f"{indent}🎥 Vídeos: {len(botoes)} | 📂 Subpastas: {len(urls_pastas)}")

        for i in range(len(botoes)):
            try:
                # Re-localiza para evitar erro de elemento antigo (stale)
                btns = driver.find_elements(By.XPATH, "//button[contains(., 'Play')] | //i[contains(@class, 'fa-play')]/..")
                if i < len(btns):
                    print(f"{indent}  ▶️ Play no {i+1}...")
                    
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btns[i])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", btns[i])
                    
                    time.sleep(7) # Tempo de "visualização" no servidor
                    
                    # Fecha popups ou abas de anúncio que o site possa abrir
                    if len(driver.window_handles) > 1:
                        for window in driver.window_handles[1:]:
                            driver.switch_to.window(window)
                            driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    
                    # Salva o progresso no arquivo
                    with open(ARQUIVO_SAIDA, "a") as f:
                        f.write(f"OK: {url} - Video {i+1} - {time.ctime()}\n")
            except Exception as e:
                print(f"{indent}  ⚠️ Erro no vídeo {i+1}: {e}")
                continue

        # 3. Recursividade (Entrar nas subpastas encontradas)
        if nivel < 3: # Limite de profundidade para não travar o Action
            for p_url in list(set(urls_pastas)):
                explorar_gofile(driver, p_url, nivel + 1)
                
    except Exception as e:
        print(
