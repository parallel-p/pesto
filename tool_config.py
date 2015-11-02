from stats.eq_matrix import EqMatrix
from stats.max_test_cases_count import MaxTestCasesCount
from stats.same_runs import SameRunsKirov, SameRunsACM, SameRunsBigStat
from stats.submits_ids_by_signature_visitor import SubmitsIdsBySignatureVisitor
from stats.submits_over_test_cases_numbers import SubmitsOverTestCasesNumbers
from find_same_problems import SameProblemsFinder
from find_similar_problems import SimilarProblemsFinder
from case_counter import CasesCounter
from sharding_visitor import ShardingByContestVisitor
from sharding_visitor import ShardingByProblemVisitor
from sharding_visitor import ShardingByLangVisitor
from sharding_visitor import ShardingByScoringVisitor
from elector_visitor import ElectorByMaxCasesVisitor
from visitor import Visitor
from os import path
from statistics import Statistics, SubmitStatistics, ProblemStatistics
from shard import shard
from stats.contests_grouper import ContestsGrouper
from problems_tree import ProblemsTree
import problems_tree_json
from problem_generator import sqlite_contest_generator
import logging

all_stats = [None,
    'StatCountSubmits',
    'StatEqMatrix',
    'StatSameRuns',
    'StatSubmitsBySignature',
    'StatSubmitsByTests',
    'StatCasesCount',
    'StatSameProblems',
    'StatSimilarProblems',
    'StatBuildTree',
    'StatDrawTree',
    'StatBuildDrawTree',
]


class StatCountSubmits(ProblemStatistics):

    _name = 'count_submits'
    _desc = 'Counts number of submits for each problem.'

    def get_input_data(self, connection):
        cursor = connection.get_cursor()
        for problem in super().get_input_data(connection):
            yield (problem.problem_id, next(cursor.execute('SELECT COUNT(*) FROM Submits WHERE problem_ref=?', (problem.db_id,)))[0])

    def calc(self, data):
        data = list(data)
        self.result = {}
        for i in data:
            self.result[i[0]] = self.result.get(i[0], 0) + i[1]

    def as_string(self):
        data = {i:'Problem #{}: {} submits'.format(i[1], self.result[i]) for i in self.result}
        return shard(data, [(lambda x:x[0], lambda x:'Contest #{}'.format(x))], key=lambda x:int(x[1]))

class StatEqMatrix(SubmitStatistics):

    _name = 'eq_matrix'
    _desc = 'Creates matrix for each problem which contains how many times cases were launched together.'

    def _create_visitor(self):
        return sharder_wrap(EqMatrix, 'scoring contest problem')

class StatSameRuns(SubmitStatistics):

    _name = 'same_runs'
    _desc = 'Counts for each problem lists of runs that were launched together.'

    def _create_visitor(self):
        return sharder_wrap(SameRuns, 'scoring contest problem')

class StatSubmitsBySignature(SubmitStatistics):

    _name = 'submits_by_signature'
    _desc = 'Counts submits with each outcome for each problem (for each language).'

    def _create_visitor(self):
        SubmitsIdsBySignatureVisitor.min_submits = self.extra.get('min_submits', 0)
        return sharder_wrap(SubmitsIdsBySignatureVisitor, 'contest problem lang' if 'lang_sharding' in self.extra else 'contest problem')

class StatSubmitsByTests(SubmitStatistics):

    _name = 'submits_by_tests'
    _desc = 'Counts submits with each number of launched tests for each problem.'

    def _create_visitor(self):
         return sharder_wrap(SubmitsOverTestCasesNumbers, 'contest')

class StatCasesCount(ProblemStatistics):

    _name = 'cases_count'
    _desc = 'Count cases for each problem.'

    counter_class = CasesCounter

class StatSameProblems(ProblemStatistics):

    _name = 'same_problems'
    _desc = 'Find same problems.'

    counter_class = SameProblemsFinder

