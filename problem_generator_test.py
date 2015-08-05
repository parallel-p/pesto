import unittest
from unittest.mock import Mock
from problem_generator import problem_generator
import ejudge_contest
import md5_hasher


class TestProblemGenerator(unittest.TestCase):
    def setUp(self):
        ejudge_contest_object = Mock()
        ejudge_contest_object.get_contest_id = Mock(return_value='42')
        ejudge_contest_object.get_problems_ids = Mock(return_value=['1', '2'])
        ejudge_contest_object.get_short_name_by_problem_id = Mock(return_value='a-plus-b')
        ejudge_contest_object.get_tests_paths_by_problem_id = Mock(return_value=[('a', 'b'), ('c', 'd')])
        ejudge_contest.EjudgeContest = Mock(return_value=ejudge_contest_object)
        md5_hasher.get_hash = Mock(return_value='hash')

    def test_common(self):
        contest_dirs = ['000001', '000179']
        result = [x for x in problem_generator(contest_dirs)]
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].problem_id, ('42', '1'))
        self.assertEqual(result[1].problem_id, ('42', '2'))
        self.assertEqual(result[2].problem_id, ('42', '1'))
        self.assertEqual(result[3].problem_id, ('42', '2'))
        for problem in result:
            self.assertEqual(problem.name, 'a-plus-b')
            self.assertEqual(problem.cases, ['hash', 'hash'])
        self.assertEqual(md5_hasher.get_hash.call_args_list, [(('a', 'b'),), (('c', 'd'),)] * 4)


if __name__ == "__main__":
    unittest.main()
