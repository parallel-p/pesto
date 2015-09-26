import unittest

from stats.submits_ids_by_signature_visitor import SubmitsIdsBySignatureVisitor
from model import Submit
from model import Run


class TestSubmitsIdBySingnatureVisitor(unittest.TestCase):
    def setUp(self):
        self.runs_OK = []
        self.runs_not_OK = []
        self.runs_mixed = []
        answer = ['OK', 'WA']
        for i in range(3):
            self.runs_OK.append(Run(None, '1', i, '100', '100', answer[0]))
            self.runs_not_OK.append(Run(None, '2', i, '100', '100', answer[1]))
            self.runs_mixed.append(Run(None, '3', i, '100', '100', answer[i % 2]))

        self.submit1 = Submit('1', '2', '3', '0', self.runs_OK, '0', 'ACM', 37)
        self.submit2 = Submit('2', '2', '3', '0', self.runs_not_OK, '1', 'ACM', 37)
        self.submit3 = Submit('3', '2', '3', '0', self.runs_mixed, '1', 'ACM', 37)
        self.submit4 = Submit('4', '2', '3', '0', self.runs_mixed, '1', 'ACM', 37)

        self.visitor = SubmitsIdsBySignatureVisitor()

    def test_data_get(self):
        self.visitor.visit(self.submit1)
        self.visitor.visit(self.submit2)
        self.visitor.visit(self.submit3)
        self.visitor.visit(self.submit4)
        res = self.visitor.get_stat_data()
        self.assertEqual(res["OKWAOK"], [2, ['3', '4']])
        self.assertEqual(res["OKOKOK"], [1, ['1']])
        self.assertEqual(res["WAWAWA"], [1, ['2']])

    def test_pretty(self):
        self.visitor.visit(self.submit1)
        self.visitor.visit(self.submit2)
        self.visitor.visit(self.submit3)
        self.visitor.visit(self.submit4)
        good_res = '''Total submits: 4
2 submits: OKWAOK
  Samples: 3, 4
1 submits: OKOKOK
  Samples: 1
1 submits: WAWAWA
  Samples: 2
'''
        self.assertEqual(self.visitor.pretty_print(), good_res)
        self.visitor.min_submits = 2
        good_res = '''Total submits: 4
2 submits: OKWAOK
  Samples: 3, 4
'''
        self.assertEqual(self.visitor.pretty_print(), good_res)


if __name__ == 'main':
    unittest.main()
