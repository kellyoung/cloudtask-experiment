# cloudtask experiment

This is boilerplate code for creating a Google Cloud Platform Cloud Task Queue connected to a FastAPI Cloud Run service.

The objective of this project is to deploy a running Cloud Task Queue and a running FastAPI Cloud Run service that you can create tasks for.

I used [this tutorial](https://cloud.google.com/run/docs/triggering/using-tasks#command-line_1) as a basis. However, I felt there were some details missing that I hope this project helps fill in!

## prerequisites

- `gcloud` cli ([installation instructions](https://cloud.google.com/sdk/docs/install))
- python3 (I'm using v3.11.2)

You should also have a `Google Cloud Project` and its ID ready.

### configure `gcloud``

```
gcloud config set project <PROJECT_ID>
gcloud config set run/region <REGION>
```

## installation

```
pip install -r requirements.txt
```

## deploy Cloud Run service

`main.py` contains the code for the server. The route `/` accepts POST requests because we will be passing in a payload when we create the Cloud Task. The route simply gets the request body and logs it.

The `Dockerfile` runs the FastAPI server on container start up.

The first step to deploying the Cloud Run service is to build the image. You can choose the name for your image (i.e. "task-processor")

```
gcloud builds submit --tag gcr.io/<PROJECT_ID>/<IMAGE_NAME>
```

Once your image is built, you can deploy your Cloud Run service

```
gcloud run deploy <SERVICE_NAME> --image <IMAGE_TAG> --no-allow-unauthenticated
```

The `--no-allow-unauthenticated` flag creates a service that requires a token to be sent with the task. The service is configured with default settings. You can read more about the default settings and overriding them [here](https://cloud.google.com/sdk/gcloud/reference/run/deploy).

If you want to test out if the service is up and running, you can do something like:

```
curl -X POST <CLOUD_RUN_SERVICE_URL> -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{"<KEY>": "<VALUE>"}'
```

The `CLOUD_RUN_SERVICE_URL` can be found in the console.

## create a Cloud Task Queue

```
gcloud tasks queues create <QUEUE_ID>
```

You can read more about the default settings for the queue and how to override them [here](https://cloud.google.com/tasks/docs/configuring-queues#rate) 

## create a Service Account and grant access

First, create a service account.

```
gcloud iam service-accounts create <SERVICE_ACCOUNT_NAME> \
   --display-name <DISPLAYED_SERVICE_ACCOUNT_NAME>
```

Then, give your newly created Service Account permission to invoke your Cloud Run service by creating an IAM policy binding with the role of `run.invoker` between the Cloud Run service and the Service Account. This will be used to create Cloud Tasks with permissions to the service.

```
gcloud run services add-iam-policy-binding <CLOUD_RUN_SERVICE> \
   --member=serviceAccount:<SERVICE_ACCOUNT_NAME>@<PROJECT_ID>.iam.gserviceaccount.com \
   --role=roles/run.invoker
```

Finally, grant your newly created Service Account access to your project so it can take actions on the resources in your project.

```
gcloud projects add-iam-policy-binding <CLOUD_RUN_SERVICE> \
   --member=serviceAccount:<SERVICE_ACCOUNT_NAME>@<PROJECT_ID>.iam.gserviceaccount.com \ --role=roles/run.invoker
```

## create a Cloud Task

The script `create-task.py` will create a task that will be sent to your Cloud Run service.

You may need to provide credentials to your local environment first:

```
gcloud auth application-default login
```

Run the script:

```
python create-task.py --url "<CLOUD_RUN_SERVICE_URL>" --project "<GCLOUD_PROJECT_ID>" --service_account "<SERVICE_ACCOUNT_EMAIL>" --location "<QUEUE_LOCATION>" --queue "<CLOUD_TASK_QUEUE_ID>"
```

After running the script, it should print out information about the task created. You can ensure that the Cloud Task was sent to your Cloud Run service by looking at the logs of your Cloud Run service and confirming that you see a log line like `### PAYLOAD { "message": "CLOUD TASK EXPERIMENT TEST: <TASK_ID>" }`