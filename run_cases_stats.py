from argparse import ArgumentParser
from case_counter import CasesCounter
from find_same_problems import SameProblemsFinder
from find_similar_problems import SimilarProblemsFinder
from problem_generator import problem_generator
import os


def display_stats_list():
    print('Statistics list:')
    print('0. cases_count - Count cases for each problem.')
    print('1. same_problems - Find same problems.')
    print('2. similar_problems - Find similar problems (problems with many same tests)')


parser = ArgumentParser(description='Run cases-based statistic.')
parser.add_argument('-m', '--multicontest', help='contest_dir contains several contests.', action='store_true')
parser.add_argument('contest_dir', help='Name of a directory with contest files', type=str)
parser.add_argument('statistic', help='Name of statistic to run.', nargs='?', type=str)
args = vars(parser.parse_args())

if 'statistic' not in args:
    display_stats_list()
    exit()

if not os.path.isdir(args['contest_dir']):
    print('Please, specify correct directory.')
    exit()

contest_dirs = [args['contest_dir']]

if args['multicontest']:
    contest_dirs = os.listdir(args['contest_dir'])
    for i in range(len(contest_dirs)):
        contest_dirs[i] = os.path.join(args['contest_dir'], contest_dirs[i])

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