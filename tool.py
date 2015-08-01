import sys
import os
import os.path
from ejudge_parse import ejudge_parse
from compositor_visitor import CompositorVisitor
from importlib import import_module
from importlib.util import find_spec
import argparse


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
    if csv_filenames:
        return 'Supposed filenames:\n---\n{}\n---\n'.format('\n'.join(csv_filenames))
    return ''


def suppose_statistics():
    stat_names = [filename[:-3] for filename in os.listdir('stats') if filename.endswith('.py')
                  and not filename.endswith('_test.py') and not filename == '__init__.py']
    if stat_names:
        return 'Supposed names:\n---\n{}\n---\n'.format('\n'.join(stat_names))
    return ''


def get_arguments_from_keyboard():
    base_dir = input('Enter contests base dir name: ').strip()
    while not os.path.isdir(base_dir):
        base_dir = input('Please, enter correct directory name: ').strip()
    base_dir = base_dir.rstrip('/').rstrip('\\')

    is_multicontest = input('Does this directory contain only one contest? (y/n) ').lower()
    while is_multicontest[0] not in 'yn':
        is_multicontest = input('Enter "y" or "n": ').lower()
    is_multicontest = is_multicontest[0] == 'n'

    csv_filename = input('Enter csv database filename: ' + suppose_csv()).strip()
    while not (os.path.isfile(csv_filename) and os.access(csv_filename, os.R_OK)):
        csv_filename = input('Please, enter correct filename: ').strip()

    stats_counters = []
    while not stats_counters:
        stats_names = input('Enter statistics names (separate by spaces). ' + suppose_statistics()).split()
        stats_modules = []
        for stats_name in stats_names:
            if find_spec('stats.' + stats_name) is not None:
                stats_modules.append(import_module('stats.' + stats_name))
            else:
                print(stats_name, 'not found')  # TODO something more noticeable
        for i in stats_modules:
            try:
                # stats_counters.append(eval(i.__name__ + '.' + i.classname)())
                stats_counters.append(getattr(i, i.classname)())
            except AttributeError:
                print(i.__name__.split('.')[1], 'is broken, skipping')  # TODO something more noticeable
        if not stats_counters:
            print('No statistics selected')  # TODO something more noticeable

    return base_dir, is_multicontest, csv_filename, stats_counters, {}


def get_arguments_from_cmdline():
    parser = argparse.ArgumentParser(description="Calculate some statistics")
    parser.add_argument('-m', '--multicontest', help='base_dir contains several contests', action='store_true')
    parser.add_argument('-o', '--outfile', help='output file')
    parser.add_argument('base_dir', help="directory containing xml's")
    parser.add_argument('csv_filename', help="csv file")
    parser.add_argument('stats_names', help="names of statistics modules", nargs='+')
    args = vars(parser.parse_args())
    stats_names = args['stats_names']
    stats_modules = []
    for stats_name in stats_names:
        if find_spec('stats.' + stats_name) is not None:
            stats_modules.append(import_module('stats.' + stats_name))
        else:
            print(stats_name, 'not found')
    stats_counters = []
    for i in stats_modules:
        try:
            # stats_counters.append(eval(i.__name__ + '.' + i.classname)())
            stats_counters.append(getattr(i, i.classname)())
        except AttributeError:
            print(i.__name__.split('.')[1], 'is broken, skipping')
    if not stats_counters:
        print('No statistics selected')
        exit()
    optional = {}
    if args['outfile']:
        optional['outfile'] = args['outfile']
    return args['base_dir'], args['multicontest'], args['csv_filename'], stats_counters, optional


def main():
    if len(sys.argv) < 2:
        base_dir, is_multicontest, csv_filename, stats_counters, optional = get_arguments_from_keyboard()
    else:
        base_dir, is_multicontest, csv_filename, stats_counters, optional = get_arguments_from_cmdline()
    base_dir = base_dir.rstrip('/').rstrip('\\')
    if is_multicontest:
        home_dirs = [base_dir + os.path.sep + i for i in os.listdir(base_dir)]
    else:
        home_dirs = [base_dir]
    compositor = CompositorVisitor(*stats_counters)
    ejudge_parse(home_dirs, csv_filename, compositor)
    result = compositor.pretty_print()
    if 'outfile' in optional:
        with open(optional['outfile'], 'w') as outfile:
            outfile.write(result)
    else:
        print()
        print(result)


if __name__ == "__main__":
    main()
