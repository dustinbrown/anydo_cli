import click
import mock
import pytest

from anydo_cli.lib.dynamic_commands import InvalidCommand, MyCLI


class TestCli(object):
    @pytest.fixture(scope="class")
    def cli(self) -> MyCLI:
        return MyCLI(help="testing")

    def test_list_commands(self, cli):
        assert isinstance(cli.list_commands({}), list)
        assert len(cli.list_commands({})) > 0

    @mock.patch('anydo_cli.lib.dynamic_commands.os.listdir')
    @mock.patch('anydo_cli.lib.dynamic_commands.open')
    @mock.patch('anydo_cli.lib.dynamic_commands.eval')
    @mock.patch('anydo_cli.lib.dynamic_commands.compile')
    def test_list_commands_gathers_correct_commands(self, compile, eval, open, listdir, cli):
        listdir.return_value = ['bad.txt']
        cli.list_commands({})
        open.assert_not_called()

    def test_get_command(self, cli):
        assert isinstance(cli.get_command({}, 'list'), click.core.Command)

    def test_invalid_command_raises(self, cli):
        # noinspection PyTypeChecker
        with pytest.raises(InvalidCommand):
            cli.get_command({}, 'bananas')