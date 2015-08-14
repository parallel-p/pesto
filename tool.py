import tool_config
import argparse
from dao_problems import DAOProblems
from dao_submits import DAOSubmits
import toollib
from sqlite_connector import SQLiteConnector


def parse_args():
    parser = argparse.ArgumentParser(description="Load database and calculate some statistics")
    toollib.parse_args_config(parser)
    toollib.parse_args_input(parser)
    toollib.parse_args_output(parser)

    parser.add_argument('--scoring', help="contest scoring (acm, kirov)", nargs='?')
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
        try:
            config = toollib.read_config('config.ini', 'tool')
        except KeyError:
            print('Incorrect config.ini')
            exit()

    output, database_filename, scoring = None, None, None
    try:
        output = (args['output'] if args['output'] else config['output']) if not args['console'] else None
        output = output.rstrip('/').rstrip('\\') if output else None
        database_filename = args['database'] if args['database'] else config['database']
        scoring = (args['scoring'] if args['scoring'] else (config['scoring'] if config['scoring'] else 'ACM'))
    except KeyError:
        print('Invalid config, see config.ini.example')
        exit()
    if database_filename is None:
        print('Database file is not defined.')
        exit()
    scoring = scoring.upper()
    if scoring not in ('KIROV', 'ACM'):
        print('Unknown scoring: ' + scoring)
        exit()

    stats_counter = tool_config.get_factory_by_preset(args['preset_name'], output)
    if stats_counter is None:
        print('Preset name "{}" is not defined or invalid.'.format(args['preset_name']))
        print('Presets available:', tool_config.get_presets_info())
        exit()

    optional = dict()
    is_pickle_writer = False
    if args['preset_name'] in ['6', 'gen_pickles']:
        is_pickle_writer = True

    if output and not (args['preset_name'] in ['6', 'gen_pickles']):
        optional['outfile'] = output
    if args['preset_name'] in ['6', 'gen_pickles']:
        optional['preset_name'] = 'gen_pickles'
    else:
        optional['preset_name'] = args['preset_name']

    return database_filename, stats_counter, optional, scoring, is_pickle_writer

def count_stat(connector, scoring, visitor_factory):
    problem_cursor = connector.get_cursor()
    submit_cursor = connector.get_cursor()
    visitor_by_problem = dict()
    dao_submits = DAOSubmits(connector)
    dao_problems = DAOProblems(connector)
    for problem_row in problem_cursor.execute('SELECT problems.id, contest_ref, problem_id, problems.name '
                                              'FROM Problems, Contests '
                                              'WHERE Contests.id=Problems.contest_ref AND scoring=? ORDER BY contest_id', (scoring, )):
        problem = dao_problems.deep_load(problem_row)
        visitor_by_problem[problem] = visitor_factory.create(problem)
        for submit_row in submit_cursor.execute('SELECT * '
                                                'FROM Submits '
                                                'WHERE problem_ref=?', (problem_row['id'], )):
            submit = dao_submits.deep_load(submit_row)
            submit.problem_id = problem.problem_id
            visitor_by_problem[problem].visit(submit)
        visitor_by_problem[problem].close()
    return visitor_by_problem


def pickles_mod(connector, visitor):
    problem_cursor = connector.get_cursor()
    submit_cursor = connector.get_cursor()

    dao_submits = DAOSubmits(connector)
    dao_problems = DAOProblems(connector)

    for problem_row in problem_cursor.execute('SELECT id, contest_ref, problem_id, name '
                                              'FROM Problems '):
        problem = dao_problems.deep_load(problem_row)
        for submit_row in submit_cursor.execute('SELECT * '
                                                'FROM Submits '
                                                'WHERE problem_ref=?', (problem_row['id'], )):
            submit = dao_submits.deep_load(submit_row)
            submit.problem_id = problem.problem_id
            visitor.visit(submit)
        visitor.close()


def main():
    database_filename, visitor_factory, optional, scoring, is_pickle = get_arguments()

    connector = SQLiteConnector()
    connector.create_connection(database_filename)
    if is_pickle:
        pickles_mod(connector, visitor_factory.create(None))
    else:
        stat = count_stat(connector, scoring, visitor_factory)
        result = []
        for problem in stat:
            result.append(stat[problem].pretty_print())
            stat[problem].close()
        result = '\n'.join(result)
        if 'outfile' in optional:
            with open(optional['outfile'], 'w') as outfile:
                outfile.write(result)
        else:
            print(result)

    connector.close_connection()

if __name__ == "__main__":
    main()