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
    
    print(f"⏳ Aguardando conteúdo de: {url}")
    wait = WebDriverWait(driver, 30)
    
    # Espera os arquivos carregarem
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "file_Name")))
    
    arquivos = driver.find_elements(By.CLASS_NAME, "file_Name")
    
    # SALVANDO OS DADOS NO ARQUIVO (Dentro do bloco try)
    with open("videos_processados.txt", "w") as f:
        f.write(f"Relatorio de execucao: {time.ctime()}\n")
        if arquivos:
            for arq in arquivos:
                f.write(f"📄 {arq.text}\n")
                print(f"Encontrado: {arq.text}")
        else:
            f.write("Nenhum arquivo encontrado.\n")

except Exception as e:
    print(f"❌ Erro: {e}")
    driver.save_screenshot("debug_screen.png")
    # Cria o arquivo mesmo se der erro para o GitHub Actions não reclamar
    with open("videos_processados.txt", "a") as f:
        f.write(f"\nErro ocorrido as {time.ctime()}: {str(e)}")

finally:
    driver.quit()
    print("🏁 Processo finalizado.")
