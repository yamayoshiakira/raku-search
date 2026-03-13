# yy-search application/tools/task.py

import json

from google.cloud import tasks_v2


PROJECT = "yy-search"
LOCATION = "us-central1"
QUEUE = "default"


def put(data):
    """ data type Dict """

    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(PROJECT, LOCATION, QUEUE)

    payload = json.dumps(data)

    task = {
        'app_engine_http_request': {
            'http_method': 'POST',
            'relative_uri': "/task_put",
            'headers': {
                'Content-Type': "application/json"
            },
            'body': payload.encode(),
        }
    }

    response = client.create_task(parent, task)

    return(response)
