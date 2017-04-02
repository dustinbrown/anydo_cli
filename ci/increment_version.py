import os
import pkg_resources
import sys

from ci.travis_after_all import TravisAfterAll


if __name__ == "__main__":
    try:
        travis_after_all = TravisAfterAll()
        if not travis_after_all.can_publish():
            raise SystemExit  # only one build can publish

        # TODO check for master branch only

        version = pkg_resources.get_distribution('anydo_cli').version
        split_version = version.split('.')
        try:
            split_version[-1] = str(int(split_version[-1]) + 1)
        except ValueError:
            # Add support for pre releases
            pass
        new_version = '.'.join(split_version)

        os.system("sed -i \"s/__version__ = '[0-9.]\+'/__version__ = '{}'/\" setup.py"
                  .format(new_version))
        os.system('git config --global user.email "automated@travisci.com"')
        os.system('git config --global user.name "Travis CI"')
        os.system("git add -u")
        os.system("git commit -m '[ci skip] Increase version to {}'"
                  .format(new_version))
        os.system('eval `ssh-agent -s`')
        os.system('ssh-add anydo_cli_rsa')
        os.system("git push")
    except Exception as e:
        sys.exit(2)
