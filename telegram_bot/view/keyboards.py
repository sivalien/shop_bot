from telebot import types

from telegram_bot.controller import Controller
import telegram_bot.config as cfg

def shop_keyboard(controller: Controller, first: bool = False) -> types.ReplyKeyboardMarkup:
    shops = controller.get_available_shops()
    markup = types.ReplyKeyboardMarkup()
    for shop in shops:
        markup.row(types.KeyboardButton(shop))
    if first:
        markup.row('Все магазины')
    return markup

def yes_no_keyborad() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup()
    markup.row(
        types.KeyboardButton(cfg.YES_BUTTON),
        types.KeyboardButton(cfg.NO_BUTTON)
    )
    return markup

def default_keyborad() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton(cfg.SEARCH_BUTTON))
    markup.row(types.KeyboardButton(cfg.SHOW_ALL_BUTTON))
    return markup