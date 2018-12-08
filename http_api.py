from request_resolver import *

from flask import Flask, request

import help_description

app = Flask(__name__)


@app.route('/')
def view_default():
    return 'choose command or use /help'


@app.route('/news')
def view_news():
    return get_news()


@app.route('/help')
def view_help():
    return help_description.help_description_api


@app.route('/<method>/<cryptobirge>/<pair>')
def get_cryptobirge_method_result(method, cryptobirge, pair):
    return resolve_method(cryptobirge, method, pair, request.args)


if __name__ == '__main__':
    print('API available')
    app.run()
