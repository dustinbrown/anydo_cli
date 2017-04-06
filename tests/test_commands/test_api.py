import os
import pytest
import mock

from anydo_cli.lib.api import Api, PropertyNotSet
from anydo.api import AnyDoAPI


@pytest.fixture()
def clear_environment_variables():
    if 'ANYDO_USERNAME' in os.environ.keys():
        del os.environ['ANYDO_USERNAME']
    if 'ANYDO_PASSWORD' in os.environ.keys():
        del os.environ['ANYDO_PASSWORD']


@pytest.mark.usefixtures('clear_environment_variables')
class TestCli(object):
    fake_username = 'fake_username'
    fake_password = 'fake_password'

    # noinspection PyTypeChecker
    def test_no_username_set_throws_exception(self):
        with pytest.raises(PropertyNotSet):
            os.environ['ANYDO_PASSWORD'] = self.fake_password
            api = Api()

    # noinspection PyTypeChecker
    def test_no_password_set_throws_exception(self):
        with pytest.raises(PropertyNotSet):
            os.environ['ANYDO_USERNAME'] = self.fake_username
            api = Api()

    def test_username_and_password_from_environment_variable_is_correct(self):
        self.set_environment_credentials()

        api = Api()
        assert api.username == self.fake_username
        assert api.password == self.fake_password

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
            assert api.cfg == expected_config

    def test_connect_returns_correct_api_object(self):
        self.set_environment_credentials()
        api = Api()

        api_obj = api.connect()

        assert api_obj.__class__ == AnyDoAPI

    def set_environment_credentials(self):
        os.environ['ANYDO_USERNAME'] = self.fake_username
        os.environ['ANYDO_PASSWORD'] = self.fake_password





