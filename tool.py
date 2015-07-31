import sys
from ejudge_parse import ejudge_parse
from compositor_visitor import CompositorVisitor
from importlib import import_module
import stats


def get_param(num, query):
    if len(sys.argv) > num:
        return sys.argv[num]
    return input(query)


def main():
    home_dir = get_param(1, 'Enter contests base dir name: ')
    csv_filename = get_param(2, 'Enter csv database filename: ')
    stats_names = [get_param(3, 'Enter statistics name: ')]
    if len(sys.argv) > 4:
        stats_names.extend(sys.argv[4:])
    stats_modules = [import_module('stats.' + i) for i in stats_names]
    stats_counters = [eval(i.__name__ + '.' + i.classname)() for i in stats_modules]  # creates stats objects
    compositor = CompositorVisitor(*stats_counters)
    ejudge_parse([home_dir], csv_filename, compositor)
    print(compositor.pretty_print())


if __name__ == "__main__":
    main()
