#!/usr/bin/env python3
import json

import os
import time

# from anydo.api import AnyDoAPI
# password = os.getenv('ANYDO_PASSWORD')
# api = AnyDoAPI(username='dustinjamesbrown@gmail.com', password=password)
current_time_in_epoch = int(time.time()) * 1000.0
# print(current_time_in_epoch)
# raise SystemExit


def main():
    print('it works')
    return True


# def get_due_tasks():
#     due_tasks = [task for task in api.get_all_tasks()
#                  if current_time_in_epoch > task['dueDate'] and task['status'] != 'CHECKED']
#     return [task['title'] for task in due_tasks]


# print(json.dumps(get_due_tasks()))
# print(json.dumps(api.get_all_tasks()))