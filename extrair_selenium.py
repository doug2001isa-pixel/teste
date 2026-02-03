import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ROOT_URL = "https://gofile.io/d/3JqmRC"
ARQUIVO_SAIDA = "videos_processados.txt"

def explorar_gofile(driver, url, nivel=0):
    indent = "  " * nivel
    print(f"{indent}📂 Pasta: {url}")
    try:
        driver.get(url)
        
        # Espera carregar o container principal
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "content"))
            )
        except:
            print(f"{indent}⚠️ Tempo esgotado para carregar a página.")

        # Scroll para ativar o carregamento de itens
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # 1. Capturar Pastas
        links = driver.find_elements(By.TAG_NAME, "a")
        urls_pastas = []
        for l in links:
            try:
                href = l.get_attribute("href")
                if href and "/d/" in href and href.strip("/") != url.strip("/") and href != ROOT_URL:
                    if href not in urls_pastas: urls_pastas.append(href)
            except: continue

        # 2. Capturar Vídeos - Melhorado para aguardar o botão ser clicável
        try:
            botoes = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Play')] | //i[contains(@class, 'fa-play')]/.."))
            )
        except:
            botoes = []

        print(f"{indent}🎥 Vídeos: {len(botoes)} | 📂 Subpastas: {len(urls_pastas)}")

        for i in range(len(botoes)):
            try:
                # Re-localiza para evitar 'stale element reference'
                btns = driver.find_elements(By.XPATH, "//button[contains(., 'Play')] | //i[contains(@class, 'fa-play')]/..")
                if i < len(btns):
                    print(f"{indent}  ▶️ Play no {i+1}...")
                    
                    # Tenta clicar via JavaScript (mais garantido no modo Headless)
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btns[i])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", btns[i])
                    
                    time.sleep(5) # Simula o tempo de visualização
                    
                    # Fecha abas extras se o GoFile abrir anúncios/popups
                    if len(driver.window_handles) > 1:
                        for window in driver.window_handles[1:]:
                            driver.switch_to.window(window)
                            driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    
                    with open(ARQUIVO_SAIDA, "a") as f:
                        f.write(f"OK: {url} - Video {i+1} - {time.ctime()}\n")
            except Exception as e:
                print(f"{indent}  ⚠️ Erro no vídeo {i+1}: {e}")
                continue

        # 3. Recursividade (limitando para evitar loop infinito)
        if nivel < 5: 
            for p_url in list(set(urls_pastas)):
                explorar_gofile(driver, p_url, nivel + 1)
                
    except Exception as e:
        print(f"{indent}❌ Erro geral na pasta: {e}")

# --- SETUP CHROME HEADLESS ---
chrome_options = Options()
chrome_options.add_argument("--headless=new") # O novo headless é melhor
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0
