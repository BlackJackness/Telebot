import requests
from bs4 import BeautifulSoup
from binance import binance_exchange
from exmo import exmo_exchange
from args_parser import name_to_parse_method


def get_exchange(alias):
    if alias == 'bin':
        return binance_exchange
    elif alias == 'exmo':
        return exmo_exchange
    else:
        return None


def get_news():
    r = requests.get(f'https://cryptonews.com')
    soup = BeautifulSoup(r.text, "lxml")
    column = soup.find('div', class_='cn-list cols')
    news = column.find_all('div', class_='cn-tile row article')
    news_list = ['Current news : ']
    for item in news:
        tm = item.find('time').get_text()
        link = item.find('h4').find('a')
        text = link.get_text()
        ref = 'https://cryptonews.com' + link['href']
        news_list += [f'\t{tm} : {text}\n\tNow more : {ref}\n']
    return '\n'.join(news_list)


def resolve_method(cryptobirge, method_name, pair, query):
    exchange = get_exchange(cryptobirge)
    if method_name in exchange.birge_methods:
        parse_func = name_to_parse_method[method_name]
        query_args = parse_func(query)
        sell_coin, buy_coin = pair.split('_')
        return getattr(exchange, method_name)(sell_coin, buy_coin, *query_args)
    else:
        return "Неизвестная команда"
