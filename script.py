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
        
        # Localiza todos os itens na página
        all_items = driver.find_elements(By.CSS_SELECTOR, ".contentItem, a[href*='/d/']")
        total_items = len(all_items)
        print(f"Total de itens encontrados na página: {total_items}")

        for i in range(total_items):
            try:
                # Re-localiza os itens para evitar erro de referência
                current_items = driver.find_elements(By.CSS_SELECTOR, ".contentItem, a[href*='/d/']")
                if i >= len(current_items): break
                
                item = current_items[i]
                nome_ficheiro = item.text.lower()
