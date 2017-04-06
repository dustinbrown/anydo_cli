import json
import yaml
import pytest
import mock
from unittest.mock import Mock
from click.testing import CliRunner

from anydo_cli.commands.list import list
from anydo_cli.lib.api import Api
from anydo.api import AnyDoAPI


class Data:
    tasks = [
        {"dueDate": 100000, "status": "CHECKED", "title": "completed_but_old"},
        {"dueDate": 100000, "status": "blah", "title": "old_and_uncompleted"},
        {"dueDate": 1000000000000, "status": "CHECKED", "title": "new_and_completed"}
    ]
    due_tasks_titles_expected = [
        "old_and_uncompleted"
    ]


class TestList(object):
    @pytest.mark.parametrize("args, expected_output, data", [
        (
            # Return all tasks in json
            ["tasks"],                  # command
            json.dumps(Data.tasks),     # expected data
            Data.tasks                  # mock returned data
        ),
        (
            # Return all tasks in yaml
            ["-o", "yaml", "tasks"],
            yaml.dump(Data.tasks),
            Data.tasks
        ),
        (
            # Return task titles in json
            ["tasks", "-t"],
            json.dumps([task["title"] for task in Data.tasks]),
            Data.tasks
        )
    ])
    @mock.patch("anydo_cli.commands.list.Api")
    def test_list_tasks(self, api, args, expected_output, data):
        TestList.mock_api(api, data)
        TestList.assert_output(args, expected_output)

    @pytest.mark.parametrize("args, expected_output, data", [
            (
                # Return due task in json
                ["due_tasks"],                                      # command
                json.dumps(Data.due_tasks_titles_expected),     # expected data
                Data.tasks                                      # mock returned data
            ),
            (
                # Return due task in yaml
                ["-o", "yaml", "due_tasks"],
                yaml.dump(Data.due_tasks_titles_expected),
                Data.tasks
            ),
            (
                # Return no tasks
                ["due_tasks"],
                '',
                []
            )
        ])
    @mock.patch("anydo_cli.commands.list.Api")
    def test_list_due_tasks(self, api, args, expected_output, data):
        TestList.mock_api(api, data)
        TestList.assert_output(args, expected_output)

    @staticmethod
    def mock_api(api: Mock, get_all_tasks: list):
        anydo_api_attrs = {"get_all_tasks.return_value": get_all_tasks}
        mock_api_connect = Mock(spec=AnyDoAPI, **anydo_api_attrs)
        api_attrs = {"connect.return_value": mock_api_connect}
        api.return_value = Mock(spec=Api, **api_attrs)

    @staticmethod
    def assert_output(args, expected_output):
        runner = CliRunner()
        result = runner.invoke(list, args=args)
        assert expected_output.strip() == result.output.strip()