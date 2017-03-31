import os
import pkg_resources


if __name__ == "__main__":
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
    os.system("git add -u")
    os.system("git commit -m '[ci skip] Increase version to {}'"
              .format(new_version))
    os.system('eval `ssh-agent -s`')
    os.system('ssh-add anydo_cli_rsa')
    os.system("git push")