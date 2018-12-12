import requests
import time
from datetime import datetime
from mpl_finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from math import ceil

SEC_PER_DAY = 24 * 3600
BINANCE_UPLOAD_CONST = 30000


def get_timestamp_format(date_from_format, date_to_format, format):
    if date_from_format is None:
        date_from_format = datetime.utcfromtimestamp(int(time.time()) - SEC_PER_DAY - time.timezone).strftime(
            '%Y-%m-%d %H:%M:%S')
    if date_to_format is None:
        date_to_format = datetime.utcfromtimestamp(int(time.time()) - time.timezone).strftime('%Y-%m-%d %H:%M:%S')
    date_from = int(time.mktime(datetime.strptime(date_from_format, format).timetuple())) + time.timezone
    date_to = int(time.mktime(datetime.strptime(date_to_format, format).timetuple())) + time.timezone
    return date_from, date_to, date_from_format, date_to_format


class BinanceExchange:
    birge_methods = {'current_coin_course', 'print_graph', 'last_trades', 'do_analytics', 'check_price'}

    def current_coin_course(self, sell_coin, buy_coin='USDT', number=1):
        r = requests.get(f'https://www.binance.com/api/v1/klines?symbol={sell_coin}{buy_coin}&interval=1m')
        rate = r.json()[-1][4]
        return f'''Текущий курс заданной пары {sell_coin}/{buy_coin} : {rate}
    Значит,при продаже {number} {sell_coin} вы получите {float(rate) * float(number)} {buy_coin}'''

    def print_graph(self, sell_coin, buy_coin='USDT', date_from_format=None, date_to_format=None,
                    format='%Y-%m-%d %H:%M:%S'):
        date_from, date_to, date_from_format, date_to_format = get_timestamp_format(date_from_format, date_to_format,
                                                                                    format)
        r = requests.get(
            f'https://www.binance.com/api/v1/klines?symbol={sell_coin}{buy_coin}&interval=1m&startTime={date_from*1000}&endTime={date_to*1000}')
        opened = []
        high = []
        low = []
        close = []
        xdate = []
        for item in r.json():
            candle_time = int(item[0]) // 1000
            if candle_time < date_from:
                continue
            if candle_time > date_to:
                break
            opened.append(float(item[1]))
            high.append(float(item[2]))
            low.append(float(item[3]))
            close.append(float(item[4]))
            xdate.append(datetime.fromtimestamp(candle_time - time.timezone))
        fig, ax = plt.subplots()
        ax.set_xlabel('Date')
        ax.set_ylabel(f'One {sell_coin} in {buy_coin}')
        ax.set_title(f'{sell_coin}/{buy_coin} from {date_from_format} to {date_to_format}')
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

    def last_trades(self, sell_coin, buy_coin='USDT', limit=20):
        r = requests.get(f'https://www.binance.com/api/v1/aggTrades?limit={limit}&symbol={sell_coin}{buy_coin}')
        last_trades_list = [f'Последние сделки в паре {sell_coin}/{buy_coin}']
        ind = 1
        for item in r.json():
            date = datetime.utcfromtimestamp(int(item['T']) // 1000 - time.timezone).strftime('%Y-%m-%d %H:%M:%S')
            quantity, price = item['q'], item['p']
            buy_volume = round(float(price) * float(quantity), 6)
            last_trades_list += [
                f"\t{ind}. {date} buy {quantity} {sell_coin} for {buy_volume} {buy_coin} were price was {price}"]
            ind += 1
        return "\n".join(last_trades_list)

    def do_analytics(self, sell_coin, buy_coin='USDT', date_from_format=None, date_to_format=None,
                     format='%Y-%m-%d %H:%M:%S'):
        date_from, date_to, date_from_format, date_to_format = get_timestamp_format(date_from_format, date_to_format,
                                                                                    format)
        r = requests.get(
            f'https://www.binance.com/api/v1/klines?symbol={sell_coin}{buy_coin}&interval=1m&endTime={date_from * 1000}')
        open_cost = float(r.json()[-1][4])
        r = requests.get(
            f'https://www.binance.com/api/v1/klines?symbol={sell_coin}{buy_coin}&interval=1m&endTime={date_to * 1000}')
        close_cost = float(r.json()[-1][4])
        delta_cost = round(close_cost - open_cost, 9)
        return f'''Стоймость {sell_coin} при открытии {date_from_format} : {open_cost} {buy_coin}
    Стоймость {sell_coin} при закрытии {date_to_format} : {close_cost} {buy_coin}
    Итоговое изменение : {delta_cost} {buy_coin}'''

    def check_price(self, sell_coin, buy_coin, value):
        value = float(value)
        num_of_check = 100
        while num_of_check > 0:
            num_of_check -= 1
            r = requests.get(f'https://www.binance.com/api/v1/klines?symbol={sell_coin}{buy_coin}&interval=1m')
            rate = float(r.json()[-1][4])
            if rate >= value:
                return f'''Текущий курс заданной пары {sell_coin}/{buy_coin} : {rate}'''
            time.sleep(10)
        return f'Биржа сегодня не благосклонна,текущий курс {rate}'


binance_exchange = BinanceExchange()
