import json
from datetime import timedelta
import requests
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(7),
    "retry_delay": timedelta(minutes=1),
    "catchup_by_default": False,
    "retries": 10,
    "email": ["christian.siegert@gaf.de", "christian.koehler@gaf.de"],
    "email_on_failure": True,
    "email_on_retry": False,
    "execution_timeout": timedelta(hours=5),
    "queue": "clc_prod_apply_model_queue",
}

CONCURRENCY = 20  # should be ~ 2 * number_of_cfs_instances

CFS_URL = "calculate-feature-service.gaf-prod"
APPLY_MODEL_URL = "apply-model-service.gaf-prod"

CFS_DATA_SOURCE = "element_aws_clc"

print("testing sync")


def get_data_from_payload(param_name: str, data_type, **kwargs):
    try:
        data = kwargs["dag_run"].conf[param_name]
    except KeyError:
        msg = f"The following parameter cannot be found in the payload object: {param_name}"
        raise KeyError(msg) from None
    except Exception as e:
        raise Exception(f"something went wrong with retrieving the {param_name}: {e}") from e

    if not isinstance(data, data_type):
        raise TypeError(f"{param_name} is not of type {data_type}")

    return data


def call_cfs(**kwargs):
    pid = f"{kwargs['dag_run'].run_id}_{kwargs['task_instance'].try_number}"
    print(f"process id {pid}")

    epsg = get_data_from_payload("epsg", int, **kwargs)
    resampling = get_data_from_payload("resampling", str, **kwargs)
    cloudmask_type = get_data_from_payload("cloudmask_type", str, **kwargs)
    data_type = get_data_from_payload("data_type", str, **kwargs)
    path_prefix = get_data_from_payload("path_prefix", str, **kwargs)
    use_cache = kwargs["ti"].xcom_pull(task_ids="calculate_feature_service", key="use_cache")
    if use_cache is None:
        use_cache = get_data_from_payload("use_cache", bool, **kwargs)

    params = {
        "process_id": pid,
        "path_prefix": path_prefix,
        "to_upload": True,
        "use_cache": use_cache,
        "resolution": 10,
        "data_source": CFS_DATA_SOURCE,
        "epsg": epsg,
        "resampling": resampling,
        "cloudmask_type": cloudmask_type,
        "data_type": data_type,
    }

    data = get_data_from_payload("data", dict, **kwargs)
    # automatically produce Data Score Layer
    data["features"]["SCL"] = {"values": ["COUNT"]}

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    service_url = CFS_URL
    request_url = f"http://{service_url}:5000/s2scenesfeatures"

    print(f"Calling CFS with params: {params}, data: {data}.")
    res = requests.post(request_url, params=params, data=json.dumps(data), headers=headers)

    print(f"received response: {res.text}")
    res.raise_for_status()

    # print(f"missing_images: {res.json()['missing_images']}")
    # print(f"filtered_out: {res.json()['filtered_out']}")

    ti = kwargs["ti"]
    ti.xcom_push(key="tif_files", value=res.json()["results"])


def format_filenames_from_cfs(files):
    print(f"files from cfs: {files}")
    apply_model_data = {}

    # feature = e.g. NDVI
    for feature in sorted(files.keys()):
        # metric = e.g. raw
        metric_filename = files[feature]
        if len(metric_filename) > 1:
            msg = (
                f"Only one metric is allowed, however, {len(metric_filename)} have been specified."
                " {metric_filename}"
            )
            raise ValueError(msg)
        for metric, filename in metric_filename.items():
            if feature == "SCL" and metric == "COUNT":
                continue
            if not isinstance(filename, str) or not filename.endswith(('.tif', '.tiff')):
                raise Exception(f"Input Filename: {filename} does not have tif extension")
            apply_model_data[feature] = filename

    print(f"files correctly formatted: {apply_model_data}")
    return apply_model_data


def call_apply_model(**kwargs):
    run_id = kwargs["dag_run"].run_id
    pid = f"{run_id}_{kwargs['task_instance'].try_number}"
    print(f"process id {pid}")

    model_path = get_data_from_payload("model_path", str, **kwargs)

    params = {"process_id": pid, "model_path": model_path}

    ti = kwargs["ti"]
    results = ti.xcom_pull(key="tif_files", task_ids="calculate_feature_service")
    files = results["data"]
    print(f"files from cfs: {files}")
    formatted_files = format_filenames_from_cfs(files)

    acquisition_dates = results["metadata"]["acquisition_dates"]
    print(f"acquisition_dates: {acquisition_dates}")
    print(f"number of acquisition dates: {len(acquisition_dates)}")

    scene_ids_by_index = get_data_from_payload("scene_ids_by_index", dict, **kwargs)

    data = {
        "inputs": formatted_files,
        "acquisition_dates": acquisition_dates,
        "scene_ids_by_index": scene_ids_by_index,
    }

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    service_url = APPLY_MODEL_URL
    request_url = f"http://{service_url}:5000/applymodel"

    res = requests.post(request_url, params=params, data=json.dumps(data), headers=headers)

    print(f"process id {pid}: {res.text}")
    res.raise_for_status()


def rerun_cfs_and_apply_model_on_failure(context):
    task_instance = context["ti"]
    task_id = task_instance.task_id
    execution_date = context["execution_date"].isoformat()
    print("AMS failed, attempting to retry with CFS use_cache set to False.")

    # Check if already retried
    already_retried = task_instance.xcom_pull(key="already_retried", task_ids=task_id)
    if already_retried:
        raise Exception("Task failed after retry.")

    # If not, set that it's retried
    task_instance.xcom_push(key="already_retried", value=True)

    if task_id == "apply_model_service" and task_instance.state == "failed":
        print("Rerunnning CFS and AMS without cache due to image caching failure")
        dag_id = context["dag"].dag_id
        dag_run_id = context["dag_run"].run_id

        # Set use_cache to False in the cfs task
        cfs_task = context["dag_run"].get_task_instance("calculate_feature_service")
        cfs_task.xcom_push(key="use_cache", value=False)

        # Trigger the rerun of cfs task and all downstream tasks, i.e. apply_model
        rerun_cfs = BashOperator(
            task_id="rerun_cfs",
            bash_command=(
                f"airflow tasks clear {dag_id} --task-regex calculate_feature_service --upstream "
                f"--downstream --start-date {execution_date} --end-date {execution_date}"
            ),
            dag=context["dag"],
        )
        rerun_cfs.execute(context=context)

        raise Exception(
            f"Rerunning dag '{dag_id}' with run_id '{dag_run_id}' due to failure in task '{task_id}'"
        )


##########################
##########################
##########################

dag = DAG(
    "apply_model_dag",
    default_args=default_args,
    schedule=None,
    max_active_runs=CONCURRENCY + 2,
    max_active_tasks=CONCURRENCY,
)

cfs = PythonOperator(
    task_id="calculate_feature_service",
    provide_context=True,
    python_callable=call_cfs,
    dag=dag,
)

apply_model = PythonOperator(
    task_id="apply_model_service",
    provide_context=True,
    python_callable=call_apply_model,
    execution_timeout=timedelta(hours=1),
    on_failure_callback=rerun_cfs_and_apply_model_on_failure,
    dag=dag,
)

cfs >> apply_model
