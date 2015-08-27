#!/usr/bin/python3
import argparse
import logging

from dao import ContestsDAO, ProblemsDAO
import tool_config
from dao_submits import DAOSubmits
import toollib
from sqlite_connector import SQLiteConnector


def parse_args():
    parser = argparse.ArgumentParser(description="Load database and calculate some statistics")
    toollib.parse_args_config(parser)
    toollib.parse_args_input(parser)
    toollib.parse_args_output(parser)
    toollib.parse_args_filters(parser)

    parser.add_argument('--scoring', help="contest scoring (acm, kirov)", nargs='?')
    parser.add_argument('--no-lang-sharding', help="do not shard by language in submits_by_signature", action="store_true")
    parser.add_argument('preset_name', help="name or number of statistics preset", nargs='?')


    return vars(parser.parse_args())


def get_arguments():
    args, config = parse_args(), None
    cfg_name = args['cfg'] or 'config.ini'
    try:
        config = toollib.read_config(cfg_name, 'tool')
    except KeyError:
        print('Incorrect config')
        exit()
    toollib.init_logging(cfg_name)

    output, database_filename, scoring = None, None, None
    try:
        output = (args['output'] if args['output'] else config['output']) if not args['console'] else None
        output = output.rstrip('/').rstrip('\\') if output else None
        database_filename = args['database'] if args['database'] else config['database']
        scoring = (args['scoring'] if args['scoring'] else config.get('scoring'))
    except KeyError:
        print('Invalid config, see config.ini.example')
        exit()
    if database_filename is None:
        print('Database file is not defined.')
        exit()
    if scoring:
        scoring = scoring.upper()
        if scoring == 'ALL':
            scoring = None
        elif scoring not in ('KIROV', 'ACM'):
            print('Unknown scoring: ' + scoring)
            exit()

    stats_counter = tool_config.get_visitor_by_preset(args['preset_name'], output, args['no_lang_sharding'])
    if stats_counter is None:
        if args['preset_name']:
            print('Preset name "{}" is not defined or invalid.'.format(args['preset_name']))
        print('Presets available:', tool_config.get_presets_info())
        exit()

    optional = dict()
    is_pickle_writer = False
    if args['preset_name'] in ['7', 'gen_pickles']:
        is_pickle_writer = True

    if output and not (args['preset_name'] in ['7', 'gen_pickles']):
        optional['outfile'] = output
    if args['preset_name'] in ['7', 'gen_pickles']:
        optional['preset_name'] = 'gen_pickles'
    else:
        optional['preset_name'] = args['preset_name']
    optional['filter_problem'] = args['filter_problem']
    optional['filter_contest'] = args['filter_contest']

    return database_filename, stats_counter, optional, scoring, is_pickle_writer

def count_stat(connector, scoring, visitor, optional):
    problem_cursor = connector.get_cursor()
    submit_cursor = connector.get_cursor()
    no_scoring = scoring is None
    if no_scoring:
        contest_cursor = connector.get_cursor()
    dao_submits = DAOSubmits(connector)
    dao_problems = ProblemsDAO(connector)
    query = ('SELECT problems.id, contest_ref, problem_id, problems.name '
                                              'FROM Problems, Contests '
                                              'WHERE Contests.id=Problems.contest_ref {} ORDER BY contest_id')
    args = []
    if scoring:
        query = query.format('AND scoring=? {}')
        args.append(scoring)
    if optional['filter_contest']:
        query = query.format('AND Contests.contest_id=? {}')
        args.append(optional['filter_contest'].rjust(6, '0'))
    if optional['filter_problem']:
        query = query.format('AND Problems.problem_id=? {}')
        args.append(optional['filter_problem'])
    query = query.format('')
    for problem_row in problem_cursor.execute(query, args):
        problem = dao_problems.deep_load(problem_row)
        logging.info('Processing problem {} from contest {}'.format(problem.problem_id[1], problem.problem_id[0]))
        if no_scoring:
            contest_row = contest_cursor.execute('SELECT {} FROM Contests WHERE Contests.id=?'.format(ContestsDAO.columns), (problem_row['contest_ref'],)).fetchone()
            scoring = ContestsDAO.load(contest_row).scoring
            logging.debug('Scoring is {}'.format(scoring))
        for submit_row in submit_cursor.execute('SELECT * '
                                                'FROM Submits '
                                                'WHERE problem_ref=?', (problem_row['id'], )):
            submit = dao_submits.deep_load(submit_row)
            submit.problem_id = problem.problem_id
            submit.scoring = scoring.upper()
            visitor.visit(submit)
    visitor.close()
    return visitor


def pickles_mod(connector, visitor):
    problem_cursor = connector.get_cursor()
    submit_cursor = connector.get_cursor()

    dao_submits = DAOSubmits(connector)
    dao_problems = ProblemsDAO(connector)

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
    database_filename, visitor, optional, scoring, is_pickle = get_arguments()

    connector = SQLiteConnector()
    connector.create_connection(database_filename)
    if is_pickle:
        pickles_mod(connector, visitor)
    else:
        stat = count_stat(connector, scoring, visitor, optional)
        result = stat.pretty_print()
        if 'outfile' in optional:
            with open(optional['outfile'], 'w') as outfile:
                outfile.write(result)
        else:
            print(result)

    connector.close_connection()

if __name__ == "__main__":
    main()
