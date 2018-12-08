def bind_parser(query_args):
    def parse_args(query):
        args = []
        for arg in query_args:
            if arg in query:
                args.append(query[arg])
        return args

    return parse_args


name_to_parse_method = {
    'current_coin_course': bind_parser(['number']),
    'print_graph': bind_parser(['data_from', 'data_to', 'format']),
    'last_trades': bind_parser(['limit']),
    'do_analytics': bind_parser(['data_from', 'data_to', 'format']),
    'check_price': bind_parser(['value']),
}
