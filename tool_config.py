from stats.eq_matrix import EqMatrix
from stats.max_test_cases_count import MaxTestCasesCount
from stats.same_runs import SameRunsKirov, SameRunsACM, SameRunsBigStat
from stats.submits_ids_by_signature_visitor import SubmitsIdsBySignatureVisitor
from stats.submits_over_test_cases_numbers import SubmitsOverTestCasesNumbers
from find_same_problems import SameProblemsFinder
from find_similar_problems import SimilarProblemsFinder
from find_elephants import FindElephants
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
from tree_drawer import TreeDrawer


def get_presets_info():
    return """
        1. count_submits - Counts number of submits for each problem.
        2. eq_matrix - Creates matrix for each problem which contains how many times cases were launched together.
        3. same_runs - Counts for each problem lists of runs that were launched together.
        4. submits_by_signature - Counts submits with each outcome for each problem for each language.
        5. submits_by_tests - Counts submits with each number of launched tests for each problem.
        6. same_runs_big_stat - Counts for all problem lists of runs that were launched together.
        7. cases_count - Count cases for each problem.
        8. same_problems - Find same problems.
        9. similar_problems - Find similar problems (problems with many same tests).
        10. build_tree - Build tree of similar problems and write it to json file.
        11. draw_tree - Build tree of similar problems and draw it to file.
        12. draw_saved_tree - load tree from json and draw it to file.
        13. find_elephants - find problems with the same inputs and outputs.
    """

class StatCountSubmits(ProblemStatistics):

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

    def _create_visitor(self):
        return sharder_wrap(EqMatrix, 'scoring contest problem')

class StatSameRuns(SubmitStatistics):

    def _create_visitor(self):
        return sharder_wrap(SameRuns, 'scoring contest problem')

class StatSubmitsBySignature(SubmitStatistics):

    def _create_visitor(self):
        SubmitsIdsBySignatureVisitor.min_submits = self.min_submits
        return sharder_wrap(SubmitsIdsBySignatureVisitor, 'contest problem')

class StatSubmitsBySignatureLang(SubmitStatistics):  # kostil

    def _create_visitor(self):
        SubmitsIdsBySignatureVisitor.min_submits = self.min_submits
        return sharder_wrap(SubmitsIdsBySignatureVisitor, 'contest problem lang')

class StatSubmitsByTests(SubmitStatistics):

    def _create_visitor(self):
         return sharder_wrap(SubmitsOverTestCasesNumbers, 'contest')

class StatCasesCount(ProblemStatistics):
    counter_class = CasesCounter

class StatSameProblems(ProblemStatistics):
    counter_class = SameProblemsFinder

class StatSimilarProblems(ProblemStatistics):
    counter_class = SimilarProblemsFinder

class StatBuildTree(ProblemStatistics):
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
        drawer = TreeDrawer(tree, contests_grouper)  # TODO "saving..." when all lines are located
        drawer.save_image_to_file(filename)

class StatBuildDrawTree(StatBuildTree, StatDrawTree):  # sorry
    def _get_json(self):
        return self.result  # TODO do not convert json to string

class StatFindElephants(ProblemStatistics):
    counter_class = FindElephants

def sharder_wrap(visitor, sharders):
    sharders = list(map(str.capitalize, sharders.split()))
    visitor = ClassFactory(visitor)
    for sharder in sharders[::-1]:
        sharder_class = globals()['ShardingBy{}Visitor'.format(sharder)]
        visitor = ClassFactory(sharder_class, visitor)
    return visitor.create()

def get_stat_by_preset(preset, extra):
    if preset in ['1', 'count_submits']:
        return StatCountSubmits
    if preset in ['2', 'eq_matrix']:
        return StatEqMatrix
    if preset in ['3', 'same_runs']:
        return StatSameRuns
    if preset in ['4', 'submits_by_signature']:
        cl =  StatSubmitsBySignatureLang if 'lang_sharding' in extra else StatSubmitsBySignature
        cl.min_submits = extra.get('min_submits', 0)  # TODO find a better solution
        return cl
    if preset in ['5', 'submits_by_tests']:
        return StatSubmitsByTests
    if preset in ['6', 'same_runs_big_stat']:  # TODO something here
        print('gg')
        exit()
    if preset in ['7', 'cases_count']:
        return StatCasesCount
    if preset in ['8', 'same_problems']:
        return StatSameProblems
    if preset in ['9', 'similar_problems']:
        return StatSimilarProblems
    if preset in ['10', 'build_tree']:
        return StatBuildTree
    if preset in ['11', 'draw_saved_tree']:
        return StatDrawTree
    if preset in ['12', 'draw_tree']:
        return StatBuildDrawTree
    if preset in ['13', 'find_elephants']:
        return StatFindElephants


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
