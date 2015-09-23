import unittest
from unittest.mock import Mock, patch

from visitor import Visitor

from tool_config import get_presets_info
from tool_config import SameRuns


class TestSameRuns(unittest.TestCase):
    @patch('tool_config.SameRunsACM')
    def test_visit_acm(self, cl):
        vis = SameRuns()
        submit = Mock(scoring='acm')
        vis.visit(submit)
        cl.assert_any_call()
        vis.child.visit.assert_called_once_with(submit)

    @patch('tool_config.ElectorByMaxCasesVisitor')
    def test_visit_kirov(self, cl):
        vis = SameRuns()
        submit = Mock(scoring='kirov')
        vis.visit(submit)
        vis.child.visit.assert_called_once_with(submit)

    def test_funcs(self):
        vis = SameRuns()
        vis.child = Mock()
        vis.child.get_stat_data.return_value = 42
        vis.child.pretty_print.return_value = 228
        self.assertEqual(vis.get_stat_data(), 42)
        self.assertEqual(vis.pretty_print(), 228)


if __name__ == "__main__":
    unittest.main()
