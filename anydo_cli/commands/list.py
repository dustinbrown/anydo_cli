import time

import click
from anydo_cli.lib.api import Api
from anydo_cli.lib.outputFormat import OutputFormat, print_with_format


@click.group()
@click.option('-o', '--output-format', type=click.Choice(OutputFormat.valid_formats()),
              help='Type of output format', default=OutputFormat.JSON)
@click.pass_context
def list(ctx, output_format):
    ctx.obj = {}
    api = Api()
    ctx.obj['api'] = api.connect
    ctx.obj['output_format'] = output_format


@list.command()
@click.option('-t', '--title', is_flag=True, help='Show only titles')
@click.pass_context
def tasks(ctx, title: bool):
    """
    List all tasks. By default, this command will return a list of tasks with each task containing
    the full payload from anydo.
    """
    api = ctx.obj['api']
    raw_tasks = [task for task in api().get_all_tasks()]
    output_tasks = raw_tasks
    if title:
        output_tasks = [task['title'] for task in raw_tasks]

    print_with_format(output_tasks, ctx.obj['output_format'])


@list.command()
@click.pass_context
def due_tasks(ctx):
    """
    List all tasks that are currenty due. By default, this command returns a list of titles. 
    """
    api = ctx.obj['api']
    current_time_in_epoch = int(time.time()) * 1000.0
    due_tasks = [task for task in api().get_all_tasks()
                 if current_time_in_epoch > task['dueDate'] and task['status'] != 'CHECKED']
    if not due_tasks:
        return
    else:
        print_with_format([task['title'] for task in due_tasks], ctx.obj['output_format'])
