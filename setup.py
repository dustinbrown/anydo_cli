from setuptools import setup, find_packages
from setuptools.command.test import test
import sys


class Tox(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


setup(name="anydo_cli",
      version="0.0.1",
      description="cli for python-anydo",
      license="MIT",
      install_requires=["python-anydo"],
      author="Dustin Brown",
      author_email="dustinjamesbrown@gmail.com",
      url="https://github.com/dustinbrown/anydo_cli",
      packages=find_packages(),
      keywords="anydo",
      tests_require=['tox-travis', 'pycodestyle'],
      cmdclass={'test': Tox},
      zip_safe=True,
      entry_points={
          'console_scripts': [
              'anydo = anydo_cli.commands.cli:main'
          ]
      })