from request_resolver import *
import re

methods = {'current_coin_course', 'print_graph', 'last_trades', 'do_analytics'}
coins = ['BTC', 'ETH', 'ETC', 'ADA']


def test_current_coin_course():
    for coin in coins:
        bin_res = resolve_method('bin', 'current_coin_course', f'{coin}_USDT', {})
        exmo_res = resolve_method('exmo', 'current_coin_course', f'{coin}_USD', {})
        assert re.match(
            'Текущий курс заданной пары ' + coin + '/USDT : [0-9.]+\n {4}Значит,при продаже [0-9.]+ ' + coin + ' вы получите [0-9.]+ USDT',
            bin_res)
        assert re.match(f'Текущий курс заданной пары ' + coin + '/USD :', exmo_res)
        bin_count = float(re.search('[0-9.]+', bin_res).group(0))
        exmo_count = float(re.search('[0-9.]+', exmo_res).group(0))
        assert abs(bin_count - exmo_count) / max(bin_count, exmo_count) < 0.1


dates = {
    'data_from': '2018-10-5 20:00:00',
    'data_to': '2018-11-5 21:05:00'
}


def test_print_graph():
    for coin in coins:
        bin_res = resolve_method('bin', 'print_graph', f'{coin}_USDT', dates)
        exmo_res = resolve_method('exmo', 'print_graph', f'{coin}_USD', dates)
        assert open(bin_res)
        assert open(exmo_res)


def test_last_trades():
    query = {
        'limit': 1
    }
    for coin in coins:
        bin_res = resolve_method('bin', 'last_trades', f'{coin}_USDT', query)
        exmo_res = resolve_method('exmo', 'last_trades', f'{coin}_USD', query)
        assert re.match(
            'Последние сделки в паре ' + coin + r'/USDT\n\t[0-9]+\. [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} (buy|sell) [0-9.]+ ' + coin + ' for [0-9.]+ USDT were price was [0-9.]+',
            bin_res)
        assert re.match(
            'Последние сделки в паре ' + coin + r'/USD\n\t[0-9]+\. [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} (buy|sell) [0-9.]+ ' + coin + ' for [0-9.]+ USD were price was [0-9.]+',
            exmo_res)


real_changes = {'BTC': ['6588.17 USDT', '6455.02 USDT', '-133.15 USDT', '6634.43363601 USD', '6463.79999999 USD',
                        '-170.63363602 USD'],
                'ETH': ['223.94 USDT', '208.68 USDT', '-15.26 USDT', '223.60116459 USD', '209.5828455 USD',
                        '-14.01831909 USD'],
                'ETC': ['11.0278 USDT', '9.3613 USDT', '-1.6665 USDT', '11.12185252 USD', '9.3507 USD',
                        '-1.77115252 USD'],
                'ADA': ['0.08226 USDT', '0.07677 USDT', '-0.00549 USDT', '0.0829955 USD', '0.0769382 USD',
                        '-0.0060573 USD']}


def test_do_analytics():
    for coin in coins:
        expected = real_changes[coin]
        bin_res = resolve_method('bin', 'do_analytics', coin + '_USDT', dates)
        exmo_res = resolve_method('exmo', 'do_analytics', coin + '_USD', dates)
        changes = []
        for match in re.findall('-?[0-9.]+ USDT', bin_res):
            changes.append(match)
        for match in re.findall('-?[0-9.]+ USD', exmo_res):
            changes.append(match)
        for excpect, result in zip(expected, changes):
            assert excpect == result
