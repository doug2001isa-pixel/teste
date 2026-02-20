import time
import subprocess
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_chrome_version():
    """Detecta a versão do Chrome instalada no runner do GitHub"""
    try:
        version_str = subprocess.check_output(["google-chrome", "--version"]).decode("utf-8")
        version_match = re.search(r"(\d+)\.", version_str)
        return int(version_match.group(1))
    except:
        return 144  # Fallback caso a detecção falhe

# --- CONFIGURAÇÕES DO NAVEGADOR ---
options = uc.ChromeOptions()
options.add_argument("--headless=new") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

chrome_ver = get_chrome_version()
print(f"🚀 Iniciando navegador (Chrome v{chrome_ver})...")

# Inicializa o driver com a versão correta para evitar o erro de SessionNotCreated
driver = uc.Chrome(options=options, version_main=chrome_ver)

try:
    url = "https://gofile.io/d/3JqmRC"
    driver.get(url)
    
    print(f"⏳ Aguardando carregamento de: {url}")
    # O GoFile é pesado; o WebDriverWait é essencial aqui
    wait = WebDriverWait(driver, 30) 
    
    # Espera até que a lista de arquivos (ou o container de arquivos) apareça
    # Tentamos um seletor comum no GoFile para a lista de arquivos
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#filesList, .file_Name")))
    
    print("✅ Página carregada com sucesso!")
    print("Título:", driver.title)
    
    # Listar nomes dos arquivos encontrados
    arquivos = driver.find_elements(By.CLASS_NAME, "file_Name")
    
    if not arquivos:
        print("⚠️ Nenhum arquivo visível. O site pode estar bloqueando bots ou a pasta está vazia.")
    else:
        for arq in arquivos:
            print(f"📄 Arquivo encontrado: {arq.text}")

    # Cria um arquivo de log para o GitHub Artifacts não dar erro de "não encontrado"
with open("videos_processados.txt", "w") as f:
    f.write("Iniciando processo...")

except Exception as e:
    print(f"❌ Erro durante a execução: {e}")
    # O screenshot é sua melhor ferramenta de debug no GitHub Actions
    driver.save_screenshot("debug_screen.png")

finally:
    if 'driver' in locals():
        driver.quit()
    print("🏁 Processo finalizado.")
