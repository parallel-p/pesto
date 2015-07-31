import sys
import os
import os.path
from ejudge_parse import ejudge_parse
from compositor_visitor import CompositorVisitor
from importlib import import_module
from importlib.util import find_spec
import stats


def get_param(num, query):
    if len(sys.argv) > num:
        return sys.argv[num]
    return input(query)


def get_stats_names(num, query):
    if len(sys.argv) > num:
        return sys.argv[num:]
    else:
        return input(query).split()


def suppose_csv():
    csv_filenames = [filename for filename in os.listdir() if filename.endswith('.csv')]
    if csv_filenames != []:
        return 'Supposed filenames:\n---\n{}\n---\n'.format('\n'.join(csv_filenames))
    return ''


def suppose_statistics():
    stat_names = [filename[:-3] for filename in os.listdir('stats') if filename.endswith('.py') and not filename.endswith('_test.py') and not filename == '__init__.py']
    if stat_names != []:
        return 'Supposed names:\n---\n{}\n---\n'.format('\n'.join(stat_names))
    return ''


def main():
    base_dir = get_param(1, 'Enter contests base dir name (if this directory contains several contests, add "%" before its name): ').strip()
    while not os.path.isdir(base_dir.lstrip('%')):
        base_dir = input('Please, enter correct directory names: ').split()
    base_dir = base_dir.rstrip('/').rstrip('\\')
    if base_dir.strip()[0] == '%':
        base_dir = base_dir[1:].strip()
        home_dirs = [base_dir + os.path.sep + i for i in os.listdir(base_dir)]
    else:
        home_dirs = [base_dir]
    csv_filename = get_param(2, 'Enter csv database filename: ' + suppose_csv())
    while not (os.path.isfile(csv_filename) and os.access(csv_filename, os.R_OK)):
        csv_filename = input('Please, enter correct filename: ')
    stats_names = get_stats_names(3, 'Enter statistics names (separate by spaces). ' + suppose_statistics())
    stats_modules = [import_module('stats.' + i) for i in stats_names if find_spec('stats.' + i) is not None]
    while len(stats_modules) == 0:
        stats_name = input('Please, enter correct stats name: ')
        if find_spec('stats.' + stats_name) is not None:
            stats_modules.append(import_module('stats.' + stats_name))
    stats_counters = [eval(i.__name__ + '.' + i.classname)() for i in stats_modules]  # creates stats objects
    compositor = CompositorVisitor(*stats_counters)
    ejudge_parse(home_dirs, csv_filename, compositor)
    print()
    print(compositor.pretty_print())


if __name__ == "__main__":
    main()
