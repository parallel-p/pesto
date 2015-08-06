import unittest
from unittest.mock import Mock, MagicMock
from pesto_testcase import PestoTestCase
import configparser
import toollib


class ToollibTest(PestoTestCase):
    def test_parse_args_filters(self):
        parser = Mock()
        toollib.parse_args_filters(parser)
        good_parser = Mock()
        good_parser.add_argument('--filter-problem', help='process only submits for the problem selected')
        good_parser.add_argument('--filter-user', help='process only submits by the selected user')
        good_parser.add_argument('--filter-contest', help='process only submits in the selected contest')
        self.assertEqual(parser.add_argument.call_args_list, good_parser.add_argument.call_args_list)

    def test_parse_args_input(self):
        parser = Mock()
        toollib.parse_args_input(parser)
        good_parser = Mock()
        good_parser.add_argument('-m', '--multicontest', help='base_dir contains several contests', action='store_true')
        good_parser.add_argument('--dir', help="directory containing xml's/pickles")
        self.assertEqual(parser.add_argument.call_args_list, good_parser.add_argument.call_args_list)

    def test_parse_args_output(self):
        parser = Mock()
        toollib.parse_args_output(parser)
        good_parser = Mock()
        good_parser.add_argument('-c', '--console', help='output to console', action='store_true')
        good_parser.add_argument('-o', '--output', help='output file')
        self.assertEqual(parser.add_argument.call_args_list, good_parser.add_argument.call_args_list)

    def test_parse_args_config(self):
        parser = Mock()
        toollib.parse_args_config(parser)
        good_parser = Mock()
        good_parser.add_argument('--cfg', help="config file")
        self.assertEqual(parser.add_argument.call_args_list, good_parser.add_argument.call_args_list)

    def test_read_config_full(self):
        config_parser_backup = configparser.ConfigParser
        config_parser_object = MagicMock()
        configparser.ConfigParser = Mock(return_value=config_parser_object)
        result = toollib.read_config('filename')
        config_parser_object.read.assert_called_once_with('filename')
        self.assertEqual(result, config_parser_object)
        configparser.ConfigParser = config_parser_backup

    def test_read_config_section_good(self):
        config_parser_backup = configparser.ConfigParser
        config_parser_object = MagicMock()
        config_parser_object.__contains__ = Mock(return_value=True)
        configparser.ConfigParser = Mock(return_value=config_parser_object)
        result = toollib.read_config('filename', 'section')
        config_parser_object.read.assert_called_once_with('filename')
        self.assertEqual(result, config_parser_object.__getitem__.return_value)
        configparser.ConfigParser = config_parser_backup
    
    def test_read_config_section_bad(self):
        config_parser_backup = configparser.ConfigParser
        config_parser_object = MagicMock()
        config_parser_object.__contains__ = Mock(return_value=False)
        configparser.ConfigParser = Mock(return_value=config_parser_object)
        result = toollib.read_config('filename', 'section')
        config_parser_object.read.assert_called_once_with('filename')
        self.assertEqual(result, None)
        configparser.ConfigParser = config_parser_backup

if __name__ == "__main__":
    unittest.main()
