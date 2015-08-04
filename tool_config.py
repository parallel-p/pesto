from stats.count_submits import SubmitsCounter
from stats.eq_matrix import EqMatrix
from stats.max_test_cases_count import MaxTestCasesCount
from stats.same_runs import SameRuns
from stats.submits_ids_by_signature_visitor import SubmitsIdsBySignatureVisitor
from stats.submits_over_test_cases_numbers import SubmitsOverTestCasesNumbers
from pickle_submits import PickleWriter
from visitor_factory import VisitorFactory
from sharding_visitor import ShardingByContestVisitor
from sharding_visitor import ShardingByProblemVisitor


def get_presets_info():
    return """
        1.count_submits - Counts number of submits for each problem.
        2.eq_matrix - Creates matrix for each problem which contains how many times cases were launched together.
        3.count_cases - Counts number of cases for each problem.
        4.same_runs - Counts for each problem lists of runs that were launched together.
        5.submits_by_signature - Counts submits with each outcome for each problem.
        6.submits_by_tests - Counts submits with each number of launched tests for each problem.
        7.gen_pickles - Generates fast access information for next use.
    """


def get_visitor_by_preset(preset):
    if preset in ['1', 'count_submits']:
        return ShardingByContestVisitor(SubmitsCounterFactory())
    if preset in ['2', 'eq_matrix']:
        return ShardingByProblemVisitor(EqMatrixFactory())
    if preset in ['3', 'count_cases']:
        return MaxTestCasesCount()
    if preset in ['4', 'same_runs']:
        return SameRuns()
    if preset in ['5', 'submits_by_signature']:
        return ShardingByProblemVisitor(SubmitsIdsBySignatureFactory())
    if preset in ['6', 'submits_by_tests']:
        return SubmitsOverTestCasesNumbers()
    if preset in ['7', 'gen_pickles']:
        return PickleWriter()
    return None


class SubmitsCounterFactory(VisitorFactory):
    def create(self, key):
        return SubmitsCounter()


class EqMatrixFactory(VisitorFactory):
    def create(self, key):
        return EqMatrix()


class SubmitsIdsBySignatureFactory(VisitorFactory):
    def create(self, key):
        return SubmitsIdsBySignatureVisitor()
