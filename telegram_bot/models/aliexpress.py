from typing import List
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from telegram_bot.models.item import Item
from telegram_bot.models.shop import Shop, singleton
import telegram_bot.config as cfg


@singleton
class Aliexpress(Shop):
    def __init__(self) -> None:
        super().__init__('https://aliexpress.ru')

    def _get_source_page(self, request: str):
        driver = webdriver.Chrome(cfg.CHROME_DRIVER_PATH)
        driver.get(self.link)
        search = driver.find_element(by=By.NAME, value='SearchText')
        search.click()
        search.send_keys(request)
        search.send_keys(Keys.ENTER)
        bs = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        return bs
    
    def get_items(self, request: str, number: int = 5):
        source_page = self._get_source_page(request)
        if source_page.find('div', {'class': "SearchWrap_SearchError__error__oy8dw"}) is not None:
            return None
        if source_page.find('p', {'class': 'ali-kit_Base__base__104pa1 ali-kit_Base__default__104pa1 ali-kit_Paragraph__paragraph__1w2ua6 ali-kit_Paragraph__size-s__1w2ua6 SpellCheckerNotification_SpellCheckerNotification__wordsWrap__10t57'}) is not None:
            return None
        refs = source_page.find_all('a', {'class': 'product-snippet_ProductSnippet__galleryBlock__tusfnx'})[:number]
        prices = source_page.find_all('div', {'class': 'snow-price_SnowPrice__mainM__1ehyuw'})[:number]
        res = []
        for i in range(number):
            response = requests.get(self.link + refs[i].get('href'))
            res.append(Item(
                link=self.link + refs[i].get('href'),
                name=BeautifulSoup(response.content, 'html.parser').find('h1').text,
                price=prices[i].text,
                image='https:' + refs[i].find('img').get('src')
            ))

        return res