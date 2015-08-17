import unittest
from unittest.mock import Mock
from case_counter import CasesCounter


class TestCountCases(unittest.TestCase):
    def setUp(self):
        self.problems = [Mock(cases=[i for i in range(2)], problem_id=('17', '1')),
                         Mock(cases=[i for i in range(3)], problem_id=('17', '2')),
                         Mock(cases=[i for i in range(4)], problem_id=('17', '3'))]
        self.counter = CasesCounter(self.problems)

    def test_get_stat_data(self):
        self.assertEqual(self.counter.get_stat_data(), {('17', '1'): 2,
                                                        ('17', '2'): 3,
                                                        ('17', '3'): 4
                                                        }
                         )

        self.assertEqual(self.counter.result, {('17', '1'): 2,
                                               ('17', '2'): 3,
                                               ('17', '3'): 4
                                               }
                         )

    def test_str(self):
        self.counter.get_stat_data()
        self.assertEqual(str(self.counter), 'Contest #000017 Problem #1: 2 case(s)\n'
                                            'Contest #000017 Problem #2: 3 case(s)\n'
                                            'Contest #000017 Problem #3: 4 case(s)\n')

if __name__ == "__main__":
    unittest.main()
