import unittest

from ejudge_xml_parse import ejudge_xml_parse, EjudgeXmlParseResult


class TestEjudgeXmlParse(unittest.TestCase):
    def test_parse_result(self):
        res = EjudgeXmlParseResult("42", "OK", "kirov", ["OK", "OK", "OK"])
        self.assertEqual(res.submit_id, "42")
        self.assertEqual(res.submit_outcome, "OK")
        self.assertEqual(res.scoring, "kirov")
        self.assertEqual(res.run_outcomes, ["OK", "OK", "OK"])

    def test_normal(self):
        file = open('testdata/xml/normal.xml', encoding='utf-8')
        res = ejudge_xml_parse(file)
        file.close()
        self.assertNotEqual(res, None)
        self.assertEqual(res.submit_id, '15')
        self.assertEqual(res.submit_outcome, 'OK')
        self.assertEqual(res.scoring, "kirov")
        self.assertEqual(res.run_outcomes,
                         [('348', '310', 'OK'), ('199', '200', 'OK'), ('327', '240', 'OK'), ('304', '280', 'OK')])

    def test_binary(self):
        file = open('testdata/xml/normal.xml', 'rb')  # imagine it is gzipped
        res = ejudge_xml_parse(file)
        file.close()
        self.assertNotEqual(res, None)
        self.assertEqual(res.submit_id, '15')
        self.assertEqual(res.submit_outcome, 'OK')
        self.assertEqual(res.scoring, "kirov")
        self.assertEqual(res.run_outcomes,
                         [('348', '310', 'OK'), ('199', '200', 'OK'), ('327', '240', 'OK'), ('304', '280', 'OK')])

    def test_empty_xml(self):
        file = open('testdata/xml/empty_xml.xml', encoding='utf-8')
        res = ejudge_xml_parse(file)
        file.close()
        self.assertEqual(res, None)

    def test_non_xml(self):
        file = open('testdata/xml/non_xml.xml', encoding='utf-8')
        res = ejudge_xml_parse(file)
        file.close()
        self.assertEqual(res, None)

    def test_non_unicode(self):
        file = open('testdata/xml/non_unicode.xml', encoding='utf-8')
        res = ejudge_xml_parse(file)
        file.close()
        self.assertEqual(res, None)

    def test_wrong_xml(self):
        file = open('testdata/xml/wrong.xml', encoding='utf-8')
        res = ejudge_xml_parse(file)
        file.close()
        self.assertEqual(res, None)


if __name__ == '__main__':
    unittest.main()
