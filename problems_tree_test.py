import unittest
from unittest.mock import Mock
from problems_tree import ProblemsTree
import find_similar_problems


class TestProblemsTree(unittest.TestCase):
    def setUp(self):
        self.problems = []
        self.problems.append(Mock(cases=['a1', 'a2', 'a3', 'a4', 'a5', 'a6'], problem_id=('42', '1')))
        self.problems[-1].name = '42a'
        self.problems.append(Mock(cases=['b1', 'b2', 'b3', 'b4', 'b5'], problem_id=('42', '2')))
        self.problems[-1].name = '42b'
        self.problems.append(Mock(cases=['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7'], problem_id=('43', '2')))
        self.problems[-1].name = '43a'
        self.problems.append(Mock(cases=['a1', 'a2', 'a3', 'a4', 'a5', 'a7'], problem_id=('43', '1')))
        self.problems[-1].name = '43b'
        self.problems.append(Mock(cases=['c1', 'c2', 'c3', 'c4'], problem_id=('44', '1')))
        self.problems[-1].name = '44a'
        self.problems.append(Mock(cases=['c1', 'c2', 'c3'], problem_id=('45', '1')))
        self.problems[-1].name = '45a'
        self.problems.append(Mock(cases=['c1', 'c2', 'c3', 'c4'], problem_id=('46', '1')))
        self.problems[-1].name = '46a'
        for problem in self.problems:
            string = 'Problem #{0} ("{1}") from contest #{2}'.\
                format(problem.problem_id[1], problem.name, problem.problem_id[0])
            problem.__str__ = Mock(return_value=string)

        finder_object = Mock()
        finder_object.get_same_tests_count = lambda p1, p2: len(set(p1.cases) & set(p2.cases))
        finder_object.get_added_tests_count = lambda p1, p2: len(p2.cases) - len(set(p1.cases) & set(p2.cases))
        finder_object.get_removed_tests_count = lambda p1, p2: len(p1.cases) - len(set(p1.cases) & set(p2.cases))
        finder_object.get_similarity = lambda p1, p2: len(set(p1.cases) & set(p2.cases)) / \
            max(len(p1.cases), len(p2.cases))
        finder_object.get_stat_data = Mock(return_value=[(self.problems[0], self.problems[3]),
                                                         (self.problems[1], self.problems[2]),
                                                         (self.problems[4], self.problems[5]),
                                                         (self.problems[4], self.problems[6]),
                                                         (self.problems[5], self.problems[6])])
        find_similar_problems.SimilarProblemsFinder = Mock(return_value=finder_object)

        self.tree = ProblemsTree(self.problems)

    def test_common(self):
        self.assertEqual(self.tree.get_previous_problem(self.problems[0]), None)
        self.assertEqual(self.tree.get_previous_problem(self.problems[1]), None)
        self.assertEqual(self.tree.get_previous_problem(self.problems[2]), self.problems[1])
        self.assertEqual(self.tree.get_previous_problem(self.problems[3]), self.problems[0])
        self.assertEqual(self.tree.get_previous_problem(self.problems[4]), None)
        self.assertEqual(self.tree.get_previous_problem(self.problems[5]), self.problems[4])
        self.assertEqual(self.tree.get_previous_problem(self.problems[6]), self.problems[4])

    def test_str(self):
        result_string = str(self.tree)
        correct_string = """Problem #1 ("42a") from contest #42: it is a new problem. Tests: 6.
Problem #2 ("42b") from contest #42: it is a new problem. Tests: 5.
Problem #2 ("43a") from contest #43: is based on Problem #2 ("42b") from contest #42. Tests: +2, -0, 5 not changed.
Problem #1 ("43b") from contest #43: is based on Problem #1 ("42a") from contest #42. Tests: +1, -1, 5 not changed.
Problem #1 ("44a") from contest #44: it is a new problem. Tests: 4.
Problem #1 ("45a") from contest #45: is based on Problem #1 ("44a") from contest #44. Tests: +0, -1, 3 not changed.
Problem #1 ("46a") from contest #46: it is Problem #1 ("44a") from contest #44. Tests: 4.
"""
        self.assertEqual(result_string, correct_string)

    def test_get_problems(self):
        self.tree.problems = 42
        self.assertEqual(self.tree.get_problems(), 42)

    def test_parent_relation(self):
        tree = ProblemsTree(self.problems)
        tree.finder = Mock()
        tree.finder.get_similarity.return_value = 1
        tree.finder.get_same_tests_count.return_value = 2
        tree.finder.get_removed_tests_count.return_value = 3
        tree.finder.get_added_tests_count.return_value = 4
        tree.get_previous_problem = Mock()
        problem = Mock()
        prev_problem = tree.get_previous_problem()

        self.assertEqual(tree.get_similarity_to_parent(problem), 1)
        tree.finder.get_similarity.assert_called_once_with(prev_problem, problem)
        self.assertEqual(tree.get_tests_same_with_parent(problem), 2)
        tree.finder.get_same_tests_count.assert_called_once_with(prev_problem, problem)
        self.assertEqual(tree.get_removed_tests_count(problem), 3)
        tree.finder.get_removed_tests_count.assert_called_once_with(prev_problem, problem)
        self.assertEqual(tree.get_added_tests_count(problem), 4)
        tree.finder.get_added_tests_count.assert_called_once_with(prev_problem, problem)

        self.assertEqual(tree.get_relation_to_parent(problem), (1, 2, 3, 4))

if __name__ == "__main__":
    unittest.main()
