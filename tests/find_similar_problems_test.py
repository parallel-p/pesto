import unittest
from unittest.mock import Mock

from find_similar_problems import SimilarProblemsFinder


class TestFindSimilarProblems(unittest.TestCase):
    def setUp(self):
        self.problems = []
        self.problems.append(Mock(cases=['a1', 'a2', 'a3', 'a4', 'a5', 'a6'], problem_id=('42', '1')))
        self.problems[-1].name = '42a'
        self.problems.append(Mock(cases=['b1', 'b2', 'b3', 'b4', 'b5'], problem_id=('42', '2')))
        self.problems[-1].name = '42b'
        self.problems.append(Mock(cases=['b7', 'b2', 'b4', 'b3', 'b5', 'b6', 'b1'], problem_id=('43', '2')))
        self.problems[-1].name = '43a'
        self.problems.append(Mock(cases=['a1', 'a2', 'a3', 'a4', 'a5', 'a7'], problem_id=('43', '1')))
        self.problems[-1].name = '43b'
        self.problems.append(Mock(cases=['c2', 'c1', 'c3', 'c4'], problem_id=('44', '1')))
        self.problems[-1].name = '44a'
        self.problems.append(Mock(cases=[], problem_id=('45', '1')))
        self.problems[-1].name = '45a'
        self.problems.append(Mock(cases=[], problem_id=('45', '2')))
        self.problems[-1].name = '45b'
        self.finder = SimilarProblemsFinder(self.problems)

    def test_common(self):
        result = self.finder.get_stat_data()
        self.assertEqual(len(result), 2)
        self.assertTrue((self.problems[0], self.problems[3]) in result)
        self.assertTrue((self.problems[1], self.problems[2]) in result)

    def test_similarity(self):
        for problem_1 in self.problems:
            for problem_2 in self.problems:
                if problem_1 != problem_2:
                    self.assertEqual(self.finder.get_same_tests_count(problem_1, problem_2),
                                     len(set(problem_1.cases) & set(problem_2.cases)))
                    self.assertEqual(self.finder.get_added_tests_count(problem_1, problem_2),
                                     len(set(problem_2.cases) - set(problem_1.cases)))
                    self.assertEqual(self.finder.get_removed_tests_count(problem_1, problem_2),
                                     len(set(problem_1.cases) - set(problem_2.cases)))

    def test_str(self):
        result_string = str(self.finder)
        correct_string = """Problems 42a from contest #42 and problem 43b from contest #43 are similar (83%). Tests: +1, -1, 5 not changed.
Problems 42b from contest #42 and problem 43a from contest #43 are similar (71%). Tests: +2, -0, 5 not changed.
"""
        self.assertEqual(sorted(result_string.split('\n')), sorted(correct_string.split('\n')))


if __name__ == "__main__":
    unittest.main()

