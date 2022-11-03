from collections import OrderedDict, defaultdict
from typing import DefaultDict, List

from telegram_bot.models.aliexpress import Aliexpress
from telegram_bot.models.lamoda import Lamoda
from telegram_bot.models.wildberries import Wildberries
import telegram_bot.config as cfg
from telegram_bot.exceptions import AlreadyChosenShop, ShopNotExist
from telegram_bot.models.database import Database


class ShopList:
    def __init__(self) -> None:
        self.shops = OrderedDict({
            Aliexpress(): True,
            Lamoda(): True,
            Wildberries(): True,
        })
        self.available_shop_number = cfg.SHOP_NUMBER
        self.chosen_shop = None
        self.db = Database()

    def add_shop(self, name: str) -> bool:
        if name not in self.shops:
            raise ShopNotExist
        if not self.shops[name]:
            raise AlreadyChosenShop
        self.shops[name] = False
        self.available_shop_number -= 1
        return self.available_shop_number == 0

    def get_available_shops(self) -> List[str]:
        res = []
        for shop in self.shops:
            if self.shops[shop]:
                res.append(shop.name)
        return res

    def get_items(self, request, id, all_shops: bool = False):
        res = {}
        numbers = defaultdict(lambda: 2 if all_shops else 5, self.db.get_shop_item_numbers(id=id))
        for shop in self.shops:
            if all_shops or not self.shops[shop]:
                res[shop.name] = shop.get_items(request=request, number=numbers[shop])
                self.shops[shop] = True
        self.available_shop_number = cfg.SHOP_NUMBER
        return res

    def select_shop(self, shop: str) -> None:
        if shop not in self.shops:
            raise ShopNotExist
        self.chosen_shop = shop

    def get_shop_item_number(self, id, all_shops: bool = False) -> DefaultDict[str, int]:
        return defaultdict(lambda: 2 if all_shops else 5, self.db.get_shop_item_numbers(id))

    def add_shop_item_number(self, message) -> None:
        if int(message.text) <= 0:
            raise ValueError
        self.db.add(message.chat.id, self.chosen_shop, int(message.text))