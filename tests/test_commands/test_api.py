import unittest
import mock


import os

from anydo_cli.lib.api import Api, PropertyNotSet
from anydo.api import AnyDoAPI

class TestCli(unittest.TestCase):
    # noinspection PyAttributeOutsideInit
    def setUp(self):
        self.fake_user = 'fake_user'
        self.fake_password = 'fake_password'

    def tearDown(self):
        self.clear_environment_variables()

    def test_no_username_set_throws_exception(self):
        self.clear_environment_variables()
        os.environ['ANYDO_PASSWORD'] = self.fake_password
        self.assertRaises(PropertyNotSet, Api)

    def test_no_password_set_throws_exception(self):
        self.clear_environment_variables()
        os.environ['ANYDO_USERNAME'] = self.fake_user
        self.assertRaises(PropertyNotSet, Api)

    def test_username_and_password_from_environment_variable_is_correct(self):
        self.clear_environment_variables()
        self.set_environment_credentials()

        api = Api()
        self.assertTrue(api.username == self.fake_user)
        self.assertTrue(api.password == self.fake_password)

    @mock.patch('anydo_cli.lib.api.os.path.isfile')
    @mock.patch('anydo_cli.lib.api.yaml.load')
    def test_config_file_returns_config(self, load, isfile):
        self.set_environment_credentials()

        isfile.return_value = True

        with mock.patch('anydo_cli.lib.api.open', create=True) as mock_open:
            mock_open.return_value = mock.MagicMock()
            expected_config = {'test': 'test'}
            load.return_value = expected_config

            api = Api()
            self.assertEquals(api.cfg, expected_config)

    def test_connect_returns_correct_api_object(self):
        self.set_environment_credentials()
        api = Api()

        api_obj = api.connect()

        self.assertEquals(api_obj.__class__, AnyDoAPI)

    def set_environment_credentials(self):
        os.environ['ANYDO_USERNAME'] = self.fake_user
        os.environ['ANYDO_PASSWORD'] = self.fake_password

    def clear_environment_variables(self):
        if 'ANYDO_USERNAME' in os.environ.keys():
            del os.environ['ANYDO_USERNAME']
        if 'ANYDO_PASSWORD' in os.environ.keys():
            del os.environ['ANYDO_PASSWORD']




