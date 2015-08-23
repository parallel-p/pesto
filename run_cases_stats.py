#!/usr/bin/python3

from argparse import ArgumentParser
from case_counter import CasesCounter
from find_same_problems import SameProblemsFinder
from find_similar_problems import SimilarProblemsFinder
from problem_generator import sqlite_problem_generator, sqlite_contest_generator
from problems_tree import ProblemsTree
from tree_drawer import TreeDrawer
from stats.contests_grouper import ContestsGrouper
import problems_tree_json
import sqlite_connector
import toollib


def display_stats_list():
    print('Statistics list:')
    print('0. cases_count - Count cases for each problem.')
    print('1. same_problems - Find same problems.')
    print('2. similar_problems - Find similar problems (problems with many same tests)')
    print('3. draw_tree - Build tree of similar problems and draw it to file')
    print('4. build_problems_tree - Build tree of similar problems and write it to json file')
    print('5. draw_saved_tree - load tree from json and draw it to file')


def parse_args():
    parser = ArgumentParser(description='Run cases-based statistic.')
    toollib.parse_args_input(parser)
    parser.add_argument('--tree-json', help="saved tree (only for draw_saved_tree)")
    toollib.parse_args_output(parser)
    toollib.parse_args_config(parser)
    parser.add_argument('statistic', help='Name of statistic to run.', nargs='?', type=str)
    return vars(parser.parse_args())


def print_result(result, filename):
    if filename is None:
        print(result)
    else:
        with open(filename, 'w') as outfile:
            outfile.write(result)


def main():
    args = parse_args()
    
    config_name = args['cfg'] if args['cfg'] else 'config.ini'
    output_file = args['output'] if args['output'] else None

    config = toollib.read_config(config_name, 'cases_stats')
    if config is None:
        print('Incorrect config specified.')
        exit()

    if args['statistic'] is None:
        display_stats_list()
        exit()

    use_database = (args['statistic'] not in ['5', 'draw_saved_tree'])

    if use_database:
        sqlite_db = args['database'] if args['database'] else config.get('database')
        if sqlite_db is None:
            print('Database is not specified.')
            exit()
        conn = sqlite_connector.SQLiteConnector()
        conn.create_connection(sqlite_db)
        problems_generator = sqlite_problem_generator(conn)
        contests_generator = sqlite_contest_generator(conn)

    if args['statistic'] in ['0', 'cases_count']:
        counter = CasesCounter(problems_generator)
        print_result(str(counter), output_file)
    elif args['statistic'] in ['1', 'same_problems']:
        finder = SameProblemsFinder(problems_generator)
        print_result(str(finder), output_file)
    elif args['statistic'] in ['2', 'similar_problems']:
        finder = SimilarProblemsFinder(problems_generator)
        print_result(str(finder), output_file)
    elif args['statistic'] in ['3', 'draw_tree']:
        if output_file is None:
            print('Sorry, I can\'t draw tree to console')
            exit()
        contests_grouper = ContestsGrouper(contests_generator)
        contests = contests_grouper.get_contests_sorted()
        contest_to_problems = dict()
        for contest in contests:
            contest_to_problems[contest.contest_id] = []
        for problem in problems_generator:
            contest_id = problem.problem_id[0]
            if contest_id in contest_to_problems:
                contest_to_problems[contest_id].append(problem)
        problems = []
        for contest in contests:
            problems += contest_to_problems[contest.contest_id]
        tree = ProblemsTree(problems)
        drawer = TreeDrawer(tree, contests_grouper)
        drawer.save_image_to_file(output_file)
    elif args['statistic'] in ['4', 'build_problems_tree']:
        contests_grouper = ContestsGrouper(contests_generator)
        contests = contests_grouper.get_contests_sorted()
        contest_to_problems = dict()
        for contest in contests:
            contest_to_problems[contest.contest_id] = []
        for problem in problems_generator:
            contest_id = problem.problem_id[0]
            if contest_id in contest_to_problems:
                contest_to_problems[contest_id].append(problem)
        problems = []
        for contest in contests:
            problems += contest_to_problems[contest.contest_id]
        tree = ProblemsTree(problems)
        print_result(problems_tree_json.save_tree(tree, contests_grouper), output_file)
    elif args['statistic'] in ['5', 'draw_saved_tree']:
        if output_file is None:
            print('Sorry, I can\'t draw tree to console')
            exit()
        saved_tree_filename = args['tree_json']
        if not saved_tree_filename:
            print('Saved tree file is not specified')
            exit()
        with open(saved_tree_filename, 'r') as saved_tree_file:
            tree, contests_grouper = problems_tree_json.load_tree(saved_tree_file.read())
        drawer = TreeDrawer(tree, contests_grouper)
        drawer.save_image_to_file(output_file)
    else:
        print('Incorrect statistic specified.')
        display_stats_list()


if __name__ == '__main__':
    main()
