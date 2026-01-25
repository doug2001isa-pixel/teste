import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# --- CONFIGURAÇÕES ---
# O GitHub pegará o Token do "Secret" que você cadastrará lá
TOKEN = os.getenv("GOFILE_TOKEN") 
ROOT_URL = "https://gofile.io/d/3JqmRC"
ARQUIVO_SAIDA = "links_gofile_profundo.txt"
ARQUIVO_HISTORICO = "historico_pastas.txt"

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r") as f:
            return set(line.strip() for line in f)
    return set()

def salvar_no_historico(url):
    with open(ARQUIVO_HISTORICO, "a") as f:
        f.write(url + "\n")

def extrair_conteudo_recursivo(driver, url, historico, nivel=0):
    if url in historico:
        print(f"{'  ' * nivel}⏭️ Pulando (já processada): {url}")
        return

    indent = "  " * nivel
    print(f"{indent}📂 Acessando: {url}")
    
    try:
        driver.get(url)
        # Injeta o cookie de login em cada nova navegação se houver TOKEN
        if TOKEN:
            driver.add_cookie({"name": "accountToken", "value": TOKEN})
        
        time.sleep(10) # Tempo maior para o servidor do GitHub carregar
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        links_da_pagina = driver.find_elements(By.TAG_NAME, "a")
        
        pastas_para_visitar = []
        arquivos_encontrados = []

        for el in links_da_pagina:
            href = el.get_attribute("href")
            nome = el.text.strip() or "Item_Sem_Nome"
            
            if href:
                if "gofile.io/d/" in href and href != url and href != ROOT_URL:
                    if href not in [p[1] for p in pastas_para_visitar]:
                        pastas_para_visitar.append((nome, href))
                elif "/contents/" in href or "download" in href.lower() or "/v/" in href:
                    if href not in [a[1] for a in arquivos_encontrados]:
                        arquivos_encontrados.append((nome, href))

        if arquivos_encontrados:
            with open(ARQUIVO_SAIDA, "a", encoding="utf-8") as f:
                for nome, link in arquivos_encontrados:
                    f.write(f"{indent}[ARQUIVO] {nome} -> {link}\n")
                    print(f"{indent}  📄 Arquivo: {nome}")

        salvar_no_historico(url)

        for nome_p, link_p in pastas_para_visitar:
            with open(ARQUIVO_SAIDA, "a", encoding="utf-8") as f:
                f.write(f"\n{indent}[PASTA] {nome_p} -> {link_p}\n")
            extrair_conteudo_recursivo(driver, link_p, historico, nivel + 1)

    except Exception as e:
        print(f"{indent}❌ Erro em {url}: {e}")

# --- EXECUÇÃO (OTIMIZADA PARA GITHUB) ---
chrome_options = Options()
chrome_options.add_argument("--headless") # Obrigatório no GitHub
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    historico = carregar_historico()
    if not os.path.exists(ARQUIVO_SAIDA):
        with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
            f.write(f"--- RELATÓRIO GOFILE GITHUB ACTIONS ---\n\n")
    
    # Inicia a recursão
    extrair_conteudo_recursivo(driver, ROOT_URL, historico)
    print("\n✨ Varredura automatizada concluída!")

except Exception as e:
    print(f"💥 Erro fatal: {e}")
finally:
    driver.quit()
