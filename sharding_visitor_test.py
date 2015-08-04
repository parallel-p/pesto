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
        self.assertEqual(self.shard_visitor.pretty_print(), "Key: 10\n1")

    def test_two_visitors(self):
        for i in range(2):
            self.shard_visitor.visit(10)
        self.shard_visitor.visit(20)
        self.assertEqual(self.shard_visitor.pretty_print(), "Key: 10\n2\n\nKey: 20\n1")

    def test_raw_stats(self):
        for i in range(2):
            self.shard_visitor.visit(20)
        self.shard_visitor.visit(10)
        self.assertEqual(self.shard_visitor.get_stat_data(), [('10', 1), ('20', 2)])


def do_visits(visitor):
    visitor.visit(Submit("0", ("1", "2"), "3", "1", [], 'OK', 'ACM'))
    visitor.visit(Submit("0", ("1", "5"), "1", "3", [], 'OK', 'olympiad'))
    visitor.visit(Submit("0", ("1", "2"), "2", "1", [], 'OK', 'ACM'))
    visitor.visit(Submit("0", ("5", "2"), "2", "8", [], 'OK', 'kirov'))
    visitor.visit(Submit("0", ("1", "2"), "1", "1", [], 'OK', 'kirov'))


class TestByProblem(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByProblemVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {("1", "2"), ("1", "5"), ("5", "2")})
        self.assertEqual(len(visitor.visitors[("1", "2")].submits), 3)
        self.assertEqual(len(visitor.visitors[("1", "5")].submits), 1)
        self.assertEqual(len(visitor.visitors[("5", "2")].submits), 1)


class TestByContest(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByContestVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {"1", "5"})
        self.assertEqual(len(visitor.visitors["1"].submits), 4)
        self.assertEqual(len(visitor.visitors["5"].submits), 1)


class TestByUser(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByUserVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {"3", "1", "2"})
        self.assertEqual(len(visitor.visitors["3"].submits), 1)
        self.assertEqual(len(visitor.visitors["1"].submits), 2)
        self.assertEqual(len(visitor.visitors["2"].submits), 2)


class TestByLang(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByLangVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {"1", "3", "8"})
        self.assertEqual(len(visitor.visitors["1"].submits), 3)
        self.assertEqual(len(visitor.visitors["3"].submits), 1)
        self.assertEqual(len(visitor.visitors["8"].submits), 1)


class TestByScoring(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByScoringVisitor(FakeFactory())
        do_visits(visitor)
        self.assertEqual(set(visitor.visitors.keys()), {"ACM", "olympiad", "kirov"})
        self.assertEqual(len(visitor.visitors["ACM"].submits), 2)
        self.assertEqual(len(visitor.visitors["olympiad"].submits), 1)
        self.assertEqual(len(visitor.visitors["kirov"].submits), 2)

if __name__ == "__main__":
    unittest.main()
