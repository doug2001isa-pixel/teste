import time
import subprocess
import re
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Garante que os arquivos existam para o GitHub não dar erro de "Not Found"
with open("videos_processados.txt", "w") as f:
    f.write("Iniciando script...\n")

def get_chrome_version():
    try:
        version_str = subprocess.check_output(["google-chrome", "--version"]).decode("utf-8")
        version_match = re.search(r"(\d+)\.", version_str)
        return int(version_match.group(1))
    except:
        return 144

options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

chrome_ver = get_chrome_version()
driver = uc.Chrome(options=options, version_main=chrome_ver)

try:
    url = "https://gofile.io/d/3JqmRC"
    print(f"🚀 Acessando: {url}")
    driver.get(url)
    
    # Tira um print IMEDIATAMENTE após o get
    driver.save_screenshot("debug_screen.png")
    print("📸 Print inicial salvo.")

    # Espera generosa para o Gofile/Cloudflare
    time.sleep(25)
    
    # Tira outro print após o carregamento
    driver.save_screenshot("debug_screen_pos_load.png")
    
    print(f"📄 Titulo: {driver.title}")
    
    # Tenta listar os elementos
    arquivos = driver.find_elements(By.CLASS_NAME, "file_Name")
    
    with open("videos_processados.txt", "a") as f:
        f.write(f"Sucesso: {len(arquivos)} arquivos encontrados.\n")
        for a in arquivos:
            f.write(f"{a.text}\n")

except Exception as e:
    print(f"❌ Erro fatal: {e}")
    # Se der erro, tenta salvar o print onde parou
    try:
        driver.save_screenshot("debug_screen_erro.py.png")
    except:
        pass
finally:
    driver.quit()
