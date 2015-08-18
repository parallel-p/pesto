import unittest
from visitor import Visitor
from tool_config import get_presets_info
from tool_config import get_factory_by_preset
from tool_config import VisitorFactory
import tool_config
from unittest.mock import Mock, patch


class TestToolConfig(unittest.TestCase):
    def test_info(self):
        self.assertEqual(type(get_presets_info()), str)

    def test_presets(self):
        presets1 = ['1', 'count_submits', '2', 'eq_matrix', '3', 'same_runs']
        presets2 = ['4', 'submits_by_signature', '5', 'submits_by_tests', '6', 'gen_pickles']
        for preset in presets1 + presets2:
            self.assertEqual(issubclass(type(get_factory_by_preset(preset, 'kek.txt')), VisitorFactory), True)
        self.assertEqual(get_factory_by_preset('kek', 'kok.txt'), None)

    @patch('tool_config.SameRunsACMFactory')
    @patch('tool_config.SameRunsKirovFactory')
    def test_same_runs_factory(self, kirov, acm):
        factory = tool_config.SameRunsFactory()
        self.assertIsInstance(factory.create('ACM'), tool_config.ShardingByProblemVisitor)
        acm.assert_any_call()
        self.assertIsInstance(factory.create('kirov'), tool_config.ShardingByProblemVisitor)
        kirov.assert_any_call()

    @patch('tool_config.EqMatrixFactory')
    def test_eq_matrix_factory(self, eq):
        factory = tool_config.EqMatrixShardingByProblem()
        self.assertIsInstance(factory.create(1), tool_config.ShardingByProblemVisitor)


    def test_same_runs_acm(self):
        factory = tool_config.SameRunsACMFactory()
        self.assertIsInstance(factory.create(1), tool_config.SameRunsACM)

    def test_same_runs_big_stat(self):
        factory = tool_config.SameRunsBigStatFactory()
        self.assertIsInstance(factory.create(1), tool_config.SameRunsBigStat)

    @patch('tool_config.PickleWriter')
    def test_pickle_writer(self, pw):
        factory = tool_config.PickleWriterFactory('1337')
        result = factory.create(1)
        self.assertEqual(result.default_path, '1337')

    def test_custom_sharding_factory(self):
        shard = Mock(return_value=42)
        vis = Mock()
        factory = tool_config.CustomShardingFactory(shard, vis)
        self.assertEqual(factory.create(1), 42)
        vis.assert_any_call()

    def test_custom_visitor_factory(self):
        vis = Mock(return_value=42)
        factory = tool_config.CustomVisitorFactory(vis)
        self.assertEqual(factory.create(1), 42)

    @patch('tool_config.SameRunsKirovFactory2')
    def test_same_runs_kirov(self, ki):
        factory = tool_config.SameRunsKirovFactory()
        self.assertIsInstance(factory.create(1), tool_config.ElectorByMaxCasesVisitor)
        ki.assert_any_call()

    def test_same_runs_kirov2(self):
        factory = tool_config.SameRunsKirovFactory2()
        self.assertIsInstance(factory.create(1), tool_config.SameRunsKirov)

    def test_submits_counter(self):
        factory = tool_config.SubmitsCounterFactory()
        self.assertIsInstance(factory.create(1), tool_config.SubmitsCounter)

    def test_max_counter(self):
        factory = tool_config.MaxTestCasesCountFactory()
        self.assertIsInstance(factory.create(1), tool_config.MaxTestCasesCount)

    def test_eq_matrix(self):
        factory = tool_config.EqMatrixFactory()
        self.assertIsInstance(factory.create(1), tool_config.EqMatrix)

    @patch('tool_config.SubmitsIdsBySignatureFactory2')
    def test_submit_ids_sign(self, si):
        factory = tool_config.SubmitsIdsBySignatureFactory()
        self.assertIsInstance(factory.create(1), tool_config.ShardingByLangVisitor)
        si.assert_any_call()

    def test_submit_ids_sign2(self):
        factory = tool_config.SubmitsIdsBySignatureFactory2()
        self.assertIsInstance(factory.create(1), tool_config.SubmitsIdsBySignatureVisitor)

if __name__ == "__main__":
    unittest.main()
