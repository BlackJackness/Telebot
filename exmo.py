import requests
import time
import json
from bs4 import BeautifulSoup
from headers import exmo_headers
from datetime import datetime
from mpl_finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

SEC_PER_DAY = 24 * 3600


def get_timestamp_format(date_from_format, date_to_format, format):
    if date_from_format is None:
        date_from_format = datetime.utcfromtimestamp(int(time.time()) - SEC_PER_DAY).strftime(
            '%Y-%m-%d %H:%M:%S')
    if date_to_format is None:
        date_to_format = datetime.utcfromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
    date_from = int(time.mktime(datetime.strptime(date_from_format, format).timetuple()))
    date_to = int(time.mktime(datetime.strptime(date_to_format, format).timetuple()))
    return date_from, date_to, date_from_format, date_to_format


class ExmoExchange:
    birge_methods = {'current_coin_course', 'print_graph', 'last_trades', 'do_analytics', 'check_price'}

    def current_coin_course(self, sell_coin, buy_coin='USD', number=1):
        r = requests.get(f'https://exmo.me/en/trade#?pair={sell_coin}_{buy_coin}')
        soup = BeautifulSoup(r.text, "lxml")
        trs = soup.find_all('tr', class_='table_body pair')
        need_pair = f"{sell_coin}/{buy_coin}"
        for tr in trs:
            fields = tr.find_all('td')
            pair = fields[1].get_text()
            if need_pair == pair:
                buy = fields[2].get_text()
                sell = fields[3].get_text()
                changes = fields[4].get_text()
                change_result = float(buy) * float(number)
                return f'''Текущий курс заданной пары {sell_coin}/{buy_coin} :
                                        покупка : {buy}
                                        продажа  : {sell}
                                        колебания курса : {changes}
    Значит,при продаже {number} {sell_coin} вы получите {change_result} {buy_coin}'''

    def last_trades(self, sell_coin, buy_coin='USD', limit=10):
        r = requests.post('https://exmo.me/ctrl/trades', data=json.dumps({'pair': f"{sell_coin}_{buy_coin}"}),
                          headers=exmo_headers)
        last_trades_list = [f'Последние сделки в паре {sell_coin}/{buy_coin}']
        ind = 1
        for item in r.json()['data']['items'][::-1]:
            if ind > int(limit):
                break
            date = datetime.utcfromtimestamp(int(item['date'])).strftime('%Y-%m-%d %H:%M:%S')
            ttype, quantity, price, amount = item['type'], item['quantity'], item['price'], item['amount']
            last_trades_list += [
                f"\t{ind}. {date} {ttype} {quantity} {sell_coin} for {amount} {buy_coin} were price was {price}"]
            ind += 1
        return "\n".join(last_trades_list)

    def print_graph(self, sell_coin, buy_coin='USD', date_from_format=None, date_to_format=None,
                    format='%Y-%m-%d %H:%M:%S'):
        date_from, date_to, date_from_format, date_to_format = get_timestamp_format(date_from_format, date_to_format,
                                                                                    format)
        r = requests.get(
            f'https://exmo.me/ctrl/chart/history?symbol={sell_coin}_{buy_coin}&resolution=30&from={date_from}&to={date_to}',
            headers=exmo_headers)
        opened = []
        high = []
        low = []
        close = []
        xdate = []
        for item in r.json()['candles']:
            opened.append(item['o'])
            high.append(item['h'])
            low.append(item['l'])
            close.append(item['c'])
            xdate.append(datetime.fromtimestamp(int(item['t']) // 1000 - time.timezone))
        fig, ax = plt.subplots()
        ax.set_xlabel('Date')
        ax.set_ylabel(f'One {sell_coin} in {buy_coin}')
        ax.set_title(
            f'{sell_coin}/{buy_coin} from {date_from_format} to {date_to_format}')
        candlestick2_ohlc(ax, np.array(opened), np.array(high), np.array(low), np.array(close), colorup='g', width=0.8)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

        def mydate(x, pos):
            try:
                return xdate[int(x)]
            except IndexError:
                return ''

        ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.grid(True)
        plt.autoscale(True)
        hash_name = hex(
            abs(hash('bin')) * abs(hash(sell_coin) + hash(buy_coin) * hash(date_from_format) + hash(date_to_format)))
        plt.savefig(f'{hash_name}.png')
        return f'{hash_name}.png'

    def do_analytics(self, sell_coin, buy_coin='USD', date_from_format=None, date_to_format=None,
                     format='%Y-%m-%d %H:%M:%S'):
        date_from, date_to, date_from_format, date_to_format = get_timestamp_format(date_from_format, date_to_format,
                                                                                    format)
        r = requests.get(
            f'https://exmo.me/ctrl/chart/history?symbol={sell_coin}_{buy_coin}&resolution=30&from={date_from}&to={date_to}',
            headers=exmo_headers)
        candles = r.json()['candles']
        open_cost = float(candles[0]['o'])
        close_cost = float(candles[-1]['c'])
        delta_cost = round(close_cost - open_cost, 9)
        return f'''Стоймость {sell_coin} при открытии {date_from_format} : {open_cost} {buy_coin}
    Стоймость {sell_coin} при закрытии {date_to_format} : {close_cost} {buy_coin}
    Итоговое изменение : {delta_cost} {buy_coin}'''

    def check_price(self, sell_coin, buy_coin, value):
        value = float(value)
        num_of_check = 100
        while num_of_check > 0:
            num_of_check -= 1
            r = requests.get(f'https://exmo.me/en/trade#?pair={sell_coin}_{buy_coin}')
            soup = BeautifulSoup(r.text, "lxml")
            trs = soup.find_all('tr', class_='table_body pair')
            need_pair = f"{sell_coin}/{buy_coin}"
            for tr in trs:
                fields = tr.find_all('td')
                pair = fields[1].get_text()
                if need_pair == pair:
                    buy = float(fields[2].get_text())
                    if buy >= value:
                        return f'''Текущий курс заданной пары {sell_coin}/{buy_coin} : {buy}'''
                    else:
                        break
            time.sleep(10)
        return f'Биржа сегодня не благосклонна,текущий курс {buy}'


exmo_exchange = ExmoExchange()
