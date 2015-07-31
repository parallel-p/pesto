import sys
import ejudge_parse
import visitor


def get_param(num, query):
    if len(sys.argv) > num:
        return sys.argv[num]
    return input(query)

home_dir = get_param(1, 'Enter contests base dir name: ')
csv_filename = get_param(2, 'Enter csv database filename: ')
stats_names = [get_param(3, 'Enter statistics name: ')]
if len(sys.argv) > 4:
    stats_names.extend(sys.argv[4:])
stats_modules = [__import__('stats.' + i) for i in stats_names]
stats_counters = [visitor.Visitor() for i in stats_modules]  # should create stats objects here
ejudge_parse.ejudge_parse(home_dir, stats_counters, csv_filename)
for i in stats_modules:
    print(i.get_stat_data())
