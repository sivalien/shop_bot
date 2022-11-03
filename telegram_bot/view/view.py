from telebot import types

import telegram_bot.config as cfg
from telegram_bot.view.keyboards import default_keyborad, shop_keyboard, yes_no_keyborad


def start(bot, message: types.Message, first=False) -> None:
    text = cfg.HELLO_MESSAGE if first else cfg.FINAL_COMMAND
    bot.send_message(message.chat.id, text=text, reply_markup=default_keyborad(), parse_mode="Markdown")
    if first:
        bot.send_photo(message.chat.id, photo='https://sun9-39.userapi.com/impf/c854216/v854216672/41eea/Ii_YZCmegiI.jpg?size=960x712&quality=96&sign=2bfc14c917d3f0e5130b2b891077e970&type=album')

def send_shop_keyboard(bot, message, available_shops, first: bool = False) -> types.Message:
    return bot.send_message(message.chat.id, text="Выберите магазин", reply_markup=shop_keyboard(available_shops, first))

def select_item_number(bot, message, error: bool = False):
    return bot.send_message(message.chat.id, 'Число товаров должно быть натуральным.\nПопробуйте снова:' if error else 'Введите число товаров, которое вы хотите установить:', reply_markup=types.ReplyKeyboardRemove())

def wrong_shop(bot, message, shops, already_chosen: bool = False, first: bool = False):
    text = 'Такого магазина я не знаю(\n Выберите один магазин из предложенных ниже:' if not already_chosen else 'Вы уже выбрали этот магазин.\n Выберите один магазин из предложенных ниже:'
    return bot.send_message(
            message.chat.id,
            text,
            reply_markup=shop_keyboard(shops, first=first)
        )

def change_shop_number(bot, message):
    bot.send_message(message.chat.id, 'Число товаров успешно изменено!')
    start(bot, message)

def show_all(bot, message, shops) -> None:
    text = '\n'.join([f'{i + 1}. {shop}' for (i, shop) in enumerate(shops)])
    bot.send_message(message.chat.id, text)
    start(bot, message)

def unknown_command(bot, message) -> None:
    bot.send_message(message.chat.id, cfg.UNKNOWN_COMMAND, reply_markup=default_keyborad())

def add_shop(bot, message, error: bool = False) -> None:
    return bot.send_message(message.chat.id, cfg.UNKNOWN_COMMAND if error else 'Добавить еще магазин?', reply_markup=yes_no_keyborad())

def enter_item_name(bot, message):
    return bot.send_message(message.chat.id, 'Введите название товара:', reply_markup=types.ReplyKeyboardRemove())

def show_items(bot, message, items):
    for shop in items:
        if items[shop] is None:
            bot.send_message(
                message.chat.id,
                f'В магазине {shop} нет товара \"{message.text}\"'
            )
        else:
            bot.send_message(
                message.chat.id,
                f'Товары из магазина {shop}'
            )
            for item in items[shop]:
                bot.send_photo(message.chat.id, item.image, caption=item.name + '\n' + item.price + '\n' + item.link)
    start(bot, message)