import unittest
from sharding_visitor import ShardingVisitor
from visitor import Visitor
from factory import Factory

class FakeFactory(Factory):
    def create(key):
        return FakeVisitor()

class FakeVisitor(Visitor):
    def __init__(self):
        super().__init__()
        self.result = 0

    def visit(self, submit):
        self.result += 1

    # Returns ready for print string of result data
    def pretty_print(self):
        return str(self.result)


class FunctionTesting(unittest.TestCase):
    def setUp(self):
        self.shard_visitor = ShardingVisitor(FakeFactory)

    def test_empty_output(self):
        self.assertEqual(self.shard_visitor.pretty_print(), "")

    def test_empty_data(self):
        self.assertEqual(self.shard_visitor.get_stat_data(), [])

    def test_one_visitors(self):
        self.shard_visitor.visit(10)
        self.assertEqual(self.shard_visitor.pretty_print(), "1")

    def test_two_visitors(self):
        for i in range(2):
            self.shard_visitor.visit(10)
        self.shard_visitor.visit(20)
        self.assertEqual(self.shard_visitor.pretty_print(), "2\n\n1")

    def test_raw_stats(self):
        for i in range(2):
            self.shard_visitor.visit(10)
        self.shard_visitor.visit(20)
        self.assertEqual(self.shard_visitor.get_stat_data(), [2, 1])


if __name__ == "__main__":
    unittest.main()
