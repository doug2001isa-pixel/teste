import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações do Navegador
options = uc.ChromeOptions()
options.add_argument("--headless=new") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# User-agent real para evitar bloqueios de IP de data center
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

print("🚀 Iniciando navegador...")
driver = uc.Chrome(options=options)

try:
    url = "https://gofile.io/d/3JqmRC"
    driver.get(url)
    
    # Espera até 20 segundos para encontrar um elemento de arquivo ou pasta
    print(f"⏳ Aguardando conteúdo de: {url}")
    wait = WebDriverWait(driver, 20)
    
    # O GoFile costuma usar IDs ou classes que começam com 'file' ou 'content'
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "file_Name")))
    
    print("✅ Página carregada com sucesso!")
    print("Título:", driver.title)
    
    # Exemplo: Listar nomes dos arquivos encontrados
    arquivos = driver.find_elements(By.CLASS_NAME, "file_Name")
    for arq in arquivos:
        print(f"📄 Arquivo encontrado: {arq.text}")

except Exception as e:
    print(f"❌ Erro durante a execução: {e}")
    # Tira um print para você ver o que o bot está vendo (ajuda muito no debug)
    driver.save_screenshot("debug_screen.png")

finally:
    driver.quit()
    print("🏁 Processo finalizado.")
