import time
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from telegram_bot.models.item import Item
from telegram_bot.models.shop import Shop, singleton
import telegram_bot.config as cfg


@singleton
class Lamoda(Shop):
    def __init__(self) -> None:
        super().__init__('https://www.lamoda.ru')

    def _get_source_page(self, request: str):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage') 
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(self.link)
        button = driver.find_element(by=By.XPATH, value='//*[@id="vue-root"]/div/div[1]/header/div[3]/div/div/div/div/button')
        button.click()
        search = driver.find_element(by=By.CLASS_NAME, value='_3jotUx9G5izzdWD5DIoPVO')
        search.click()
        search.send_keys(request)
        search.send_keys(Keys.ENTER)
        time.sleep(1)
        bs = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        return bs
    
    def get_items(self, request: str, number: int = 5):
        source_page = self._get_source_page(request)
        if source_page.find('title').text.strip() == 'Поиск не дал результатов':
            return None
        products = source_page.find_all('div', {'class': 'x-product-card__card'})[:number]
        items = []
        for product in products:
            items.append(Item(
                link=self.link + product.find('a').get('href'),
                name=product.find('div', {'class': 'x-product-card-description__product-name'}).text,
                price=product.find_all('span')[-3].text,
                image='https:' + product.find('img').get('src')
            ))
        return items