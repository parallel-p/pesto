from argparse import ArgumentParser
from case_counter import CasesCounter
from find_same_problems import SameProblemsFinder
from find_similar_problems import SimilarProblemsFinder
from problem_generator import problem_generator, sqlite_problem_generator
import toollib


def display_stats_list():
    print('Statistics list:')
    print('0. cases_count - Count cases for each problem.')
    print('1. same_problems - Find same problems.')
    print('2. similar_problems - Find similar problems (problems with many same tests)')


def parse_args():
    parser = ArgumentParser(description='Run cases-based statistic.')
    toollib.parse_args_input(parser)
    toollib.parse_args_output(parser)
    toollib.parse_args_config(parser)
    parser.add_argument('statistic', help='Name of statistic to run.', nargs='?', type=str)
    return vars(parser.parse_args())


def main():
    args = parse_args()
    
    config_name = args['cfg'] if args['cfg'] else 'config.ini'

    config = toollib.read_config(config_name, 'cases_stats')
    if config is None:
        print('Incorrect config scpecifed.')
        exit()

    if args['statistic'] is None:
        display_stats_list()
        exit()

    sqlite_db = args['database'] if args['database'] else config.get('database')

    if sqlite_db is None:
        print('Database is not specified.')
        exit()

    generator = sqlite_problem_generator(sqlite_db)

    if args['statistic'] in ['0', 'cases_count']:
        counter = CasesCounter(generator)
        print(str(counter))
    elif args['statistic'] in ['1', 'same_problems']:
        finder = SameProblemsFinder(generator)
        print(str(finder))
    elif args['statistic'] in ['2', 'similar_problems']:
        finder = SimilarProblemsFinder(generator)
        print(str(finder))
    else:
        print('Incorrect statistic specified.')
        display_stats_list()


if __name__ == '__main__':
    main()
