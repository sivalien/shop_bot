import time
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from telegram_bot.models.shop import Shop, singleton
from telegram_bot.models.item import Item
import telegram_bot.config as cfg


@singleton
class Wildberries(Shop):
    def __init__(self) -> None:
        super().__init__('https://www.wildberries.ru/')

    def _get_source_page(self, request: str):
        driver = webdriver.Chrome(executable_path=cfg.CHROME_DRIVER_PATH)
        driver.get(self.link)
        search = driver.find_element(
            by=By.ID,
            value='searchInput',
        )
        time.sleep(2)
        search.click()
        search.send_keys(request)
        search.send_keys(Keys.ENTER)
        time.sleep(7)
        bs = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        return bs

    def get_items(self, request: str, number: int = 5) -> List[Item]:
        source_page = self._get_source_page(request)
        if source_page.find('div', {'id': 'emptySearchRecommendations'}) is None or not source_page.find('div', {'id': 'emptySearchRecommendations'}).text == "":
            return None
        product_cards = source_page.find_all('div', {'class': 'product-card__wrapper'})[:number]
        items = []
        for product in product_cards:
            price = product.find('ins', {'class': 'lower-price'}) or product.find('span', {'class': 'lower-price'})
            items.append(Item(
                link=product.find('a').get('href'),
                name=product.find('span', {'class': 'goods-name'}).text,
                price=price.text.strip(),
                image='https:' + product.find('img').get('src')
            ))
        return items

    