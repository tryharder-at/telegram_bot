from random import choice, shuffle
from itertools import cycle

import pymorphy2

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, \
    CallbackContext
from settings import TOKEN
import logging


places = {'спорт': ['стадион', 'дворец спорта', 'тренажёрный зал', 'бассейн'],
          'культура': ['театр', 'музей', 'библиотека', 'дом культуры'],
          'развлечения': ['клуб', 'кино', 'сауна', 'бар', 'караоке', 'квесты', 'боулинг', 'бильярдный зал',
                          'спортивно-тактические клубы'],
          'медицина': ['больница', 'поликлиника', 'стоматология', 'травмпункт'],
          'медтовары': ['аптека', 'медтовары'],
          'животные': ['Товары для животных', 'ветеренарная клиника'],
          'питание': ['кафе', 'ресторан', 'макдональдс', 'kfc', 'столовая', 'пиццерия', 'суши бар', 'банкетный зал'],
          'религия': ['православный храм', 'мечеть', 'собор'],
          'магазины': ['торговый центр', 'спорттовары', 'магазин одежды', 'детский магазин', 'канцтовары',
                       'книжный магазин'],
          'автосервис': ['штрафстоянка', 'шиномонтаж', 'заправка', 'автомойка', 'авторемонт', 'стоянка', 'автохимия',
                         'шины, диски'],
          'туризм': ['гостиница', 'хостел', 'отель', 'база отдыха', 'авиабилеты', 'железнодорожные билеты'],
          'прогулка': ['парк', 'сквер', 'экскурсии', 'достопримечательность', 'отдых'],
          }

reply_keyboard = [['Развлечения', 'Питание'],
                  ['Спорт', 'Религия', 'Туризм'],
                  ['Культура', 'Магазины'],
                  ['Автосервис', 'Медтовары', 'Медицина'],
                  ['Животные', 'Прогулка'],
                  ['Погода'],
                  ['Сменить город'],
                  ['Главное меню'],
                  ]
# inline_kb_menu=InlineKeyboardMarkup([[InlineKeyboardButton( ['Главное меню'], callback_data='on_menu')]])

inline_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Следующее место', callback_data=1)]])

inline_keyboard_1 = InlineKeyboardMarkup([[InlineKeyboardButton('Следующий день', callback_data=2)]])

inline_keyboard_2 = InlineKeyboardMarkup([[InlineKeyboardButton('Следующий день', callback_data=2)],
                                          [InlineKeyboardButton('Предыдущий день', callback_data=3)]])


# Stages
FIRST, SECOND = range(2)


def start(update, context):
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("Guide", callback_data='on_guide'),
         InlineKeyboardButton("Traffic", callback_data='on_traffic')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Привет! Выберите действие!",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def guide(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Какой город тебя интересует?",

    )
    return 1


def town(update, context: CallbackContext) -> int:
    pass


def interests(update, context):
    global location

    message = update.message.text.lower()

    if message == 'сменить город':
        return 1
    elif message=='главное меню':
        keyboard = [
            [InlineKeyboardButton("Guide", callback_data='on_guide'),
             InlineKeyboardButton("Traffic", callback_data='on_traffic')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        update.message.reply_text(
            "Привет! Выберите действие!",
            reply_markup=reply_markup
        )
        # Tell ConversationHandler that we're in state `FIRST` now
        return FIRST

    elif message == 'погода':
        pass

    elif message in places:
        update.message.reply_text("Начинаю поиск...")

        _1 = 8  # choice(range(3, len(places[message]+1)))

        datas = []
        _text = []

        random_places = []

        for _ in range(len(places[message]), 0, -1):
            random_place = choice(places[message])
            while True:
                if random_place not in random_places:
                    break
                random_place = choice(places[message])

           # result = search(context.user_data['locality'], random_place, _1)
           # # print('Результат поиска: ', result)
           # for _ in result:
           #     data = _[0]
           #     coord = _[1]
           #
           #     if data not in datas:
           #         static_api_request = "http://static-maps.yandex.ru/1.x/?ll={}&l=map&z=15&pt={},pm2blywm1".format(
           #             coord, coord)
           #         # print('Информация прошла проверку: ', data)
           #         _text.append('[Картинка.]({})\n{} ({})'.format(static_api_request, data, random_place))
           #         datas.append(data)

        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        shuffle(_text)

        _text = cycle(_text)
        _return = update.message.reply_text(next(_text), reply_markup=inline_keyboard)
        location[_return.message_id] = _text
        update.message.reply_text("Выберите сферу которая вас интересует", reply_markup=markup)

        return 2

    else:
        return 2


def change_places(update, context):
    global location

    query = update.callback_query
    bot = context.bot

    if query.data == '1':
        mes = next(location[query.message.message_id])
        print(mes)
        bot.edit_message_text(text=mes,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id, parse_mode='markdown',
                              reply_markup=inline_keyboard)

    elif query.data == '2':
        pass



    elif query.data == '3':
        pass

    return 2


def traff_inf(update, context):
    query = update.callback_query
    bot = context.bot

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Если захочешь узнать про пробки, то набери\n"
             "{АДРЕС1}:{АДРЕС2}\n"
             "или\n"
             "{АДРЕС}\n",

    )
    return 3


def traffic(update: Update, context: CallbackContext):
    pass

    # Create the Updater and pass it your bot's token.


def start_over(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Guide", callback_data='on_guide'),
         InlineKeyboardButton("Traffic", callback_data='on_traffic')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Привет! Выберите действие!",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(guide, pattern='on_guide'),
                    CallbackQueryHandler(traff_inf, pattern='on_traffic'),
                    ],
            1: [MessageHandler(Filters.text & ~(Filters.command), town, pass_user_data=True)],
            2: [MessageHandler(Filters.text & ~(Filters.command), interests,
                               pass_user_data=True),
                CallbackQueryHandler(change_places, pass_user_data=True),
                # CallbackQueryHandler(start_over, pattern='on_menu'),

                ],
            3: [MessageHandler(Filters.text & ~(Filters.command), traffic,
                               pass_user_data=True), ]

        },
        fallbacks=[CommandHandler('start', start)]
    )
    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()