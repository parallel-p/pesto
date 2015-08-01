import unittest
from stats.submits_ids_by_signature_visitor import SubmitsIdsBySignatueVisitor
from model import Submit
from model import Run

class TestSubmitsIdBySingnatureVisitor(unittest.TestCase):
    def setUp(self):
        self.runs_OK = []
        self.runs_not_OK = []
        self.runs_mixed = []
        answer = ['OK', 'WA']
        for i in range(3):
            self.runs_OK.append(Run(None, '1', i, answer[0]))
            self.runs_not_OK.append(Run(None, '2', i, answer[1]))
            self.runs_mixed.append(Run(None, '3', i, answer[i % 2]))

        self.submit1 = Submit('1', '2', '3', self.runs_OK,'0')
        self.submit2 = Submit('2', '2', '3', self.runs_not_OK,'1')
        self.submit3 = Submit('3', '2', '3', self.runs_mixed,'1')
        self.submit4 = Submit('4', '2', '3', self.runs_mixed,'1')

        self.visitor = SubmitsIdsBySignatueVisitor()

    def test_dadta_get(self):
        self.visitor.visit(self.submit1)
        self.visitor.visit(self.submit2)
        self.visitor.visit(self.submit3)
        self.visitor.visit(self.submit4)
        res = self.visitor.get_stat_data()
        self.assertEqual(res["OKWAOK"], ['3', '4'])
        self.assertEqual(res["OKOKOK"], ['1'])
        self.assertEqual(res["WAWAWA"], ['2'])

if __name__ == 'main':
    unittest.main()