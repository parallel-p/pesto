import unittest
from unittest.mock import Mock

from sharding_visitor import ShardingVisitor

from sharding_visitor import ShardingByProblemVisitor
from sharding_visitor import ShardingByContestVisitor
from sharding_visitor import ShardingByUserVisitor
from sharding_visitor import ShardingByLangVisitor
from sharding_visitor import ShardingByScoringVisitor
from model import Submit




class FunctionTesting(unittest.TestCase):
    def setUp(self):
        self.shard_visitor = ShardingVisitor(Mock(create=lambda x:Mock()))

    def test_empty_output(self):
        self.assertEqual(self.shard_visitor.pretty_print(), "")

    def test_empty_data(self):
        self.assertEqual(self.shard_visitor.get_stat_data(), [])

    def test_comparable_key(self):
        self.assertEqual(self.shard_visitor._comparable_key('042'), 42)
        self.assertEqual(self.shard_visitor._comparable_key('abc'), 'abc')
        self.assertEqual(self.shard_visitor._comparable_key((1, 2)), (1, 2))
        self.shard_visitor.comparable_key = Mock(return_value=42)
        self.assertEqual(self.shard_visitor._comparable_key('anything'), 42)
        self.shard_visitor.comparable_key = Mock(side_effect=Exception)
        self.assertEqual(self.shard_visitor._comparable_key('42'), '42')

    def test_enum_visitors(self):
        self.shard_visitor.visitors['10'] = 1
        self.shard_visitor.visitors['2'] = 2
        self.assertEqual(list(self.shard_visitor._enum_visitors()), [('2', 2), ('10', 1)])
        self.shard_visitor.visitors['a'] = 3
        self.assertEqual(list(self.shard_visitor._enum_visitors()), [('10', 1), ('2', 2), ('a', 3)])

    def test_one_visitors(self):
        self.shard_visitor.visit(10)
        self.shard_visitor.visitors['10'].visit.assert_called_once_with(10)

    def test_two_visitors(self):
        for i in range(2):
            self.shard_visitor.visit(10)
        self.shard_visitor.visit(20)
        self.shard_visitor.visitors['10'].visit.assert_called_with(10)
        self.shard_visitor.visitors['20'].visit.assert_called_once_with(20)

    def test_raw_stats(self):
        self.shard_visitor.visitors['1'] = Mock(get_stat_data=Mock(return_value=1))
        self.shard_visitor.visitors['2'] = Mock(get_stat_data=Mock(return_value=2))
        self.assertEqual(self.shard_visitor.get_stat_data(), [('1', 1), ('2', 2)])

    def test_pretty_key(self):
        self.assertEqual(self.shard_visitor.pretty_key(5), '5')
        self.shard_visitor.visit(10)

    def test_pretty_print(self):
        self.shard_visitor.visitors['10'] = Mock(pretty_print=Mock(return_value='A'))
        self.shard_visitor.visitors['b'] = Mock(pretty_print=Mock(return_value=''))
        self.shard_visitor.visitors['c'] = Mock(pretty_print=Mock(return_value=None))
        self.shard_visitor.visitors['2'] = Mock(pretty_print=Mock(return_value='D'))
        self.assertEqual(self.shard_visitor.pretty_print(), '\n10:\n\tA\n2:\n\tD')


def do_visits(visitor):
    visitor.visit(Submit("0", ("1", "2"), "3", "1", [], 'OK', 'ACM', 37))
    visitor.visit(Submit("0", ("1", "5"), "1", "3", [], 'OK', 'olympiad', 37))
    visitor.visit(Submit("0", ("1", "2"), "2", "1", [], 'OK', 'ACM', 37))
    visitor.visit(Submit("0", ("5", "2"), "2", "8", [], 'OK', 'kirov', 37))
    visitor.visit(Submit("0", ("1", "2"), "1", "1", [], 'OK', 'kirov', 37))


class TestByProblem(unittest.TestCase):
    def test_key(self):
        visitor = ShardingByProblemVisitor(Mock())
        self.assertEqual(visitor.build_key(Mock(problem_id='42')), '42')

    def test_comparable_key(self):
        visitor = ShardingByProblemVisitor(Mock())
        self.assertEqual(visitor.comparable_key(('1', '02')), 2)

    def test_pretty_key(self):
        visitor = ShardingByProblemVisitor(Mock())
        self.assertEqual(visitor.pretty_key(('1', '2')), 'Problem #2')


class TestByContest(unittest.TestCase):
    def test_key(self):
        visitor = ShardingByContestVisitor(Mock())
        self.assertEqual(visitor.build_key(Mock(problem_id=('1', '2'))), '1')

    def test_pretty_key(self):
        visitor = ShardingByContestVisitor(Mock())
        self.assertEqual(visitor.pretty_key('1'), 'Contest #1')


class TestByUser(unittest.TestCase):
    def test_key(self):
        visitor = ShardingByUserVisitor(Mock())
        self.assertEqual(visitor.build_key(Mock(user_id='1')), '1')

    def test_pretty_key(self):
        visitor = ShardingByUserVisitor(Mock())
        self.assertEqual(visitor.pretty_key('1'), 'User #1')


class TestByLang(unittest.TestCase):
    def test_key(self):
        visitor = ShardingByLangVisitor(Mock())
        self.assertEqual(visitor.build_key(Mock(lang_id='1')), '1')

    def test_pretty_key(self):
        visitor = ShardingByLangVisitor(Mock())
        self.assertEqual(visitor.pretty_key('1'), 'Lang #1')


class TestByScoring(unittest.TestCase):
    def test_key(self):
        visitor = ShardingByScoringVisitor(Mock())
        self.assertEqual(visitor.build_key(Mock(scoring='ACM')), 'ACM')
        self.assertEqual(visitor.build_key(Mock(scoring='not_acm')), 'kirov')

    def test_pretty_key(self):
        visitor = ShardingByScoringVisitor(Mock())
        self.assertEqual(visitor.pretty_key('1'), 'Scoring type: 1')


if __name__ == "__main__":
    unittest.main()
