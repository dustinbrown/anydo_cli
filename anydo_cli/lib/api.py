import os
import sys
import yaml
from typing import Union
import logging
from anydo.api import AnyDoAPI

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


class PropertyNotSet(Exception):
    pass


class Api(object):
    __ANYDO_USERNAME = 'ANYDO_USERNAME'
    __ANYDO_PASSWORD = 'ANYDO_PASSWORD'

    def __init__(self, username='', password=''):
        self.cfg = Api.load_config_file()
        self.username = username if username else self._get_username()
        self.password = password if password else self._get_password()

    def connect(self) -> AnyDoAPI:
        return AnyDoAPI(username=self.username, password=self.password)

    def _get_username(self) -> str:
        env_var = os.getenv(Api.__ANYDO_USERNAME)
        try:
            return env_var if env_var else self.cfg[Api.__ANYDO_USERNAME]
        except KeyError:
            raise PropertyNotSet('ANYDO_USERNAME not found as an environment variable or '
                                 'in ~/.anydo_cli.yaml')

    def _get_password(self) -> str:
        env_var = os.getenv(Api.__ANYDO_PASSWORD)
        try:
            return env_var if env_var else self.cfg[Api.__ANYDO_PASSWORD]
        except KeyError:
            raise PropertyNotSet('ANYDO_PASSWORD not found as an environment variable or '
                                 'in ~/.anydo_cli.yaml')

    @staticmethod
    def load_config_file() -> Union:
        config_file = os.path.join(os.path.expanduser('~'), '.anydo_cli.yaml')
        if not os.path.isfile(config_file):
            return {}
        else:
            with open(config_file) as fd:
                return yaml.safe_load(fd)