class StatSimilarProblems(ProblemStatistics):

    _name = 'similar_problems'
    _desc = 'Find similar problems (problems with many same tests)'

    counter_class = SimilarProblemsFinder

class StatBuildTree(ProblemStatistics):

    _name = 'build_tree_json'
    _desc = 'Build tree of similar problems and write it to json file.'

    def get_input_data(self, connection):
        problems = list(super().get_input_data(connection))
        contests = list(sqlite_contest_generator(connection))
        return problems, contests


    def calc(self, data):
        problems, contests = data
        cg = ContestsGrouper(contests)
        contests = cg.get_contests_sorted()
        contest_to_problems = dict()
        for contest in contests:
            contest_to_problems[contest.contest_id] = []
        for problem in problems:
            contest_id = problem.problem_id[0]
            if contest_id in contest_to_problems:
                contest_to_problems[contest_id].append(problem)
        problems = []
        for contest in contests:
            problems += contest_to_problems[contest.contest_id]
        tree = ProblemsTree(problems)
        self.result = problems_tree_json.save_tree(tree, cg, 'pretty_json' in self.extra)

class StatDrawTree(Statistics):

    _name = 'draw_saved_tree'
    _desc = 'Load tree from json and draw it to file.'

    def _get_json(self):
        saved_tree_filename = self.extra.get('tree_json')
        if not saved_tree_filename:
            print('Saved tree file is not specified')
            exit()  # TODO something more clever here
        with open(saved_tree_filename) as saved_tree_file:
            data = result = saved_tree_file.read()
        return data

    def save_to_file(self, filename):
        if filename is None:
            print('Sorry, I can\'t draw tree to console')
            return
        tree, contests_grouper = problems_tree_json.load_tree(self._get_json())
        from tree_drawer import TreeDrawer
        drawer = TreeDrawer(tree, contests_grouper)  # TODO "saving..." when all lines are located
        drawer.save_image_to_file(filename)

class StatBuildDrawTree(StatBuildTree, StatDrawTree):  # sorry

    _name = 'draw_tree'
    _desc = 'Build tree of similar problems and draw it to file.'

    def _get_json(self):
        return self.result  # TODO do not convert json to string

def sharder_wrap(visitor, sharders):
    sharders = list(map(str.capitalize, sharders.split()))
    visitor = ClassFactory(visitor)
    for sharder in sharders[::-1]:
        sharder_class = globals()['ShardingBy{}Visitor'.format(sharder)]
        visitor = ClassFactory(sharder_class, visitor)
    return visitor.create()


def get_presets_info():
    res = []
    for i, stat in enumerate(all_stats):
        if not stat:
            continue
        stat_class = globals().get(stat)
        if not stat_class:
            logging.error('Invalid statistics: ' + stat)
            continue
        res.append((str(i).rjust(2), stat_class._name, stat_class._desc))
    max_width = max(len(i[1]) for i in res)
    pretty_res = ['']
    for i in res:
        pretty_res.append('{}. {} - {}'.format(i[0], i[1].ljust(max_width), i[2]))
    pretty_res.append('')
    return '\n'.join(pretty_res)

def get_stat_by_preset(preset):
    preset = str(preset).strip().lower()
    if preset.isdigit():
        try:
            return globals()[all_stats[int(preset)]]
        except Exception:
            return None
    for stat in all_stats:
        if not stat:
            continue
        stat_class = globals().get(stat)
        if stat_class._name == preset:
            return stat_class
    return None

class SameRuns(Visitor):

    def __init__(self):
        self.child = None

    def visit(self, submit):
        if not self.child:
            if submit.scoring.upper() == 'ACM':
                self.child = SameRunsACM()
            else:
                self.child = ElectorByMaxCasesVisitor(ClassFactory(SameRunsKirov))
        self.child.visit(submit)

    def get_stat_data(self):
        return self.child.get_stat_data()

    def pretty_print(self):
        return self.child.pretty_print()

class ClassFactory:
    def __init__(self, klass, *params):
        self.klass = klass
        self.params = params

    def create(self, *args):
        return self.klass(*self.params)
