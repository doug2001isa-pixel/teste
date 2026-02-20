import time
import subprocess
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_chrome_version():
    try:
        version_str = subprocess.check_output(["google-chrome", "--version"]).decode("utf-8")
        version_match = re.search(r"(\d+)\.", version_str)
        return int(version_match.group(1))
    except:
        return 144

# Configurações
options = uc.ChromeOptions()
options.add_argument("--headless=new") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

chrome_ver = get_chrome_version()
print(f"🚀 Iniciando Chrome v{chrome_ver}...")

driver = uc.Chrome(options=options, version_main=chrome_ver)

try:
    url = "https://gofile.io/d/3JqmRC"
    driver.get(url)
    
    # 1. Espera extra inicial para o Cloudflare/JS processar
    print(f"⏳ Aguardando renderização inicial...")
    time.sleep(15) 
    
    # 2. Tira um print preventivo para vermos o estado da página
    driver.save_screenshot("estado_inicial.png")
    
    wait = WebDriverWait(driver, 45) # Aumentamos para 45s
    
    print(f"🔍 Procurando arquivos em: {url}")
    # Tentamos um seletor mais genérico que engloba qualquer item da lista
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.file, .file_Name, #filesList")))
    
    arquivos = driver.find_elements(By.CLASS_NAME, "file_Name")
    
    # ... resto do código de salvar arquivos ...

except Exception as e:
    print(f"❌ Erro: {e}")
    driver.save_screenshot("debug_screen.png")
    # Garante que o log seja criado para o upload não falhar
    with open("videos_processados.txt", "w") as f:
        f.write(f"Falha na captura: {time.ctime()}")

finally:
    driver.quit()
    print("🏁 Processo finalizado.")
