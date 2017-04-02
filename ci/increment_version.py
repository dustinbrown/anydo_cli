import os
import pkg_resources
import sys
import logging

from ci.travis_after_all import TravisAfterAll

log = logging.getLogger("travis.increment_version")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

BRANCHES_ALLOWED_TO_AUTO_INCREMENT = ['master']
PROJECT_NAME = sys.argv[1]


def allowed_branch() -> bool:
    return os.getenv('TRAVIS_BRANCH') in BRANCHES_ALLOWED_TO_AUTO_INCREMENT


def assert_this_build_can_auto_increment():
    if not allowed_branch():
        log.info('Not allowed branched, branch set to {}'.format(os.getenv('TRAVIS_BRANCH')))
        raise SystemExit
    travis_after_all = TravisAfterAll()
    if not travis_after_all.can_publish():
        raise SystemExit  # only one build can publish


def set_version() -> str:
    new_version = identify_version()
    log.info('setting new version to: {}'.format(new_version))
    os.system("sed -i \"s/__version__ = '[0-9.]\+'/__version__ = '{}'/\" setup.py"
              .format(new_version))

    return new_version


def identify_version() -> str:
    parsed_version = pkg_resources.get_distribution(PROJECT_NAME).version
    split_version = parsed_version.split('.')
    try:
        split_version[-1] = str(int(split_version[-1]) + 1)
    except ValueError:
        # Add support for pre releases
        pass
    new_version = '.'.join(split_version)
    return new_version


def commit_and_push_new_version(new_version: str):
    os.system('git config --global user.email "automated@travisci.com"')
    os.system('git config --global user.name "Travis CI"')
    os.system("git add -u")
    os.system("git commit -m '[ci skip] Increase version to {}'"
              .format(new_version))
    os.system('eval `ssh-agent -s`')
    os.system('ssh-add {}_rsa'.format(PROJECT_NAME))
    os.system("git push")


if __name__ == "__main__":
    try:
        assert_this_build_can_auto_increment()
        version = set_version()
        commit_and_push_new_version(version)
    except Exception as e:
        sys.exit(2)
