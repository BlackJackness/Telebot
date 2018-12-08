import telebot
import config
import requests
from time import sleep
import help_description
from io import BytesIO
from PIL import Image

bot = telebot.TeleBot(token=config.token)


def form_query(names, values):
    query = ''
    for name, value in zip(names, values):
        query += f'{name}={value}&'
    return query[:-1]


@bot.message_handler(commands=['start'])
def start_message(msg):
    fname = msg.chat.first_name
    bot.reply_to(msg, f'Welcome, {fname}.How can I help you?')


@bot.message_handler(commands=['сделки', 'сд', 't', 'trade'])
def view_trade(msg):
    args = msg.text.split(" ")
    sell_coin = args[1].upper()
    buy_coin = args[2].upper()
    exchange = args[3]
    if len(args) == 4:
        limit = 10
    else:
        limit = args[4]
    r = requests.get(f'http://127.0.0.1:5000/last_trades/{exchange}/{sell_coin}_{buy_coin}?limit={limit}')
    if int(r.status_code) != 200:
        bot.reply_to(msg, f'{sell_coin}/{buy_coin} не доступна для {exchange} биржи')
    else:
        bot.reply_to(msg, r.text)


@bot.message_handler(commands=['курс', 'к', 'c', 'change'])
def view_change(msg):
    args = msg.text.split(" ")
    sell_coin = args[1].upper()
    buy_coin = args[2].upper()
    exchange = args[3]
    if len(args) == 4:
        number = 1
    else:
        number = args[4]
    r = requests.get(f'http://127.0.0.1:5000/current_coin_course/{exchange}/{sell_coin}_{buy_coin}?number={number}')
    if int(r.status_code) != 200:
        bot.reply_to(msg, f'{sell_coin}/{buy_coin} не доступна для {exchange} биржи')
    else:
        bot.reply_to(msg, r.text)


@bot.message_handler(commands=['новости', 'н', 'news', 'n'])
def view_news(msg):
    r = requests.get(f'http://127.0.0.1:5000/news')
    return bot.reply_to(msg, r.text)


@bot.message_handler(commands=['помощь', 'п', 'help', 'h'])
def view_help(msg):
    return bot.reply_to(msg, help_description.help_description_bot)


@bot.message_handler(commands=['график', 'г', 'graph', 'g'])
def view_graph(msg):
    args = msg.text.split()
    sell_coin = args[1].upper()
    buy_coin = args[2].upper()
    exchange = args[3]
    query_values = []
    if len(args) > 4:
        query_values.append(args[4] + " " + args[5])
    if len(args) > 6:
        query_values.append(args[6] + " " + args[7])
    query = form_query(['data_from', 'data_to', 'format'], query_values)
    r = requests.get(f'http://127.0.0.1:5000/print_graph/{exchange}/{sell_coin}_{buy_coin}?{query}')
    if int(r.status_code) != 200:
        bot.reply_to(msg, f'{sell_coin}/{buy_coin} не доступна для {exchange} биржи')
    else:
        path_to_graph = r.text
        bio = BytesIO()
        bio.name = path_to_graph
        image = Image.open(path_to_graph)
        image.save(bio, 'PNG')
        bio.seek(0)
        bot.send_photo(msg.chat.id, photo=bio)


@bot.message_handler(commands=['аналитика', 'а', 'analytics', 'a'])
def view_analics(msg):
    args = msg.text.split()
    sell_coin = args[1].upper()
    buy_coin = args[2].upper()
    exchange = args[3]
    query_values = []
    if len(args) > 4:
        query_values.append(args[4] + " " + args[5])
    if len(args) > 6:
        query_values.append(args[6] + " " + args[7])
    query = form_query(['data_from', 'data_to', 'format'], query_values)
    r = requests.get(f'http://127.0.0.1:5000/do_analytics/{exchange}/{sell_coin}_{buy_coin}?{query}')
    if int(r.status_code) != 200:
        bot.reply_to(msg, f'{sell_coin}/{buy_coin} не доступна для {exchange} биржи')
    else:
        bot.reply_to(msg, r.text)


@bot.message_handler(commands=['шпион', 'ш', 's', 'spy'])
def view_spy_result(msg):
    args = msg.text.split(" ")
    sell_coin = args[1].upper()
    buy_coin = args[2].upper()
    exchange = args[3]
    upper_course = args[4]
    r = requests.get(
        f'http://127.0.0.1:5000/check_price/{exchange}/{sell_coin}_{buy_coin}?value={upper_course}')
    if int(r.status_code) != 200:
        bot.reply_to(msg, f'{sell_coin}/{buy_coin} не доступна для {exchange} биржи')
    else:
        bot.reply_to(msg, r.text)


if __name__ == '__main__':
    print('Ready to work')
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            sleep(1)
