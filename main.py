import telebot
from telebot import types

from telegram_bot.controller import Controller
from telegram_bot.exceptions import AlreadyChosenShop, ShopNotExist
import telegram_bot.config as cfg
from telegram_bot.keyboards import shop_keyboard, yes_no_keyborad, default_keyborad

#ник бота @SivalienShopBot
bot = telebot.TeleBot(cfg.TOKEN)
controller = Controller()


@bot.message_handler(commands=['start'])
def send_keyboard(message: types.Message, text: str = cfg.HELLO_MESSAGE) -> None:
    bot.send_message(message.chat.id, text=text, reply_markup=default_keyborad(), parse_mode="Markdown")
    if text == cfg.HELLO_MESSAGE:
        bot.send_photo(message.chat.id, photo='https://sun9-39.userapi.com/impf/c854216/v854216672/41eea/Ii_YZCmegiI.jpg?size=960x712&quality=96&sign=2bfc14c917d3f0e5130b2b891077e970&type=album')

@bot.message_handler(commands=['settings'])
def send_shop_keyboard(message: types.Message) -> None:
    message = bot.send_message(message.chat.id, text=cfg.CHANGE_SHOP, reply_markup=shop_keyboard(controller))
    bot.register_next_step_handler(message, select_shop_for_modifying)

def select_shop_for_modifying(message: types.Message) -> None:
    try:
        controller.select_shop(message.text)
        message = bot.send_message(message.chat.id, 'Введите число товаров, которое вы хотите установить:')
        bot.register_next_step_handler(message, get_item_number)
    except ShopNotExist:
        message = bot.send_message(
            message.chat.id,
            'Такого магазина я не знаю(\n Выберите один магазин из предложенных ниже:',
            reply_markup=shop_keyboard(controller)
        )
        bot.register_next_step_handler(message, select_shop_for_modifying)

def get_item_number(message: types.Message) -> None:
    try:
        controller.add_shop_item_number(message)
        bot.send_message(message.chat.id, 'Число товаров успешно изменено!')
        final_command(message)
    except ValueError:
        message = bot.send_message(message.chat.id, 'Число товаров должно быть натуральным числом.\nПопробуйте снова:')
        bot.register_next_step_handler(message, select_shop_for_modifying)

@bot.message_handler(content_types=['text'])
def callback(message: types.Message) -> None:
    if message.text == cfg.SEARCH_BUTTON:
        message = bot.send_message(
            message.chat.id, 
            cfg.CHOOSE_SHOP,
            reply_markup=shop_keyboard(controller, first=True),
        )
        bot.register_next_step_handler(message, select_shop, first=True)
    elif message.text == cfg.SHOW_ALL_BUTTON:
        show_all(message)
    else:
        send_keyboard(message, cfg.UNKNOWN_COMMAND)
        
def select_shop(message: types.Message, first=False) -> None:
    if message.text == cfg.ALL_SHOP_BUTTON:
        get_request(message, all_shops=True)
    else:
        try:
            controller.add_shop(message.text)
            if controller.available_shop_number == 0:
                get_request(message)
            else:
                message = bot.send_message(message.chat.id, 'Добавить еще магазин?', reply_markup=yes_no_keyborad())
                bot.register_next_step_handler(message, add_shop)
        except ShopNotExist:
            message = bot.send_message(
                message.chat.id,
                'Такого магазина я не знаю(\n Выберите один магазин из предложенных ниже:',
                reply_markup=shop_keyboard(controller, first=first)
            )
            bot.register_next_step_handler(message, select_shop)
        except AlreadyChosenShop:
            message = bot.send_message(
                message.chat.id,
                'Вы уже выбрали этот магазин.\n Выберите один магазин из предложенных ниже:',
                reply_markup=shop_keyboard(controller)
            )
            bot.register_next_step_handler(message, select_shop)

def add_shop(message: types.Message) -> None:
    if message.text == cfg.YES_BUTTON:
        message = bot.send_message(message.chat.id, cfg.CHOOSE_SHOP, reply_markup=shop_keyboard(controller))
        bot.register_next_step_handler(message, select_shop)
    elif message.text == cfg.NO_BUTTON:
        get_request(message)
    else:
        message = bot.send_message(message.chat.id, cfg.UNKNOWN_COMMAND, reply_markup=yes_no_keyborad())
        bot.register_next_step_handler(message, add_shop)

def get_request(message: types.Message, all_shops: bool = False):
    message = bot.send_message(message.chat.id, 'Введите название товара:', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, search_item, all_shops=all_shops)

def search_item(message: types.Message, all_shops: bool = False) -> None:
    bot.send_message(message.chat.id, 'Поиск может занять некоторое время...')
    items = controller.get_items(message, all_shops=all_shops)
    for shop in items:
        if items[shop] is None:
            bot.send_message(
                message.chat.id,
                f'В магазине {shop} нет товара {message.text}'
            )
        else:
            bot.send_message(
                message.chat.id,
                f'Товары из магазина {shop}'
            )
            for item in items[shop]:
                bot.send_photo(message.chat.id, item.image, caption=item.name + '\n' + item.price + '\n' + item.link)
    final_command(message)

def final_command(message: types.Message) -> None:
    send_keyboard(message, cfg.FINAL_COMMAND)

def show_all(message: types.Message) -> None:
    shops = controller.get_shop_item_number(message)
    text = '\n'.join([f'{i + 1}. {shop} (показывается {shops[shop]} товаров при поиске)' for (i, shop) in enumerate(controller.get_available_shops())])
    bot.send_message(message.chat.id, text)
    final_command(message)


if __name__=='__main__':
    bot.infinity_polling()
