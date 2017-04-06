import click
import os

import anydo_cli


class InvalidCommand(Exception):
    pass


class MyCLI(click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super(MyCLI, self).__init__(*args, **kwargs)

    def list_commands(self, ctx) -> list:
        rv = list(MyCLI._gather_commands().keys())
        return rv

    @staticmethod
    def _gather_commands():
        plugin_folder = os.path.join(os.path.dirname(anydo_cli.__file__), 'commands')
        ns = {}
        for filename in os.listdir(plugin_folder):
            if not filename.endswith('.py'):
                continue
            fn = os.path.join(plugin_folder, filename)
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
        commands = {k: v for (k, v) in ns.items() if isinstance(v, click.core.Group)}
        return commands

    def get_command(self, ctx, name) -> click.core.Command:
        try:
            return MyCLI._gather_commands()[name]
        except KeyError:
            raise InvalidCommand("Command: '{}' is not a valid command".format(name))