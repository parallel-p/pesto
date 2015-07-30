import unittest
from ejudge_get_submit import ejudge_get_submit


class FakeBase:

    def __init__(self):
        self.user_id = '228'
        self.problem_id = '37'
        self.problem = None

    def get_problem_id(self, *p):
        return self.problem_id

    def get_user_id(self, *p):
        return self.user_id

    def problem_exists(self, *p):
        return self.problem is not None

    def get_problem(self, *p):
        return self.problem

    def add_problem(self, a, b, problem):
        self.problem = problem


class TestEjudgeGetSubmit(unittest.TestCase):

    def test_normal(self):
        file = open('testdata/xml/normal.xml', encoding='utf-8')
        fakebase = FakeBase()
        submit = ejudge_get_submit(file, fakebase, '12')
        self.assertNotEqual(submit, None)
        self.assertEqual(submit.submit_id, '15')
        self.assertEqual(submit.problem, fakebase.problem)
        self.assertEqual(submit.user_id, '228')
        self.assertEqual(submit.outcome, 'OK')
        self.assertNotEqual(fakebase.problem, None)
        self.assertEqual(fakebase.problem.contest_id, '12')
        self.assertEqual(fakebase.problem.problem_id, '37')
        self.assertEqual(len(fakebase.problem.case_ids), 4)
        self.assertEqual(len(submit.runs), 4)
        for i in range(4):
            self.assertEqual(submit.runs[i].problem, fakebase.problem)
            self.assertEqual(submit.runs[i].submit_id, '15')
            self.assertEqual(submit.runs[i].case_id, str(i + 1))
            self.assertEqual(submit.runs[i].outcome, 'OK')
            self.assertEqual(fakebase.problem.case_ids[i], str(i + 1))
        file.close()

    def test_non_xml(self):
        file = open('testdata/xml/non_xml.xml', encoding='utf-8')
        fakebase = FakeBase()
        self.assertEqual(ejudge_get_submit(file, fakebase, 0), None)
        file.close()

    def test_wrong_xml(self):
        file = open('testdata/xml/wrong.xml', encoding='utf-8')
        fakebase = FakeBase()
        self.assertEqual(ejudge_get_submit(file, fakebase, 0), None)
        file.close()

    def test_non_submit(self):
        file = open('testdata/xml/normal.xml', encoding='utf-8')
        fakebase = FakeBase()
        fakebase.problem_id = None
        fakebase.user_id = None
        self.assertEqual(ejudge_get_submit(file, fakebase, 0), None)
        file.close()

    def test_extend_problem(self):
        file = open('testdata/xml/normal.xml', encoding='utf-8')
        fakebase = FakeBase()
        ejudge_get_submit(file, fakebase, 0)
        file.close()
        file = open('testdata/xml/normal_extended.xml', encoding='utf-8')
        ejudge_get_submit(file, fakebase, 0)
        file.close()
        self.assertEqual(len(fakebase.problem.case_ids), 6)

if __name__ == '__main__':
    unittest.main()