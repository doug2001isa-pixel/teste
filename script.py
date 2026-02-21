import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def run():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Necessário para rodar no GitHub Actions
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Acessando Gofile...")
        driver.get("https://gofile.io/d/3JqmRC")
        
        # Espera até que os itens da lista apareçam (timeout de 30 segundos)
        wait = WebDriverWait(driver, 30)
        
        try:
            # O Gofile costuma carregar itens com a classe 'contentItem'
            wait.until(EC.presence_of_element_located((By.CLASS_SET_NAME, "contentItem")))
        except:
            print("Aviso: Itens demoraram a aparecer ou layout mudou. Tirando print...")
            driver.save_screenshot("debug_layout.png")

        items = driver.find_elements(By.CLASS_NAME, "contentItem")
        print(f"Encontrados {len(items)} itens.")

        for i in range(len(items)):
            try:
                # Re-localiza os itens a cada loop para evitar StaleElementReferenceException
                current_items = driver.find_elements(By.CLASS_NAME, "contentItem")
                item = current_items[i]
                
                nome = item.text.split('\n')[0]
                print(f"[{i+1}/{len(items)}] Abrindo: {nome}")
                
                driver.execute_script("arguments[0].click();", item)
                time.sleep(5) # Espera carregar o conteúdo

                # Verifica se há tag <video> na página
                videos = driver.find_elements(By.TAG_NAME, "video")
                if len(videos) > 0:
                    print(" -> Vídeo detectado. Reproduzindo por 5 segundos...")
                    time.sleep(5)
                
                # Tenta voltar ou fechar o modal (pressionando ESC)
                webdriver.ActionChains(driver).send_keys("\ue00c").perform() # ESC key
                time.sleep(2)
                
            except Exception as e:
                print(f"Erro ao processar item {i}: {e}")
                continue

    except Exception as e:
        print(f"Erro fatal: {e}")
        driver.save_screenshot("erro_fatal.png")
    finally:
        print("Finalizando...")
        driver.quit()

if __name__ == "__main__":
    run()
