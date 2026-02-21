import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def run():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Acessando Gofile...")
        driver.get("https://gofile.io/d/3JqmRC")
        time.sleep(15)
        
        # Pegamos apenas os IDs ou uma referência estável, para não dar erro de index
        items_count = len(driver.find_elements(By.CSS_SELECTOR, ".contentItem, a[href*='/d/']"))
        print(f"Sucesso! Encontrados {items_count} itens.")

        for i in range(items_count):
            try:
                # RE-LOCALIZA os itens a cada iteração para evitar o erro de index/stale
                current_items = driver.find_elements(By.CSS_SELECTOR, ".contentItem, a[href*='/d/']")
                if i >= len(current_items): break
                
                item = current_items[i]
                print(f"[{i+1}/{items_count}] Abrindo item...")
                
                driver.execute_script("arguments[0].click();", item)
                time.sleep(10) # Tempo maior para carregar o player

                # Busca por vídeo em toda a página, inclusive dentro de possíveis Shadow DOM ou apenas demora
                videos = driver.find_elements(By.TAG_NAME, "video")
                
                if len(videos) > 0:
                    print(" -> Vídeo detectado. Reproduzindo por 5 segundos...")
                    # Tenta dar play via JS caso esteja pausado
                    driver.execute_script("document.querySelector('video').play();")
                    time.sleep(5)
                else:
                    # Se não achou <video>, pode ser que o Gofile use um player customizado ou seja pasta
                    print(" -> Vídeo não detectado (pode ser pasta ou carregamento lento).")
                
                # Volta para a lista principal (Gofile aceita ESC ou clicar no botão voltar do site)
                # Vamos tentar ESC e depois garantir que voltamos ao link original se necessário
                ActionChains(driver).send_keys("\ue00c").perform() # ESC
                time.sleep(3)
                
                # Se o ESC não fechou o player, força a volta para o link principal
                if "gofile.io/d/" not in driver.current_url or len(driver.find_elements(By.TAG_NAME, "video")) > 0:
                    driver.get("https://gofile.io/d/3JqmRC")
                    time.sleep(5)

            except Exception as e:
                print(f"Erro no item {i+1}: {e}")
                driver.get("https://gofile.io/d/3JqmRC") # Reset preventivo
                time.sleep(5)
                continue

    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        print("Finalizando sessão.")
        driver.quit()

if __name__ == "__main__":
    run()
