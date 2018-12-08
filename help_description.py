help_description_bot = '''
Чем я могу помочь?

EXG = [bin,exmo] - выбрать биржу   
COIN = [btc,eth...usdt,usd] - монеты и ресурсы доступные на 
                              бирже

'курс', 'к', 'c', 'change':
   /с COIN COIN EXG [number = 1] - показать текущий курс от 
                                   заданной пары ресурсов
    number - курс к определенному колличеству первого
             ресурса
    
'сделки', 'сд', 't', 'trade':
   /t COIN COIN EXG [limit = 10] - показать последние сделки
                                   в заданной паре
    limit - определеняет кол-во последних

'шпион', 'ш', 's', 'spy':
   /s COIN COIN EXG value - в течении некоторого времени
    проверяет,стал ли курс заданной пары больше value

'новости', 'н', 'news', 'n':
   /n - показать последние новости в мире крипто валют
   
'помощь', 'п', 'help', 'h':
   /h - всё,чем я могу помочь
   
'график', 'г', 'graph', 'g':
    /g COIN COIN EXG [date_from = now() - 5 min,date_from=now()] 
                        - отобразить график изменения курса
                          заданной пары в 'свечах' от начальной
                          даты до конечной
    date_from - начальная дата в формате
                    YYYY-MM-DD HH:MM:SS
    date_to - конечная дата в формате
                    YYYY-MM-DD HH:MM:SS
    now() - берет момент оправки
    
'аналитика', 'а', 'analytics', 'a':
    /a COIN COIN EXG [date_from = now() - 5 min,date_from=now()]
                    - показать изменение курса данной пары
                      с начального срока до конечного                   
    date_from - начальная дата в формате 
                        YYYY-MM-DD HH:MM:SS
    date_to - конечная дата 
                        YYYY-MM-DD HH:MM:SS
    now() - берет момент оправки
    
'''

help_description_api = '''
<pre>
Чем я могу помочь?

/news - показать последние новости в мире крипто валют

/help - всё,чем я могу помочь

/METHOD/CRYPTOBIRGE/PAIR?QUERY
    CRYPTOBIRGE = [bin,exmo]
    PAIR = COIN_COIN
    COIN = [btc,eth...usdt,usd] - монеты и ресурсы доступные на бирже
    QUERY зависит от метода
    METHOD :
        'current_coin_course'
            - показать текущий курс от заданной пары ресурсов
                number - курс к определенному колличеству первого
                ресурса
            QUERY = [number = 1]
                number - курс к определенному колличеству первого ресурса
        
        'print_graph': 
                - отобразить график изменения курса
                  заданной пары в 'свечах' от начальной
                  даты до конечной
                QUERY = [date_from = now() - 5 min,date_from=now()] 
                    date_from - начальная дата в формате
                        YYYY-MM-DD HH:MM:SS
                    date_to - конечная дата в формате
                        YYYY-MM-DD HH:MM:SS
                    now() - берет момент оправки
            
        'last_trades':
             - показать последние сделки в заданной паре
             QUERY = [limit = 10]
                limit - определеняет кол-во последних
        'do_analytics':
             - показать изменение курса данной пары
                      с начального срока до конечного
            QUERY = [date_from = now() - 5 min,date_from=now()] 
                date_from - начальная дата в формате
                    YYYY-MM-DD HH:MM:SS
                date_to - конечная дата в формате
                    YYYY-MM-DD HH:MM:SS
                now() - берет момент оправки 
        'check_price': 
            - в течении некоторого времени
                проверяет,стал ли курс заданной пары больше value
            QUERY = [value]
</pre>        
'''
