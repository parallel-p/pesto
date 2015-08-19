import unittest
from sharding_visitor import ShardingVisitor
from sharding_visitor import ShardingByProblemVisitor
from sharding_visitor import ShardingByContestVisitor
from sharding_visitor import ShardingByUserVisitor
from sharding_visitor import ShardingByLangVisitor
from sharding_visitor import ShardingByScoringVisitor
from visitor import FakeVisitor
from model import Submit
from visitor_factory import VisitorFactory
from unittest.mock import Mock


class FakeFactory(VisitorFactory):
    def create(self, key):
        return FakeVisitor()


class FunctionTesting(unittest.TestCase):
    def setUp(self):
        self.shard_visitor = ShardingVisitor(FakeFactory())

    def test_empty_output(self):
        self.assertEqual(self.shard_visitor.pretty_print(), "")

    def test_empty_data(self):
        self.assertEqual(self.shard_visitor.get_stat_data(), [])

    def test_one_visitors(self):
        self.shard_visitor.visit(10)
        self.assertEqual(self.shard_visitor.visitors.keys(), {'10'})
        self.assertEqual(self.shard_visitor.visitors['10'].submits, [10])

    def test_two_visitors(self):
        for i in range(2):
            self.shard_visitor.visit(10)
        self.shard_visitor.visit(20)
        self.assertEqual(self.shard_visitor.visitors.keys(), {'10', '20'})
        self.assertEqual(self.shard_visitor.visitors['10'].submits, [10, 10])
        self.assertEqual(self.shard_visitor.visitors['20'].submits, [20])

    def test_raw_stats(self):
        for i in range(2):
            self.shard_visitor.visit(20)
        self.shard_visitor.visit(10)
        self.assertEqual(self.shard_visitor.get_stat_data(), [('10', 1), ('20', 2)])

    def test_pretty_key(self):
        self.assertEqual(self.shard_visitor.pretty_key(5), '5')
        self.shard_visitor.visit(10)

    def test_pretty_print(self):
        self.shard_visitor.visitors['a'] = Mock(pretty_print=Mock(return_value='A'))
        self.shard_visitor.visitors['b'] = Mock(pretty_print=Mock(return_value=''))
        self.shard_visitor.visitors['c'] = Mock(pretty_print=Mock(return_value=None))
        self.shard_visitor.visitors['d'] = Mock(pretty_print=Mock(return_value='D'))
        self.assertEqual(self.shard_visitor.pretty_print(), '\na:\n\tA\nd:\n\tD')


def do_visits(visitor):
    visitor.visit(Submit("0", ("1", "2"), "3", "1", [], 'OK', 'ACM', 37))
    visitor.visit(Submit("0", ("1", "5"), "1", "3", [], 'OK', 'olympiad', 37))
    visitor.visit(Submit("0", ("1", "2"), "2", "1", [], 'OK', 'ACM', 37))
    visitor.visit(Submit("0", ("5", "2"), "2", "8", [], 'OK', 'kirov', 37))
    visitor.visit(Submit("0", ("1", "2"), "1", "1", [], 'OK', 'kirov', 37))


class TestByProblem(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByProblemVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {("1", "2"), ("1", "5"), ("5", "2")})
        self.assertEqual(len(visitor.visitors[("1", "2")].submits), 3)
        self.assertEqual(len(visitor.visitors[("1", "5")].submits), 1)
        self.assertEqual(len(visitor.visitors[("5", "2")].submits), 1)

    def test_pretty_key(self):
        visitor = ShardingByProblemVisitor(Mock())
        self.assertEqual(visitor.pretty_key(('1', '2')), 'Problem #2')


class TestByContest(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByContestVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {"1", "5"})
        self.assertEqual(len(visitor.visitors["1"].submits), 4)
        self.assertEqual(len(visitor.visitors["5"].submits), 1)

    def test_pretty_key(self):
        visitor = ShardingByContestVisitor(Mock())
        self.assertEqual(visitor.pretty_key('1'), 'Contest #1')


class TestByUser(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByUserVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {"3", "1", "2"})
        self.assertEqual(len(visitor.visitors["3"].submits), 1)
        self.assertEqual(len(visitor.visitors["1"].submits), 2)
        self.assertEqual(len(visitor.visitors["2"].submits), 2)

    def test_pretty_key(self):
        visitor = ShardingByUserVisitor(Mock())
        self.assertEqual(visitor.pretty_key('1'), 'UserID #1')


class TestByLang(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByLangVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {"1", "3", "8"})
        self.assertEqual(len(visitor.visitors["1"].submits), 3)
        self.assertEqual(len(visitor.visitors["3"].submits), 1)
        self.assertEqual(len(visitor.visitors["8"].submits), 1)

    def test_pretty_key(self):
        visitor = ShardingByLangVisitor(Mock())
        self.assertEqual(visitor.pretty_key('1'), 'LangID #1')


class TestByScoring(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByScoringVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {"ACM", "kirov"})
        self.assertEqual(len(visitor.visitors["ACM"].submits), 2)
        self.assertEqual(len(visitor.visitors["kirov"].submits), 3)

    def test_pretty_key(self):
        visitor = ShardingByScoringVisitor(Mock())
        self.assertEqual(visitor.pretty_key('blah'), 'Scoring type - #blah')

if __name__ == "__main__":
    unittest.main()
