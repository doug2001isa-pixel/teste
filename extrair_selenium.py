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
    except: return 144

options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Camuflagem extra
options.add_argument("--disable-blink-features=AutomationControlled")

chrome_ver = get_chrome_version()
driver = uc.Chrome(options=options, version_main=chrome_ver)

try:
    url = "https://gofile.io/d/3JqmRC"
    print(f"🚀 Acessando: {url}")
    driver.get(url)
    
    # Espera o carregamento básico do corpo da página
    time.sleep(20) 
    
    # Salva o print para você ver se tem CAPTCHA
    driver.save_screenshot("debug_screen.png")
    
    # Tenta pegar qualquer link que contenha o padrão de download do GoFile
    links = driver.find_elements(By.XPATH, "//a[contains(@href, 'gofile.io/download')]")
    
    print(f"📄 Título da página: {driver.title}")
    print(f"🔗 Links de download encontrados: {len(links)}")

    with open("videos_processados.txt", "w") as f:
        f.write(f"Execucao: {time.ctime()}\n")
        f.write(f"HTML Length: {len(driver.page_source)}\n")
        for l in links:
            f.write(f"Link: {l.get_attribute('href')}\n")

except Exception as e:
    print(f"❌ Erro: {e}")
    driver.save_screenshot("debug_screen.png")
finally:
    driver.quit()
    print("🏁 Processo finalizado.")
