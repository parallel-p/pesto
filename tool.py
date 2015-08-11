import tool_config
import argparse
import filter_visitor
import walker
import toollib
from sqlite_connector import SQLiteConnector
from ejudge_database import EjudgeDatabase


def parse_args():
    parser = argparse.ArgumentParser(description="Load database and calculate some statistics")
    toollib.parse_args_config(parser)
    toollib.parse_args_input(parser)
    toollib.parse_args_output(parser)
    toollib.parse_args_filters(parser)

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
        config = dict(pickle_dir='pickle', database=None, base_dir=None, trash='trash', output='output.txt')

    output, csv_filename = None, None
    try:
        output = (args['output'] if args['output'] else config['output']) if not args['console'] else None
        output = output.rstrip('/').rstrip('\\') if output else None
        csv_filename = args['database'] if args['database'] else config['database']
    except KeyError:
        print('Invalid config, see config.ini.example')
        exit()
    if csv_filename is None:
        print('Database file is not defined.')
        exit()
    stats_counter = tool_config.get_visitor_by_preset(args['preset_name'], output)
    if stats_counter is None:
        print('Preset name is not defined or invalid.')
        print('Presets available:', tool_config.get_presets_info())
        exit()

    optional = dict()
    if output and not (args['preset_name'] in ['7', 'gen_pickles']):
        optional['outfile'] = output
    if args.get('filter_problem'):
        optional['filter_problem'] = args['filter_problem']
    if args.get('filter_user'):
        optional['filter_user'] = args['filter_user']
    if args.get('filter_contest'):
        optional['filter_contest'] = args['filter_contest']

    return csv_filename, stats_counter, optional


def main():
    database_filename, visitor, optional = get_arguments()
    if 'filter_user' in optional:
        visitor = filter_visitor.FilterByUserVisitor(visitor, optional['filter_user'])
    if 'filter_problem' in optional:
        visitor = filter_visitor.FilterByProblemVisitor(visitor, optional['filter_problem'])
    if 'filter_contest' in optional:
        visitor = filter_visitor.FilterByContestVisitor(visitor, optional['filter_contest'])

    connector = SQLiteConnector()
    sqlite_cursor = connector.create_connection(database_filename)
    ej_db = EjudgeDatabase(sqlite_cursor)

    # Here we need to get all submits and visit it
    """for contest in contest_walker.walk(base_dir):
        if is_problems:
            obj_loader = walker.ProblemWalker()
            for problem in obj_loader.walk(contest[1]):
                #problem processing
                print(problem)
        if is_submits:
            obj_loader = walker.SubmitWalker(ej_db)
            if not is_pickle:
                obj_loader.contest_id = contest[0]
            for file in file_walker.walk(contest[1]):
                for submit in obj_loader.walk(file[1]):
                    if submit:
                        visitor.visit(submit)"""

    connector.close_connection()

    result = visitor.pretty_print()
    visitor.close()
    if 'outfile' in optional:
        with open(optional['outfile'], 'w') as outfile:
            outfile.write(result)
    else:
        print(result)


if __name__ == "__main__":
    main()