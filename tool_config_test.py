import unittest
from visitor import Visitor
from tool_config import get_presets_info
from tool_config import get_visitor_by_preset


class TestToolConfig(unittest.TestCase):
    def test_info(self):
        self.assertEqual(type(get_presets_info()), str)

    def test_presets(self):
        presets1 = ['1', 'count_submits', '2', 'eq_matrix', '3', 'count_cases', '4', 'same_runs_kirov']
        presets2 = ['5', 'same_runs_acm', '6', 'submits_by_signature', '7', 'submits_by_tests', '8', 'gen_pickles']
        for preset in presets1 + presets2:
            self.assertEqual(issubclass(type(get_visitor_by_preset(preset)), Visitor), True)
        self.assertEqual(get_visitor_by_preset('kek'), None)

if __name__ == "__main__":
    unittest.main()
