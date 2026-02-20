import time
import undetected_chromedriver as uc # Importante: instale com 'pip install undetected-chromedriver'
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURAÇÕES ---
ROOT_URL = "https://gofile.io/d/3JqmRC"
ARQUIVO_SAIDA = "videos_processados.txt"

def explorar_gofile(driver, url, nivel=0):
    indent = "  " * nivel
    print(f"{indent}📂 Acessando: {url}")
    try:
        driver.get(url)
        # Espera o carregamento de um seletor específico que confirma a página
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='file']"))
            )
        except:
            print(f"{indent}⚠️ Conteúdo não carregou. Tirando print para depuração...")
            driver.save_screenshot(f"erro_pag_{nivel}.png")
            return

        # Scroll suave para garantir renderização
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Captura elementos
        botoes = driver.find_elements(By.XPATH, "//button[contains(., 'Play')]")
        print(f"{indent}🎥 Vídeos detectados: {len(botoes)}")

        # Processamento simplificado
        for i in range(len(botoes)):
            try:
                # Re-localiza para evitar erro de stale element
                btns = driver.find_elements(By.XPATH, "//button[contains(., 'Play')]")
                driver.execute_script("arguments[0].click();", btns[i])
                time.sleep(5) 
                
                with open(ARQUIVO_SAIDA, "a") as f:
                    f.write(f"OK: {url} - Video {i+1} - {time.ctime()}\n")
            except Exception as e:
                print(f"{indent}  ⚠️ Erro no vídeo {i+1}: {e}")

    except Exception as e:
        print(f"{indent}❌ Erro geral na pasta: {e}")

# --- INICIALIZAÇÃO ---
options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")

print("🚀 Iniciando Chrome (Modo Undetected)...")
driver = uc.Chrome(options=options)

try:
    explorar_gofile(driver, ROOT_URL)
finally:
    driver.quit()
    print("\n✅ Processo finalizado!")
