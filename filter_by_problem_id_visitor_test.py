import unittest
from filter_by_problem_id_visitor import FilterByProblemIdVisitor
from model import Submit
from model import Problem


class VisitorForTesting():
    def __init__(self):
        self.mathcing = False

    def update_submit(self, submit):
        self.mathcing = True


class FilterVisitorTest(unittest.TestCase):
    def setUp(self):
        self.visitor = VisitorForTesting()

        self.good_problem_id = "666"
        self.bad_problem_id = "333"

        self.good_submit = Submit("666", self.good_problem_id, "666", [], "666")
        self.bad_submit = Submit("666", self.bad_problem_id, "666", [], "666")
        
    def test_init(self):
        testing_visitor = FilterByProblemIdVisitor(self.good_problem_id, self.visitor)
        self.assertEqual(testing_visitor.problem_id, "666")
        self.assertEqual(testing_visitor.target_visitor, self.visitor)

    def test_matching_problem_id(self):
        testing_visitor = FilterByProblemIdVisitor(self.good_problem_id, self.visitor)
        testing_visitor.update_submit(self.good_submit)
        self.assertTrue(self.visitor.mathcing)

    def test_mismatching_problem_id(self):
        testing_visitor = FilterByProblemIdVisitor(self.good_problem_id, self.visitor)
        testing_visitor.update_submit(self.bad_submit)
        self.assertFalse(self.visitor.mathcing)


if __name__ == "__main__":
    unittest.main()
