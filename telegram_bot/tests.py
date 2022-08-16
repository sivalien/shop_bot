import pytest

from models.item import Item
import config as cfg
from models.aliexpress import Aliexpress
from models.lamoda import Lamoda
from models.wildberries import Wildberries
from exceptions import AlreadyChosenShop, ShopNotExist
from controller import Controller


aliexpress = Aliexpress()
lamoda = Lamoda()
wildberries = Wildberries()
controller = Controller()
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
    assert controller.shops == {Aliexpress(): True, Lamoda(): True, Wildberries(): True}
    assert controller.length == cfg.SHOP_NUMBER

def test_controller_available_shops():
    assert controller.get_available_shops() == ['Aliexpress', 'Lamoda', 'Wildberries']

def test_controller_add_one_shop():
    controller.add_shop('Aliexpress')
    assert controller.length == cfg.SHOP_NUMBER - 1
    assert controller.get_available_shops() == ['Lamoda', 'Wildberries']
    assert controller.shops == {Aliexpress(): False, Lamoda(): True, Wildberries(): True}

def test_controller_exceptions():
    with pytest.raises(ShopNotExist):
        controller.add_shop('Shop')
    with pytest.raises(AlreadyChosenShop):
        controller.add_shop('Aliexpress')

def test_controller_get_items():
    items = controller.get_items('футболка')
    assert len(items) == 1 and len(items['Aliexpress']) == 5

def test_controller_add_two_shops():
    controller.add_shop('Lamoda')
    controller.add_shop('Wildberries')
    assert controller.length == cfg.SHOP_NUMBER - 2
    assert controller.shops == {Aliexpress(): True, Lamoda(): False, Wildberries(): False}
    items = controller.get_items('футболка')
    assert len(items) == 2 and len(items['Lamoda']) == 5

def test_controller_add_all_shops():
    controller.add_shop('Aliexpress')
    controller.add_shop('Lamoda')
    controller.add_shop('Wildberries')
    assert controller.length == 0
    assert controller.shops == {Aliexpress(): False, Lamoda(): False, Wildberries(): False}
    items = controller.get_items('футболка')
    assert len(items) == 3 and len(items['Lamoda']) == 2