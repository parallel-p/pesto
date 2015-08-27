import unittest
from unittest.mock import Mock, patch

from visitor import Visitor

from tool_config import get_presets_info
from tool_config import get_visitor_by_preset, SameRuns


class TestToolConfig(unittest.TestCase):
    def test_info(self):
        self.assertEqual(type(get_presets_info()), str)

    def test_presets(self):
        presets1 = ['1', 'count_submits', '2', 'eq_matrix', '3', 'same_runs']
        presets2 = ['4', 'submits_by_signature', '5', 'submits_by_tests', '6', 'gen_pickles']
        for preset in presets1 + presets2:
            self.assertIsInstance(get_visitor_by_preset(preset, 'kek.txt'), Visitor)
        self.assertIsNone(get_visitor_by_preset('kek', 'kok.txt'))


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
