import unittest
from sharding_visitor import ShardingVisitor
from sharding_visitor import ShardingByProblemVisitor
from sharding_visitor import ShardingByContestVisitor
from sharding_visitor import ShardingByUserVisitor
from visitor import FakeVisitor
from model import Submit
from visitor_factory import VisitorFactory


class FakeFactory(VisitorFactory):
    @staticmethod
    def create(key):
        return FakeVisitor()


class FunctionTesting(unittest.TestCase):
    def setUp(self):
        self.shard_visitor = ShardingVisitor(FakeFactory)

    def test_empty_output(self):
        self.assertEqual(self.shard_visitor.pretty_print(), "")

    def test_empty_data(self):
        self.assertEqual(self.shard_visitor.get_stat_data(), [])

    def test_one_visitors(self):
        self.shard_visitor.visit(10)
        self.assertEqual(self.shard_visitor.pretty_print(), "Key: 10 1")

    def test_two_visitors(self):
        for i in range(2):
            self.shard_visitor.visit(10)
        self.shard_visitor.visit(20)
        self.assertEqual(self.shard_visitor.pretty_print(), "Key: 10 2\n\nKey: 20 1")

    def test_raw_stats(self):
        for i in range(2):
            self.shard_visitor.visit(20)
        self.shard_visitor.visit(10)
        self.assertEqual(self.shard_visitor.get_stat_data(), [('10', 1), ('20', 2)])


class TestByProblem(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByProblemVisitor(FakeFactory)
        visitor.visit(Submit(0, (1, 228), 0, [], 'OK'))
        visitor.visit(Submit(0, (2007, 322), 0, [], 'OK'))
        visitor.visit(Submit(0, (1, 228), 0, [], 'OK'))
        self.assertEqual(len(visitor.visitors.keys()), 2)

class TestByContest(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByContestVisitor(FakeFactory)
        visitor.visit(Submit(0, (1, 0), 0, [], 'OK'))
        visitor.visit(Submit(0, (2, 0), 0, [], 'OK'))
        visitor.visit(Submit(0, (1, 0), 0, [], 'OK'))
        self.assertEqual(len(visitor.visitors.keys()), 2)

class TestByUser(unittest.TestCase):
    def test_submits(self):
        visitor = ShardingByUserVisitor(FakeFactory)
        visitor.visit(Submit(0, (0, 0), 1, [], 'OK'))
        visitor.visit(Submit(0, (0, 0), 2, [], 'OK'))
        visitor.visit(Submit(0, (0, 0), 1, [], 'OK'))
        self.assertEqual(len(visitor.visitors.keys()), 2)


if __name__ == "__main__":
    unittest.main()
