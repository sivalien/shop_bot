from telebot import types
import telebot

import telegram_bot.view.view as view
import telegram_bot.config as cfg
from telegram_bot.exceptions import ShopNotExist, AlreadyChosenShop
from telegram_bot.models.shoplist import ShopList


shoplist = ShopList()
bot = telebot.TeleBot(cfg.TOKEN)

def start_bot():
    bot.infinity_polling()

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    view.start(bot, message, first=True)

@bot.message_handler(commands=['settings'])
def select_action(message: types.Message) -> None:
    message = view.send_shop_keyboard(bot, message, shoplist.get_available_shops())
    bot.register_next_step_handler(message, select_shop_for_modifying)

def select_shop_for_modifying(message: types.Message) -> None:
    try:
        shoplist.select_shop(message.text)
        message = view.select_item_number(bot, message)
        bot.register_next_step_handler(message, get_item_number)
    except ShopNotExist:
        message = view.wrong_shop(bot, message, shoplist.get_available_shops())
        bot.register_next_step_handler(message, select_shop_for_modifying)

def get_item_number(message: types.Message) -> None:
    try:
        shoplist.add_shop_item_number(message)
        view.change_shop_number(bot, message)
    except ValueError:
        message = view.select_item_number(bot, message, error=True)
        bot.register_next_step_handler(message, get_item_number)

@bot.message_handler(content_types=['text'])
def callback(message: types.Message) -> None:
    if message.text == cfg.SEARCH_BUTTON:
        message = view.send_shop_keyboard(bot, message, shoplist.get_available_shops(), first=True)
        bot.register_next_step_handler(message, select_shop, first=True)
    elif message.text == cfg.SHOW_ALL_BUTTON:
        view.show_all(bot, message, shoplist.get_available_shops())
    else:
        view.unknown_command(bot, message)

def select_shop(message: types.Message, first=False) -> None:
    if message.text == cfg.ALL_SHOP_BUTTON:
        get_request(message, all_shops=True)
    else:
        try:
            shoplist.add_shop(message.text)
            if shoplist.available_shop_number == 0:
                get_request(message)
            else:
                message = view.add_shop(bot, message)
                bot.register_next_step_handler(message, add_shop)
        except ShopNotExist:
            message = view.wrong_shop(bot, message, shoplist.get_available_shops(), first=first)
            bot.register_next_step_handler(message, select_shop)
        except AlreadyChosenShop:
            message = view.wrong_shop(bot, message, shoplist.get_available_shops(), already_chosen=True)
            bot.register_next_step_handler(message, select_shop)

def add_shop(message: types.Message) -> None:
    if message.text == cfg.YES_BUTTON:
        message = view.send_shop_keyboard(bot, message, shoplist.get_available_shops())
        bot.register_next_step_handler(message, select_shop)
    elif message.text == cfg.NO_BUTTON:
        get_request(message)
    else:
        message = view.add_shop(bot, message, error=True)
        bot.register_next_step_handler(message, add_shop)

def get_request(message, all_shops: bool = False):
    bot.register_next_step_handler(view.enter_item_name(bot, message), search_items, all_shops)

def search_items(message, all_shops):
    items = shoplist.get_items(message.text, message.id, all_shops=all_shops)
    view.show_items(bot, message, items)