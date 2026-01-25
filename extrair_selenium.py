import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

ROOT_URL = "https://gofile.io/d/3JqmRC"
ARQUIVO_SAIDA = "videos_processados.txt"

def explorar_gofile(driver, url, nivel=0):
    indent = "  " * nivel
    print(f"{indent}Pasta: {url}")
    try:
        driver.get(url)
        time.sleep(12) 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # 1. Mapear subpastas
        links = driver.find_elements(By.TAG_NAME, "a")
        urls_pastas = []
        for l in links:
            try:
                href = l.get_attribute("href")
                if href and "/d/" in href and href.strip("/") != url.strip("/") and href != ROOT_URL:
                    if href not in urls_pastas:
                        urls_pastas.append(href)
            except:
                continue

        # 2. Localizar e clicar nos botões de Play
        botoes = driver.find_elements(By.XPATH, "//button[contains(., 'Play')] | //i[contains(@class, 'fa-play')]/..")
        print(f"{indent}Videos: {len(botoes)} | Subpastas: {len(urls_pastas)}")

        for i in range(len(botoes)):
            try:
                # Re-localiza os botoes para evitar erro de elemento obsoleto
                btns = driver.find_elements(By.XPATH, "//button[contains(., 'Play')] | //i[contains(@class, 'fa-play')]/..")
                if i < len(btns):
                    print(f"{indent}  Processando video {i+1}...")
                    driver.execute_script("arguments[0].scrollIntoView(true);", btns[i])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", btns[i])
                    time.sleep(3) # Tempo de visualizacao
                    
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
            except:
                continue

        # 3. Recursividade (entrar nas pastas)
        for p_url in set(urls_pastas):
            explorar_gofile(driver, p_url, nivel + 1)

    except Exception as e:
        print(f"{indent}Erro na pasta: {e}")

# --- CONFIGURACAO GITHUB ACTIONS ---
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options
