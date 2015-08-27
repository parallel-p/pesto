import unittest
from unittest.mock import Mock
import os

from pesto_testcase import PestoTestCase

from fill_db_from_contest_xml import fill_db_from_contest_xml


class FillDBFromContestXMLTest(PestoTestCase):
    def prepare_request(self, format_string, data_tuple):
        return format_string.replace('?', '{}').format(*data_tuple)

    @unittest.mock.patch('fill_db_from_contest_xml.AllFilesWalker',
                         return_value=Mock(walk=Mock(return_value=[(None, os.path.join('asdf', '123456')), \
                                                                   (None, os.path.join('asdf', '179179')), \
                                                                   (None, os.path.join('asdf', 'notnum')),
                                                                   (None, os.path.join('asdf', '031337'))])))
    @unittest.mock.patch('fill_db_from_contest_xml.ejudge_get_contest_name',
                         side_effect=['I am contest name #1', 'Contest name #2', 'Yo, i am contest name #3!'])
    @unittest.mock.patch('os.path.basename', side_effect=['123456', '179179', 'notnum', '031337'])
    @unittest.mock.patch('logging.warning', Mock())
    def test_common(self, some, useless, args):
        cursor = Mock()
        fill_db_from_contest_xml('asdf', cursor, 'lksh')
        resulting_requests = []
        for one_call in cursor.execute.call_args_list:
            format_string, data_tuple = tuple(one_call)[0]
            resulting_requests.append(self.prepare_request(format_string, data_tuple))
        good_requests = ['UPDATE Contests SET name = I am contest name #1 WHERE origin = lksh AND contest_id = 123456',
                         'UPDATE Contests SET name = Contest name #2 WHERE origin = lksh AND contest_id = 179179',
                         'UPDATE Contests SET name = Yo, i am contest name #3! WHERE origin = lksh AND contest_id = 031337']
        self.assertEqual(resulting_requests, good_requests)


if __name__ == "__main__":
    unittest.main()
