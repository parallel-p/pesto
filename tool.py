import os
import os.path
from ejudge_parse import ejudge_parse
import tool_config
import argparse
import filter_visitor
import configparser
import walker
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
    args, config = parse_args(), None
    if args['cfg']:
        try:
            config = toollib.read_config(args['cfg'], 'tool')
        except KeyError:
            print('Incorrect config filename.')
            exit()
    else:
        config = dict(pickle_dir=None, database=None, base_dir=None, trash='trash')
        config['output'] = 'pickle' if args['pickle'] else 'output.txt'

    base_dir, output, csv_filename = None, None, None
    try:
        base_dir = args['dir'] if args['dir'] else (config['pickle_dir'] if args['pickle'] else config['base_dir'])
        base_dir = base_dir.rstrip('/').rstrip('\\')
        csv_filename = args['database'] if args['database'] else config['database']
        output = (args['output'] if args['output'] else config['output']) if not args['console'] else None
        output = output.rstrip('/').rstrip('\\')
    except KeyError:
        print('Invalid config, see config.ini.example')
        exit()
    if base_dir is None:
        print('Directory is not defined.')
        exit()
    if not args['pickle'] and csv_filename is None:
        print('Database file is not defined.')
        exit()
    stats_counter = tool_config.get_visitor_by_preset(args['preset_name'], output)
    if stats_counter is None:
        print('Preset name is not defined or invalid.')
        print('Presets available:', tool_config.get_presets_info())
        exit()

    optional = dict()
    if output:
        optional['outfile'] = output
    if args.get('filter_problem'):
        optional['filter_problem'] = args['filter_problem']
    if args.get('filter_user'):
        optional['filter_user'] = args['filter_user']
    if args.get('filter_contest'):
        optional['filter_contest'] = args['filter_contest']

    return base_dir, args['multicontest'], args['pickle'], csv_filename, stats_counter, optional


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
    if is_multicontest:
        contest_walker = walker.MultipleContestWalker()
    else:
        contest_walker = walker.SingleContestWalker()

    if is_pickle:
        file_walker = walker.PickleWorker()
    else:
        file_walker = walker.AllFilesWalker()

    for contest in contest_walker.walk(base_dir):
        obj_walker = walker.SubmitWalker(csv_filename, contest[0])
        for file in file_walker.walk(contest[1]):
            for submit in obj_walker.walk(file[1]):
                if submit:
                    visitor.visit(submit)

    result = visitor.pretty_print()
    visitor.close()
    if 'outfile' in optional:
        with open(optional['outfile'], 'w') as outfile:
            outfile.write(result)
    else:
        print(result)


if __name__ == "__main__":
    main()