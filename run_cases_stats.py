from argparse import ArgumentParser
from case_counter import CasesCounter
from find_same_problems import SameProblemsFinder
from find_similar_problems import SimilarProblemsFinder
from problem_generator import problem_generator
from walker import MultipleContestWalker
import os
import configparser
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
    
    config_name = args['cfg'] if args['cfg'] else 'default.ini'

    config = toollib.read_config(config_name, 'cases_stats')
    if config is None:
        print('Incorrect config specified.')
        exit()

    if args['statistic'] is None:
        display_stats_list()
        exit()

    try:
        base_dir = args['dir'] if args['dir'] else config['base_dir']
    except KeyError:
        print('Invalid config, see config.ini.example')
        exit()

    if not os.path.isdir(base_dir):
        print('Incorrect dir specified.')
        exit()

    if args['multicontest']:
        contest_dirs = MultipleContestWalker().walk(base_dir)
    else:
        contest_dirs = [base_dir]

    if args['statistic'] in ['0', 'cases_count']:
        counter = CasesCounter(problem_generator(contest_dirs))
        print(str(counter))
    elif args['statistic'] in ['1', 'same_problems']:
        finder = SameProblemsFinder(problem_generator(contest_dirs))
        print(str(finder))
    elif args['statistic'] in ['2', 'similar_problems']:
        finder = SimilarProblemsFinder(problem_generator(contest_dirs))
        print(str(finder))
    else:
        print('Incorrect statistic specified.')
        display_stats_list()

if __name__ == '__main__':
    main()