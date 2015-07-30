import unittest
from problem import Problem


class TestProblemMethods(unittest.TestCase):

    def test_init_white(self):
        temp = Problem(0, 0, [0, 0])
        self.assertTrue(temp.contest_id == 0 and temp.problem_id == 0 and temp.case_ids == [0, 0])

    def test_init_empty_init(self):
        with self.assertRaises(TypeError):
            Problem()

    def test_init_bad_arguments(self):
        with self.assertRaises(TypeError):
            Problem([0, 0], sort(), [[0, 0], [0, 0]])

    def test_str_white(self):
        temp = Problem('luck', 'duck', [0, 0])
        self.assertEqual(str(temp), 'Contest #luck Problem #duck\nCases: [0, 0]')

if __name__ == '__main__':
    unittest.main()
