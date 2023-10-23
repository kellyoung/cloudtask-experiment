import argparse
import random
import string
import json
from google.cloud import tasks_v2

parser = argparse.ArgumentParser(description='Create a Cloud Task.')
parser.add_argument(
    '--url', '-u', help="Cloud Run service URL", type=str, required=True)
parser.add_argument('--service_account', '-s',
                    help="Service Account email", type=str, required=True)
parser.add_argument('--project', '-p',
                    help="Google Cloud Project ID", type=str, required=True)
parser.add_argument('--location', '-l',
                    help="Location of queue/service", type=str, required=True)
parser.add_argument(
    '--queue', '-q', help="Cloud Task queue ID", type=str, required=True)

args = parser.parse_args()

url = args.url
service_account_email = args.service_account
project = args.project
location = args.location
queue = args.queue


def generate_task_id():
    prefix = 'experiment-task-'
    random_digits = ''.join(random.choice(string.digits) for i in range(5))
    return prefix + random_digits


def create_task(url, service_account_email, project, location, queue):
    task_id = generate_task_id()
    json_payload = {
        "message": "CLOUD TASK EXPERIMENT TEST: {}".format(task_id)
    }

    client = tasks_v2.CloudTasksClient()
    task_request = tasks_v2.Task(
        http_request=tasks_v2.HttpRequest(
            http_method=tasks_v2.HttpMethod.POST,
            url=url,
            oidc_token=tasks_v2.OidcToken(
                service_account_email=service_account_email,
            ),
            headers={"Content-type": "application/json"},
            body=json.dumps(json_payload).encode(),
        ),
        name=(
            client.task_path(project, location, queue, task_id)
        ),
    )

    created_task = client.create_task(
        tasks_v2.CreateTaskRequest(
            # The queue to add the task to
            parent=client.queue_path(project, location, queue),
            # The task itself
            task=task_request,
        )
    )
    return created_task


print(create_task(url, service_account_email, project, location, queue))
