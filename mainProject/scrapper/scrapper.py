from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
import time
from bs4 import BeautifulSoup
import json

class coin_market_scrapper:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def __init__(self, coin_name, driver_path=None):
        self.coin_name = coin_name.lower().replace(' ', '-')
        self.url = f"{self.BASE_URL}{self.coin_name}/"
        self.driver = self._init_firefox_driver()


    def _init_driver(self):
        # service = Service(self.driver_path)
        chrome_options = chromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usuage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def _init_firefox_driver(self):
        # service = Service(self.driver_path)
        firefox_options = firefoxOptions()
        firefox_options.add_argument("-headless")
        firefox_options.add_argument("-incognito")
        firefox_options.add_argument("-no-sandbox")
        firefox_options.add_argument("-disable-dev-shm-usuage")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
        return driver

    def fetch_html(self):
        self.driver.get(self.url)
        time.sleep(0.1) 
        html = self.driver.page_source
        self.driver.quit()
        return html

    def extract_coin_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        coin_name = soup.find('span', {'data-role': 'coin-name'}).text.strip().split(' ')[0]
        coin_symbol = soup.find('span', {'data-role': 'coin-symbol'}).text.strip()
        current_price = soup.find('span', {'class': 'sc-d1ede7e3-0 fsQm base-text'}).text.strip()

        market_cap_section = soup.find('div', {'id': 'section-coin-stats'})
        stats = market_cap_section.find_all('dd', {'class': 'base-text'})
        market_cap = stats[0].text.strip().split("%")[1]
        volume_24h = stats[1].text.strip().split("%")[1]
        volume_by_market_cap = stats[2].text.strip()
        circulating_supply = stats[3].text.strip()
        total_supply = stats[4].text.strip()
        max_supply = stats[5].text.strip()
        fully_diluted_market_cap = stats[6].text.strip()
        change_in_volume = stats[1].text.strip().split('$')[0]
        change_in_market_cap = stats[0].text.strip().split('$')[0]

        ranking = soup.findAll("span", {"class": "text slider-value rank-value"})
        ranking_by_volume = ranking[0].text.strip() or ""
        ranking_by_market_cap = ranking[1].text.strip() or ""

        links_section = soup.findAll('div', {"data-role": "body"})[1]
        official_links = [a['href'] for a in links_section.find_all('a', {'rel': 'nofollow noopener'})]

        return {
            'coin_name': coin_name,
            'coin_symbol': coin_symbol,
            'current_price': current_price,
            'market_cap': market_cap,
            'volume_24h': volume_24h,
            'volume_by_market_cap': volume_by_market_cap,
            'circulating_supply': circulating_supply,
            'total_supply': total_supply,
            'max_supply': max_supply,
            'fully_diluted_market_cap': fully_diluted_market_cap,
            'change_in_volume': change_in_volume,
            'change_in_market_cap': change_in_market_cap,
            'ranking_by_volume': ranking_by_volume,
            'ranking_by_market_cap': ranking_by_market_cap,
            'official_links': official_links
        }

    def get_coin_data(self):
        html = self.fetch_html()
        coin_data = self.extract_coin_data(html)
        return coin_data

    def get_coin_data_as_json(self):
        coin_data = self.get_coin_data()
        return json.dumps(coin_data, indent=4)

if ( __name__ == "__main__" ) :
    coin_name = "bitcoin"
    scraper = coin_market_scrapper(coin_name)
    coin_data_json = scraper.get_coin_data_as_json()
    print(coin_data_json)
