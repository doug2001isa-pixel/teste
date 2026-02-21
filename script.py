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
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv')
    
    try:
        print("Acessando Gofile...")
        driver.get("https://gofile.io/d/3JqmRC")
        time.sleep(15)
        
        # Localiza os itens iniciais
        items_elements = driver.find_elements(By.CSS_SELECTOR, ".contentItem, a[href*='/d/']")
        total_items = len(items_elements)
        print(f"Sucesso! Encontrados {total_items} itens na página.")

        for i in range(total_items):
            try:
                # Re-localiza os itens para evitar erro de referência (stale element)
                current_items = driver.find_elements(By.CSS_SELECTOR, ".contentItem, a[href*='/d/']")
                if i >= len(current_items):
                    break
                
                item = current_items[i]
                nome_ficheiro = item.text.lower()
                
                # FILTRO: Só clica se for extensão de vídeo
                if not any(ext in nome_ficheiro for ext in video_extensions):
                    continue

                print(f"[{i+1}/{total_items}] Abrindo vídeo: {nome_ficheiro.splitlines()[0]}")
                
                # Clique via JS
                driver.execute_script("arguments[0].click();", item)
                time.sleep(12) 

                # Busca por vídeo (inclusive dentro de iFrames)
                video_found = False
                videos = driver.find_elements(By.TAG_NAME, "video")
                
                if len(videos) > 0:
                    video_found = True
                else:
                    iframes = driver.find_elements(By.TAG_NAME, "iframe")
                    for iframe in iframes:
                        try:
                            driver.switch_to.frame(iframe)
                            if len(driver.find_elements(By.TAG_NAME, "video")) > 0:
                                video_found = True
                                break
                            driver.switch_to.default_content()
                        except:
                            driver.switch_to.default_content()

                if video_found:
                    print(" -> Tag <video> detectada! Reproduzindo por 5 segundos...")
                    driver.execute_script("document.querySelector('video').play();")
                    time.sleep(5)
                else:
                    print(" -> Vídeo não detectado no HTML, aguardando 5s de buffer...")
                    time.sleep(5)

                # Volta para a página principal
                driver.get("https://gofile.io/d/3JqmRC")
                time.sleep(8)
                driver.switch_to.default_content()

            except Exception as e_item:
                print(f"Erro ao processar item {i+1}: {e_item}")
                driver.get("https://gofile.io/d/3JqmRC")
                time.sleep(5)
                continue

    except Exception as e_fatal:
        print(f"Erro Crítico: {e_fatal}")
        driver.save_screenshot("erro_fatal.png")
    
    finally:
        print("Finalizando sessão.")
        driver.quit()

if __name__ == "__main__":
    run()
