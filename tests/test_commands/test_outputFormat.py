import unittest
import mock
from anydo_cli.lib.outputFormat import OutputFormat, print_with_format


class TestOutputFormat(unittest.TestCase):
    def test_valid_formats_returns_correct_list(self):
        expected_list = ['json', 'yaml']
        self.assertListEqual(expected_list, OutputFormat.valid_formats())

    @mock.patch('anydo_cli.lib.outputFormat.json.dumps')
    @mock.patch('anydo_cli.lib.outputFormat.yaml.dump')
    def test_print_with_format_prints_json(self, dump, dumps):
        expected_thing_to_print = {'test': 'test'}
        print_with_format(expected_thing_to_print)
        dumps.assert_called_once_with(expected_thing_to_print)
        dump.assert_not_called()

    @mock.patch('anydo_cli.lib.outputFormat.json.dumps')
    @mock.patch('anydo_cli.lib.outputFormat.yaml.dump')
    def test_print_with_format_prints_yaml(self, dump, dumps):
        expected_thing_to_print = {'test': 'test'}
        print_with_format(expected_thing_to_print, OutputFormat.YAML)
        dump.assert_called_once_with(expected_thing_to_print)
        dumps.assert_not_called()
