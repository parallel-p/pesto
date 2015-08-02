import sys
import os
import os.path
from ejudge_parse import ejudge_parse
from compositor_visitor import CompositorVisitor
from importlib import import_module
from importlib.util import find_spec
import argparse
import filter_visitor
from pickle_walker import pickle_walker


def suppose_csv():
    csv_filenames = [filename for filename in os.listdir() if filename.endswith('.csv')]
    if csv_filenames:
        return 'Supposed filenames:\n---\n{}\n---\n'.format('\n'.join(csv_filenames))
    return ''


def suppose_statistics():
    stat_names = [filename[:-3] for filename in os.listdir('stats') if filename.endswith('.py')
                  and not filename.endswith('_test.py') and not filename == '__init__.py']
    if not stat_names:
        return ''
    stat_formatted = ['{}: {}'.format(num, stat) for num, stat in enumerate(stat_names)]
    return ('Supposed names:\n---\n{}\n---\n'.format('\n'.join(stat_formatted)), stat_names)


def get_arguments():
    parser = argparse.ArgumentParser(description="Calculate some statistics")
    parser.add_argument('-m', '--multicontest', help='base_dir contains several contests', action='store_true')
    parser.add_argument('-o', '--outfile', help='output file')
    parser.add_argument('--filter-problem', metavar='ID', help='process only submits for the problem selected')
    parser.add_argument('--filter-user', metavar='ID', help='process only submits by the selected user')
    parser.add_argument('--filter-contest', metavar='ID', help='process only submits in the selected contest')
    parser.add_argument('-p', '--pickle', help='contest dirs contains pickles instead of xmls', action='store_true')
    parser.add_argument('base_dir', nargs='?', default=None, help="directory containing xml's")
    parser.add_argument('csv_filename', nargs='?', default=None, help="csv file")
    parser.add_argument('stats_names', default=None, help="names of statistics modules", nargs='*')
    args = vars(parser.parse_args())

    base_dir = args['base_dir']
    is_multicontest = args['multicontest']
    is_pickle = args['pickle']
    request_multicontest = 0

    if base_dir is None:
        base_dir = input('Enter contests base dir name: ').strip()
        request_multicontest = 1
    while not os.path.isdir(base_dir):
        base_dir = input('Please, enter correct directory name: ').strip()
    base_dir = base_dir.rstrip('/').rstrip('\\')
    if request_multicontest:
        is_multicontest = input('Does this directory contain only one contest? (y/n) ').lower()
        while is_multicontest[0] not in 'yn':
            is_multicontest = input('Enter "y" or "n": ').lower()
        is_multicontest = is_multicontest[0] == 'n'

    if not is_pickle:
        is_pickle = input('Does this directory contain only one contest? (y/n) ').lower()
        while is_pickle[0] not in 'yn':
            is_pickle = input('Enter "y" or "n": ').lower()
        is_pickle = is_pickle[0] == 'y'

    csv_filename = args['csv_filename']
    if csv_filename is None:
        csv_filename = input('Enter csv database filename: ' + suppose_csv()).strip()
    while not (os.path.isfile(csv_filename) and os.access(csv_filename, os.R_OK)):
        csv_filename = input('Please, enter correct filename: ').strip()

    stats_names = args['stats_names']
    stats_counters = []
    while not stats_counters:
        if stats_names is None:
            supposed_stats = suppose_statistics()
            stats_names = input('Enter statistics names or numbers (separate by spaces): ' + supposed_stats[0]).split()
            for i in range(len(stats_names)):
                if stats_names[i].isdigit():
                    try:
                        stats_names[i] = supposed_stats[1][int(stats_names[i])]
                    except IndexError:
                        print('There is no statistics', i)
        stats_modules = []
        for stats_name in stats_names:
            if find_spec('stats.' + stats_name) is not None:
                stats_modules.append(import_module('stats.' + stats_name))
            else:
                print(stats_name, 'not found')  # TODO something more noticeable
        for i in stats_modules:
            try:
                stats_counters.append(getattr(i, i.classname)())
            except AttributeError:
                print(i.__name__.split('.')[1], 'is broken, skipping')  # TODO something more noticeable
        if not stats_counters:
            print('No statistics selected')  # TODO something more noticeable
        stats_names = None

    optional = {}
    if args['outfile']:
        optional['outfile'] = args['outfile']
    if args.get('filter_problem'):
        optional['filter_problem'] = args['filter_problem']
    if args.get('filter_user'):
        optional['filter_user'] = args['filter_user']
    if args.get('filter_contest'):
        optional['filter_contest'] = args['filter_contest']

    return base_dir, is_multicontest, is_pickle, csv_filename, stats_counters, optional


def main():
    base_dir, is_multicontest, is_pickle, csv_filename, stats_counters, optional = get_arguments()
    if is_multicontest:
        home_dirs = [base_dir + os.path.sep + i for i in os.listdir(base_dir)]
    else:
        home_dirs = [base_dir]
    visitor = CompositorVisitor(*stats_counters)
    if 'filter_user' in optional:
        visitor = filter_visitor.FilterByUserVisitor(visitor, optional['filter_user'])
    if 'filter_problem' in optional:
        visitor = filter_visitor.FilterByProblemVisitor(visitor, optional['filter_problem'])
    if 'filter_contest' in optional:
        visitor = filter_visitor.FilterByContestVisitor(visitor, optional['filter_contest'])
    if is_pickle:
        print('!!!')
        for home_dir in home_dirs:
            for submit in pickle_walker(home_dir):
                visitor.visit(submit)
    else:
        ejudge_parse(home_dirs, csv_filename, visitor)
    result = visitor.pretty_print()
    if 'outfile' in optional:
        with open(optional['outfile'], 'w') as outfile:
            outfile.write(result)
    else:
        print()
        print(result)


if __name__ == "__main__":
    main()
