import os
import os.path
from ejudge_parse import ejudge_parse
import tool_config
import argparse
import filter_visitor
from pickle_walker import pickle_walker

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate some statistics")
    parser.add_argument('-m', '--multicontest', help='base_dir contains several contests', action='store_true')
    parser.add_argument('-p', '--pickle', help='contest dirs contains pickles instead of xmls', action='store_true')
    parser.add_argument('-o', '--outfile', help='output file')
    parser.add_argument('--filter-problem', metavar='ID', help='process only submits for the problem selected')
    parser.add_argument('--filter-user', metavar='ID', help='process only submits by the selected user')
    parser.add_argument('--filter-contest', metavar='ID', help='process only submits in the selected contest')
    parser.add_argument('base_dir', help="directory containing xml's")
    parser.add_argument('csv_filename', help="csv file")
    parser.add_argument('preset_name', help="name or number of statistics preset", nargs='?')
    return vars(parser.parse_args())


def get_arguments():
    args = parse_args()
    base_dir = args['base_dir']
    csv_filename = args['csv_filename']
    is_multicontest = args['multicontest']
    is_pickle = args['pickle']
    preset_name = args['preset_name']

    base_dir = base_dir.rstrip('/').rstrip('\\')  # something very important

    if not preset_name:
        print('Presets available:', tool_config.get_presets_info())
        exit()
    stats_counter = tool_config.get_visitor_by_preset(preset_name)
    if stats_counter is None:
        print('Invalid preset name')
        exit()

    optional = {}
    if args['outfile']:
        optional['outfile'] = args['outfile']
    if args.get('filter_problem'):
        optional['filter_problem'] = args['filter_problem']
    if args.get('filter_user'):
        optional['filter_user'] = args['filter_user']
    if args.get('filter_contest'):
        optional['filter_contest'] = args['filter_contest']

    return base_dir, is_multicontest, is_pickle, csv_filename, stats_counter, optional


def main():
    base_dir, is_multicontest, is_pickle, csv_filename, visitor, optional = get_arguments()
    if is_multicontest:
        home_dirs = [base_dir + os.path.sep + i for i in os.listdir(base_dir)]
    else:
        home_dirs = [base_dir]
    if 'filter_user' in optional:
        visitor = filter_visitor.FilterByUserVisitor(visitor, optional['filter_user'])
    if 'filter_problem' in optional:
        visitor = filter_visitor.FilterByProblemVisitor(visitor, optional['filter_problem'])
    if 'filter_contest' in optional:
        visitor = filter_visitor.FilterByContestVisitor(visitor, optional['filter_contest'])
    if is_pickle:
        for home_dir in home_dirs:
            for submit in pickle_walker(home_dir):
                visitor.visit(submit)
    else:
        ejudge_parse(home_dirs, csv_filename, visitor)
    result = visitor.pretty_print()
    del visitor
    if 'outfile' in optional:
        with open(optional['outfile'], 'w') as outfile:
            outfile.write(result)
    else:
        print(result)


if __name__ == "__main__":
    main()
