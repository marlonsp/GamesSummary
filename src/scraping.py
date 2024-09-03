from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import sys

def scraping_games(n_pages=417):
    # Configurar opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar o Chrome em modo headless (sem interface gráfica)

    # Configurar o driver do Chrome
    driver = webdriver.Chrome(options=chrome_options)

    # Definir o número total de páginas
    total_pages = n_pages

    # Inicializar a lista para armazenar todos os hrefs
    all_hrefs = []

    # Loop para percorrer todas as páginas
    for page in range(1, total_pages + 1):
        # URL da página que você deseja extrair os dados
        url = f'https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2024&page={page}'

        # Abrir a página
        driver.get(url)
        print(f"Scraping page {page}...")
        # Esperar um pouco para garantir que o conteúdo seja carregado
        time.sleep(3)

        # Encontrar todos os elementos <div> com a classe específica
        divs = driver.find_elements(By.CSS_SELECTOR, 'div.c-finderProductCard.c-finderProductCard-game')

        # Extrair os hrefs dos links dentro dos elementos <div>
        hrefs = [div.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for div in divs if div.find_element(By.CSS_SELECTOR, 'a')]

        # Adicionar os hrefs extraídos à lista geral
        all_hrefs.extend(hrefs)
        if page % 10 == 0:
            print(f"Page {page} done")

    # Fechar o driver
    driver.quit()

    # Configuração do ChromeDriver com modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless (sem interface gráfica)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    def scrape_data(href_list):
        data = []
        cookie_done = False
        
        counter = 0
        for href in href_list:
            driver.get(href)
            
            if not cookie_done:
                # Tenta aceitar cookies se o botão estiver presente (executa uma única vez por driver)
                try:
                    reject_cookies_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
                    )
                    reject_cookies_button.click()
                    cookie_done = True
                except Exception as e:
                    print("Botão de rejeição de cookies não encontrado ou erro ao clicar:", e)
            
            # Espera o botão "Read More" estar presente e clica nele
            try:
                try:
                    read_more_button = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.c-productDetails_readMore"))
                    )
                    read_more_button.click()
                except:
                    pass

                # Espera o conteúdo ser carregado após clicar no botão
                WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.c-productionDetailsGame_description"))
                )
                
                # Coleta os dados da página
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                game_name = soup.find('h1').text.strip()
                description_span = soup.find('span', class_='c-productionDetailsGame_description')
                description = description_span.text.strip() if description_span else "No description available"

                data.append({
                    'game_name': game_name,
                    'url': href,
                    'description': description
                })

            except Exception as e:
                print(f"Error scraping {href}: {e}")

            counter += 1
            if counter % 100 == 0:
                print(f"{counter} games done")
        return pd.DataFrame(data)

    # Executar a função de raspagem
    df = scrape_data(all_hrefs)

    # Salvar o DataFrame em um arquivo CSV
    df.to_csv(f'../data/games_data_{n_pages}.csv', index=False)

    # Fechar o WebDriver
    driver.quit()

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: python scraping.py <n_pages> (max: 557, default: 417)")
        sys.exit(1)
    # receber o número de páginas como argumento
    n_pages_input = sys.argv[1]
    try:
        n_pages = int(n_pages_input)
    except ValueError:
        print("Invalid number of pages")
        sys.exit(1)
    scraping_games(n_pages)