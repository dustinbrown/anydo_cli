#!/usr/bin/env python3
import logging

import click
import pkg_resources

from anydo_cli.lib.dynamic_commands import MyCLI

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

version = pkg_resources.get_distribution("anydo_cli").version


@click.group(cls=MyCLI)
@click.version_option(version, message='%(version)s')
def entry_point():
    """anydo_cli"""
