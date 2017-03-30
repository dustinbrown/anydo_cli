import unittest
import anydo_cli.commands.cli


class TestCli(unittest.TestCase):
    def test_main(self):
        self.assertTrue(anydo_cli.commands.cli.main())
