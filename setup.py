from setuptools import setup, find_packages
from setuptools.command.test import test
import sys

__version__ = '0.0.2'


class Tox(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


setup(name='anydo_cli',
      version=__version__,
      description='cli for python-anydo',
      license='MIT',
      install_requires=['python-anydo', 'gitpython', 'click', 'pyyaml'],
      author='Dustin Brown',
      author_email='dustinjamesbrown@gmail.com',
      url='https://github.com/dustinbrown/anydo_cli',
      packages=find_packages(),
      keywords='anydo',
      tests_require=['tox-travis', 'pycodestyle', 'click', 'mock'],
      cmdclass={'test': Tox},
      zip_safe=True,
      entry_points={
          'console_scripts': [
              'anydo = anydo_cli.commands.cli:entry_point'
          ]
      })
