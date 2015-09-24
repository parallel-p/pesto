import unittest
from unittest.mock import patch, MagicMock, Mock, call

from fill_database import create_submit_walker, fill_from_xml
import fill_database as fill_database


class TestFillDatabase(unittest.TestCase):
    @patch('fill_database.EjudgeDatabase')
    @patch('fill_database.SubmitWalker', return_value=17)
    def test_create_walker(self, sw, ed):
        self.assertEqual(create_submit_walker(1), 17)
        self.assertEqual(create_submit_walker(), 17)
        ed.assert_called_once_with(1)


    @patch('builtins.print')
    @patch('fill_database.create_submit_walker')
    @patch('fill_database.MultipleContestWalker')
    @patch('fill_database.EjudgeRunsFilesWorker')
    def test_fill_from_xml(self, er, mc, sw, pr):
        walker = MagicMock(walk=MagicMock(return_value=[10, 20]))
        er.return_value = MagicMock(walk=MagicMock(return_value=[(1, 'a'), (2, 'b')]))
        mc.return_value = MagicMock(walk=MagicMock(return_value=[(1, 'a'), (2, 'b')]))
        sw.return_value = walker
        fill = Mock()
        fill_database.DBSubmitsFiller = Mock(return_value=fill)
        fill_from_xml('sqlite', 'ejudge', 'dir', 'origin')
        sw.assert_called_once_with('ejudge')
        self.assertEqual(fill_database.DBSubmitsFiller.mock_calls, [call('sqlite')])
        good = ("[call(10, 'origin'),\n call(20, 'origin'),\n call(10, 'origin'),\n "
                "call(20, 'origin'),\n call(10, 'origin'),\n call(20, 'origin'),\n "
                "call(10, 'origin'),\n call(20, 'origin')]")
        self.assertEqual(str(fill.fill_db_from_submit.call_args_list), good)


if __name__ == "__main__":
    unittest.main()
