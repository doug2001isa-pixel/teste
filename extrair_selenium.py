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
        
        # Espera carregar os itens (Essencial para GitHub Actions)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "contentItem"))
            )
        except:
            print(f"{indent}⚠️ Itens não carregaram ou pasta vazia.")

        # Rola a página para garantir carregamento dinâmico
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # 1. Pastas
        links = driver.find_elements(By.TAG_NAME, "a")
        urls_pastas = []
        for l in links:
            try:
                href = l.get_attribute("href")
                if href and "/d/" in href and href.strip("/") != url.strip("/") and href != ROOT_URL:
                    if href not in urls_pastas: urls_pastas.append(href)
            except: continue

        # 2. Vídeos (Play) - XPath aprimorado para o novo layout do GoFile
        botoes = driver.find_elements(By.XPATH, "//button[contains(., 'Play')] | //i[contains(@class, 'fa-play')]/..")
        print(f"{indent}🎥 Vídeos: {len(botoes)} | 📂 Subpastas: {len(urls_pastas)}")

        for i in range(len(botoes)):
            try:
                # Re-localiza para evitar 'stale element'
                btns = driver.find_elements(By.XPATH, "//button[contains(., 'Play')] | //i[contains(@class, 'fa-play')]/..")
                if i < len(btns):
                    print(f"{indent}  ▶️ Play no {i+1}...")
                    driver.execute_script("arguments[0].scrollIntoView(true);", btns[i])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", btns[i])
                    time.sleep(3) # Tempo de visualização
                    
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    
                    with open(ARQUIVO_SAIDA, "a") as f:
                        f.write(f"OK: {url} - Video {i+1}\n")
            except: continue

        # 3. Recursividade
        for p_url in set(urls_pastas):
            explorar_gofile(driver, p_url, nivel + 1)
    except Exception as e:
        print(f"{indent}❌ Erro: {e}")

# --- SETUP CHROME HEADLESS ---
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)

try:
    if not os.path.exists(ARQUIVO_SAIDA):
        with open(ARQUIVO_SAIDA, "w") as f: f.write("LOG DE ATIVIDADE\n")
    explorar_gofile(driver, ROOT_URL)
finally:
    print("\n🚀 Execução Concluída!")
    driver.quit()
