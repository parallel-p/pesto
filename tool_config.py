from stats.count_submits import SubmitsCounter
from stats.eq_matrix import EqMatrix
from stats.max_test_cases_count import MaxTestCasesCount
from stats.same_runs import SameRunsKirov, SameRunsACM, SameRunsBigStat
from stats.submits_ids_by_signature_visitor import SubmitsIdsBySignatureVisitor
from stats.submits_over_test_cases_numbers import SubmitsOverTestCasesNumbers
from pickle_submits import PickleWriter
from visitor_factory import VisitorFactory
from sharding_visitor import ShardingByContestVisitor
from sharding_visitor import ShardingByProblemVisitor
from sharding_visitor import ShardingByLangVisitor
from sharding_visitor import ShardingByScoringVisitor
from elector_visitor import ElectorByMaxCasesVisitor
from visitor import Visitor
from os import path


def get_presets_info():
    return """
        1.count_submits - Counts number of submits for each problem.
        2.eq_matrix - Creates matrix for each problem which contains how many times cases were launched together.
        3.same_runs - Counts for each problem lists of runs that were launched together.
        4.submits_by_signature - Counts submits with each outcome for each problem for each language.
        5.submits_by_tests - Counts submits with each number of launched tests for each problem.
        6.same_runs_big_stat - Counts for all problem lists of runs that were launched together.
        7.gen_pickles - Generates fast access information for next use.
    """

def sharder_wrap(visitor, sharders):
    sharders = list(map(str.capitalize, sharders.split()))
    visitor = ClassFactory(visitor)
    for sharder in sharders[::-1]:
        sharder_class = globals()['ShardingBy{}Visitor'.format(sharder)]
        visitor = ClassFactory(sharder_class, visitor)
    return visitor.create()


def get_visitor_by_preset(preset, output, no_lang_sharding=False):
    if preset in ['1', 'count_submits']:
        return sharder_wrap(SubmitsCounter, 'contest')
    if preset in ['2', 'eq_matrix']:
        return sharder_wrap(EqMatrix, 'scoring contest problem')
    if preset in ['3', 'same_runs']:
        return sharder_wrap(SameRuns, 'scoring contest problem')
    if preset in ['4', 'submits_by_signature']:
        return sharder_wrap(SubmitsIdsBySignatureVisitor, 'contest problem' + ('' if no_lang_sharding else ' lang'))
    if preset in ['5', 'submits_by_tests']:
        return SubmitsOverTestCasesNumbers()
    if preset in ['6', 'same_runs_big_stat']:
        return SameRunsBigStat()  # this does not work properly, however
    if preset in ['7', 'gen_pickles']:
        writer = PickleWriter()
        writer.default_path = path.join('.', output)
        return writer
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

class ClassFactory(VisitorFactory):
    def __init__(self, klass, *params):
        self.klass = klass
        self.params = params

    def create(self, *args):
        return self.klass(*self.params)
