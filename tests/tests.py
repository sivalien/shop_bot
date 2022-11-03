import pytest

from telegram_bot.models.item import Item
import telegram_bot.config as cfg
from telegram_bot.models.aliexpress import Aliexpress
from telegram_bot.models.lamoda import Lamoda
from telegram_bot.models.wildberries import Wildberries
from telegram_bot.exceptions import AlreadyChosenShop, ShopNotExist
from telegram_bot.models.shoplist import ShopList


aliexpress = Aliexpress()
lamoda = Lamoda()
wildberries = Wildberries()
shoplist = ShopList()
shops = [aliexpress, lamoda, wildberries]


def test_item():
    item = Item('link', 'name', 'price', 'image')
    assert item.link == 'link'
    assert item.name == 'name'
    assert item.price == 'price'
    assert item.image == 'image'

def test_shop():
    assert Aliexpress() is aliexpress
    assert Wildberries() is wildberries
    assert Lamoda() is lamoda

def test_shop_name():
    assert aliexpress.name == 'Aliexpress'
    assert lamoda.name == 'Lamoda'
    assert wildberries.name == 'Wildberries'

def test_shop_eq():
    assert aliexpress == 'Aliexpress'
    assert lamoda == 'Lamoda'
    assert wildberries == 'Wildberries'

def test_shop_hash():
    assert hash(aliexpress) == hash('Aliexpress')
    assert hash(lamoda) == hash('Lamoda')
    assert hash(wildberries) == hash('Wildberries')

def test_shop_get_items():
    for shop in shops:
        assert shop.get_items('fjsksgdjk') is None
        items = shop.get_items('футболка')
        assert isinstance(items, list) and isinstance(items[0], Item)

def test_controller():
    assert shoplist.shops == {Aliexpress(): True, Lamoda(): True, Wildberries(): True}
    assert shoplist.length == cfg.SHOP_NUMBER

def test_controller_available_shops():
    assert shoplist.get_available_shops() == ['Aliexpress', 'Lamoda', 'Wildberries']

def test_controller_add_one_shop():
    shoplist.add_shop('Aliexpress')
    assert shoplist.length == cfg.SHOP_NUMBER - 1
    assert shoplist.get_available_shops() == ['Lamoda', 'Wildberries']
    assert shoplist.shops == {Aliexpress(): False, Lamoda(): True, Wildberries(): True}

def test_controller_exceptions():
    with pytest.raises(ShopNotExist):
        shoplist.add_shop('Shop')
    with pytest.raises(AlreadyChosenShop):
        shoplist.add_shop('Aliexpress')

def test_controller_get_items():
    items = shoplist.get_items('футболка')
    assert len(items) == 1 and len(items['Aliexpress']) == 5

def test_controller_add_two_shops():
    shoplist.add_shop('Lamoda')
    shoplist.add_shop('Wildberries')
    assert shoplist.shops == {Aliexpress(): True, Lamoda(): False, Wildberries(): False}
    items = shoplist.get_items('футболка')
    assert len(items) == 2 and len(items['Lamoda']) == 5

def test_controller_add_all_shops():
    shoplist.add_shop('Aliexpress')
    shoplist.add_shop('Lamoda')
    shoplist.add_shop('Wildberries')
    assert shoplist.shops == {Aliexpress(): False, Lamoda(): False, Wildberries(): False}
    items = shoplist.get_items('футболка')
    assert len(items) == 3 and len(items['Lamoda']) == 2