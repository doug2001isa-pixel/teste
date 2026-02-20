import time
import subprocess
import re
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Força a criação do log no início para garantir o upload
with open("resultado.txt", "w", encoding="utf-8") as f:
    f.write("Iniciando processo...\n")

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

try:
    chrome_ver = get_chrome_version()
    print(f"🚀 Versão do Chrome detectada: {chrome_ver}")
    driver = uc.Chrome(options=options, version_main=chrome_ver)
    
    url = "https://gofile.io/d/3JqmRC"
    print(f"🌐 Acessando URL...")
    driver.get(url)
    
    # Espera 30 segundos fixa para o Cloudflare
    print("⏳ Aguardando 30 segundos para carregar...")
    time.sleep(30)
    
    # Tira o print com nome simples
    driver.save_screenshot("print_tela.png")
    print("📸 Print salvo como print_tela.png")
    
    # Tenta extrair os textos
    elementos = driver.find_elements(By.CLASS_NAME, "file_Name")
    
    with open("resultado.txt", "a", encoding="utf-8") as f:
        f.write(f"Titulo: {driver.title}\n")
        f.write(f"Elementos encontrados: {len(elementos)}\n")
        for el in elementos:
            f.write(f"Item: {el.text}\n")
    
    print(f"✅ Finalizado! Encontrados {len(elementos)} itens.")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
    with open("resultado.txt", "a", encoding="utf-8") as f:
        f.write(f"ERRO: {str(e)}\n")
finally:
    if 'driver' in locals():
        driver.quit()
