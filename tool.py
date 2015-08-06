import os
import os.path
from ejudge_parse import ejudge_parse
import tool_config
import argparse
import filter_visitor
import configparser
from pickle_walker import pickle_walker
import toollib

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate some statistics")
    toollib.parse_args_config(parser)
    toollib.parse_args_input(parser)
    toollib.parse_args_output(parser)
    toollib.parse_args_filters(parser)
    parser.add_argument('-p', '--pickle', help='contest dirs contains pickles instead of xmls', action='store_true')
    parser.add_argument('--database', help="database csv file")
    parser.add_argument('preset_name', help="name or number of statistics preset", nargs='?')
    return vars(parser.parse_args())

def get_arguments():
    args = parse_args()
    config_name = args['cfg'] if args['cfg'] else 'default.ini'
    config = toollib.read_config(config_name, 'tool')
    if config is None:
        print('Incorrect config scpecifed.')
        exit()
    try:
        base_dir = args['dir'] if args['dir'] else (config['pickle_dir'] if args['pickle'] else config['base_dir'])
        csv_filename = args['database'] if args['database'] else config['database']
        outfile = (args['outfile'] if args['outfile'] else config['outfile']) if not args['console'] else None
    except KeyError:
        print('Invalid config, see config.ini.example')
        exit()
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
    if outfile:
        optional['outfile'] = outfile
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
        home_dirs = toollib.get_contests_from_dir(base_dir)
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
    visitor.close()
    if 'outfile' in optional:
        with open(optional['outfile'], 'w') as outfile:
            outfile.write(result)
    else:
        print(result)


if __name__ == "__main__":
    main()
