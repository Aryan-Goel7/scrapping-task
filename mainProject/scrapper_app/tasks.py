from celery import shared_task 
import time
from scrapper.scrapper import coin_market_scrapper
@shared_task(bind=True)
def scrapping_task(self , coins):
    coins_data = []
    for coin in coins : 
        time.sleep(0.5)
        scraper = coin_market_scrapper(coin)
        coin_data = scraper.get_coin_data()
        coins_data.append(coin_data)
    return coins_data


