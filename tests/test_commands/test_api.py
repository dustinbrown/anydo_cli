import unittest

import os
import pytest
import mock
from unittest.mock import Mock

from anydo_cli.lib.api import Api, PropertyNotSet
from anydo.api import AnyDoAPI


@pytest.fixture()
def clear_environment_variables():
    if 'ANYDO_USERNAME' in os.environ.keys():
        del os.environ['ANYDO_USERNAME']
    if 'ANYDO_PASSWORD' in os.environ.keys():
        del os.environ['ANYDO_PASSWORD']


@pytest.fixture()
def mock_open():
    m = unittest.mock.mock_open(read_data='---\nANYDO_USERNAME: username\n')
    with mock.patch('anydo_cli.lib.api.open', m):
        yield


@pytest.mark.usefixtures('clear_environment_variables', 'mock_open')
class TestCli(object):
    fake_username = 'fake_username'
    fake_password = 'fake_password'

    # noinspection PyTypeChecker
    @mock.patch('anydo_cli.lib.api.os.path.isfile')
    def test_no_username_set_throws_exception(self, isfile):
        isfile.return_value = False
        with pytest.raises(PropertyNotSet):
            os.environ['ANYDO_PASSWORD'] = self.fake_password
            Api()

    # noinspection PyTypeChecker
    @mock.patch('anydo_cli.lib.api.os.path.isfile')
    def test_no_password_set_throws_exception(self, isfile):
        isfile.return_value = False
        with pytest.raises(PropertyNotSet):
            os.environ['ANYDO_USERNAME'] = self.fake_username
            Api()

    @mock.patch('anydo_cli.lib.api.os.path.isfile')
    def test_username_and_password_from_environment_variable_is_correct(self, isfile):
        isfile.return_value = False
        self.set_environment_credentials()
        api = Api()

        assert api.username == self.fake_username
        assert api.password == self.fake_password

    @mock.patch('anydo_cli.lib.api.os.path.isfile')
    def test_config_file_returns_config(self, isfile):
        self.set_environment_credentials()
        isfile.return_value = True

        expected_config = {'ANYDO_USERNAME': 'username'}
        api = Api()
        assert api.cfg == expected_config

    @mock.patch('anydo_cli.lib.api.os.path.isfile')
    def test_connect_returns_correct_api_object(self, isfile):
        isfile.return_value = False
        self.set_environment_credentials()
        api = Api()

        api_obj = api.connect()

        assert api_obj.__class__ == AnyDoAPI

    def set_environment_credentials(self):
        os.environ['ANYDO_USERNAME'] = self.fake_username
        os.environ['ANYDO_PASSWORD'] = self.fake_password





