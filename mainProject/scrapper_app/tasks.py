from celery import shared_task 
from scrapper.scrapper import coin_market_scrapper
@shared_task(bind=True)
def scrapping_task(self , coin_name):
    scraper = coin_market_scrapper(coin_name)
    coin_data_json = scraper.get_coin_data_as_json()
    return coin_data_json


