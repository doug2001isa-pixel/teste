import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Tenta camuflar o uso de automação
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Acessando Gofile...")
        driver.get("https://gofile.io/d/3JqmRC")
        
        # Espera forçada para garantir que o JS do Gofile processe a página
        time.sleep(15)
        
        # Tenta múltiplos seletores: a classe comum, ou qualquer link que contenha /d/
        items = driver.find_elements(By.CSS_SELECTOR, ".contentItem, a[href*='/d/']")
        
        if len(items) == 0:
            print("Nenhum item encontrado pelos seletores padrão. Verificando estrutura...")
            driver.save_screenshot("layout_atual.png")
            # Tenta pegar todos os links da página para debug
            links = driver.find_elements(By.TAG_NAME, "a")
            print(f"Total de links na página: {len(links)}")
            return

        print(f"Sucesso! Encontrados {len(items)} itens.")

        for i in range(len(items)):
            try:
                # Recarrega a lista para evitar elementos obsoletos
                current_items = driver.find_elements(By.CSS_SELECTOR, ".contentItem, a[href*='/d/']")
                item = current_items[i]
                
                nome = item.text.split('\n')[0] if item.text else f"Item {i+1}"
                print(f"[{i+1}/{len(items)}] Abrindo: {nome}")
                
                # Clique via JavaScript para ignorar sobreposições
                driver.execute_script("arguments[0].click();", item)
                time.sleep(8) # Espera o carregamento do player

                # Procura por vídeo
                video_elements = driver.find_elements(By.TAG_NAME, "video")
                if len(video_elements) > 0:
                    print(" -> Vídeo detectado. 'Assistindo' por 5 segundos...")
                    time.sleep(5)
                else:
                    print(" -> Não detectado como vídeo direto.")
                
                # Pressiona ESC para fechar modal ou voltar
                webdriver.ActionChains(driver).send_keys("\ue00c").perform()
                time.sleep(2)

            except Exception as e:
                print(f"Erro ao processar item: {e}")
                continue

    except Exception as e:
        print(f"Erro Crítico: {e}")
        driver.save_screenshot("erro_fatal.png")
    finally:
        print("Finalizando sessão.")
        driver.quit()

if __name__ == "__main__":
    run()
