#!/usr/bin/env python3
import logging

import click
import pkg_resources
import sys

from anydo_cli.lib.dynamic_commands import MyCLI

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

__version__ = '0.0.2'


@click.group(cls=MyCLI)
@click.version_option(__version__, message='%(version)s')
def entry_point():
    """anydo_cli"""
