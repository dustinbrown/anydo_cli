import pytest
from click.testing import CliRunner
from anydo_cli.commands.cli import entry_point, version


class TestCli(object):
    def test_entrypoint(self):
        runner = CliRunner()
        result = runner.invoke(entry_point)
        assert result.output != ''

    # not in love with having to supply a subcommand. http://click.pocoo.org/5/testing/
    @pytest.mark.parametrize('args, expected_output', [
        (['--version', 'list'], version),
    ])
    def test_correct_version_is_printed(self, args, expected_output):
        runner = CliRunner()
        result = runner.invoke(entry_point, args=args)
        assert expected_output == result.output.strip()
