from stats.count_submits import SubmitsCounter
from stats.eq_matrix import EqMatrix
from stats.max_test_cases_count import MaxTestCasesCount
from stats.same_runs import SameRunsKirov, SameRunsACM
from stats.submits_ids_by_signature_visitor import SubmitsIdsBySignatureVisitor
from stats.submits_over_test_cases_numbers import SubmitsOverTestCasesNumbers
from pickle_submits import PickleWriter
from visitor_factory import VisitorFactory
from sharding_visitor import ShardingByContestVisitor
from sharding_visitor import ShardingByProblemVisitor
from sharding_visitor import ShardingByLangVisitor
from sharding_visitor import ShardingByScoringVisitor
from elector_visitor import ElectorByMaxCasesVisitor
from os import path


def get_presets_info():
    return """
        1.count_submits - Counts number of submits for each problem.
        2.eq_matrix - Creates matrix for each problem which contains how many times cases were launched together.
        3.same_runs - Counts for each problem lists of runs that were launched together.
        4.submits_by_signature - Counts submits with each outcome for each problem for each language.
        5.submits_by_tests - Counts submits with each number of launched tests for each problem.
        6.gen_pickles - Generates fast access information for next use.
    """


def get_factory_by_preset(preset, output):
    if preset in ['1', 'count_submits']:
        return CustomShardingFactory(ShardingByContestVisitor, SubmitsCounterFactory)
    if preset in ['2', 'eq_matrix']:
        return CustomShardingFactory(ShardingByScoringVisitor, EqMatrixShardingByProblem)
    if preset in ['3', 'same_runs']:
        return CustomShardingFactory(ShardingByScoringVisitor, SameRunsFactory)
    if preset in ['4', 'submits_by_signature']:
        return CustomShardingFactory(ShardingByProblemVisitor, SubmitsIdsBySignatureFactory)
    if preset in ['5', 'submits_by_tests']:
        return CustomVisitorFactory(SubmitsOverTestCasesNumbers)
    if preset in ['6', 'gen_pickles']:
        default_path = path.join('.', output)
        return PickleWriterFactory(default_path)
    return None


class PickleWriterFactory(VisitorFactory):
    def __init__(self, default_path):
        self.default_path = default_path

    def create(self, key):
        result = PickleWriter()
        result.default_path = self.default_path
        return result

class CustomShardingFactory(VisitorFactory):
    def __init__(self, sharding_class, visitor_factory_class):
        self.sharding_class = sharding_class
        self.visitor_factory_class = visitor_factory_class

    def create(self, key):
        return self.sharding_class(self.visitor_factory_class())

class CustomVisitorFactory(VisitorFactory):
    def __init__(self, visitor_class):
        self.visitor_class = visitor_class

    def create(self, key):
        return self.visitor_class()

class SameRunsFactory(VisitorFactory):
    def create(self, key):
        if key == 'ACM':
            return ShardingByProblemVisitor(SameRunsACMFactory())
        else:
            return ShardingByProblemVisitor(SameRunsKirovFactory())


class EqMatrixShardingByProblem(VisitorFactory):
    def create(self, key):
        return ShardingByProblemVisitor(EqMatrixFactory())


class SameRunsACMFactory(VisitorFactory):
    def create(self, key):
        return SameRunsACM()


class SameRunsKirovFactory(VisitorFactory):
    def create(self, key):
        return ElectorByMaxCasesVisitor(SameRunsKirovFactory2())


class SameRunsKirovFactory2(VisitorFactory):
    def create(self, key):
        return SameRunsKirov()


class SubmitsCounterFactory(VisitorFactory):
    def create(self, key):
        return SubmitsCounter()


class MaxTestCasesCountFactory(VisitorFactory):
    def create(self, key):
        return MaxTestCasesCount()


class EqMatrixFactory(VisitorFactory):
    def create(self, key):
        return EqMatrix()


class SubmitsIdsBySignatureFactory(VisitorFactory):
    def create(self, key):
        return ShardingByLangVisitor(SubmitsIdsBySignatureFactory2())


class SubmitsIdsBySignatureFactory2(VisitorFactory):
    def create(self, key):
        return SubmitsIdsBySignatureVisitor()
