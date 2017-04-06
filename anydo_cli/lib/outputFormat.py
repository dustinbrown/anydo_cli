import json
# noinspection PyPackageRequirements
import yaml


class OutputFormat(object):
    YAML = 'yaml'
    JSON = 'json'

    @classmethod
    def valid_formats(cls):
        return [OutputFormat.JSON, OutputFormat.YAML]


def print_with_format(thing_to_print, output_format):
    if output_format == OutputFormat.JSON:
        print(json.dumps(thing_to_print))
    elif output_format == OutputFormat.YAML:
        print(yaml.dump(thing_to_print))
