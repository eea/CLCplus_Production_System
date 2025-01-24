import json
from datetime import timedelta
import requests
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(7),
    "retry_delay": timedelta(minutes=3),
    "catchup_by_default": False,
    'retries': 2,
    'email': ['elena.jung@gaf.de'],
    'email_on_failure': True,
    'email_on_retry': False,
    'execution_timeout': timedelta(hours=2.5),
    'queue': 'clc_test_apply_model_queue'
}

CFS_URL = "calculate-feature-service.gaf-test"
APPLY_MODEL_URL = "apply-model-service.gaf-test"


def get_data_from_payload(param_name: str, data_type,  **kwargs):
    try:
        data = kwargs['dag_run'].conf[param_name]
        print(f"{param_name} from api: {data}")
    except KeyError:
        raise KeyError(
            f"The following parameter cannot be found in the payload object: {param_name}")
    except Exception as e:
        raise Exception(f"something went wrong with retrieving the {param_name}: {e}")

    if not isinstance(data, data_type):
        raise TypeError(f"{param_name} is not of type {data_type}")

    return data


def call_cfs(**kwargs):
    # this is a test to see if the changes are pulled into Airflow
    pid = f"{kwargs['dag_run'].run_id}_{kwargs['task_instance'].try_number}"
    print(f"process id {pid}")

    epsg = get_data_from_payload("epsg", int, **kwargs)
    resampling = get_data_from_payload("resampling", str, **kwargs)
    cloudmask_type = get_data_from_payload("cloudmask_type", str, **kwargs)
    data_type = get_data_from_payload("data_type", str, **kwargs)
    path_prefix = get_data_from_payload("path_prefix", str, **kwargs)
    use_cache = get_data_from_payload("use_cache", bool, **kwargs)
    data_source = get_data_from_payload("data_source", str, **kwargs)

    params = {"process_id": pid, "path_prefix": path_prefix, "to_upload": True, "use_cache": use_cache,
              "resolution": 10, "data_source": data_source, "epsg": epsg,
              "resampling": resampling, "cloudmask_type": cloudmask_type, "data_type": data_type}

    data = get_data_from_payload("data", dict, **kwargs)
    
    input_scene_ids = data["scene_ids"] 
    print(f"the length of scene ids is : {len(input_scene_ids)}")

    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'My User Agent 1.0'}

    service_url = CFS_URL
    request_url = f"http://{service_url}:5000/s2scenesfeatures"

    res = requests.post(request_url, params=params, data=json.dumps(data), headers=headers)

    print(f"process id {pid}: {res.text}")
    res.raise_for_status()
    # print(f"missing_images: {res.json()['missing_images']}")
    # print(f"filtered_out: {res.json()['filtered_out']}")
    print(f"number of acquisition dates: {len(res.json()['results']['metadata']['acquisition_dates'])}")

    ti = kwargs['ti']
    ti.xcom_push(key="tif_files", value=res.json()["results"])


def format_filenames_from_cfs(files):
    print(f"files from cfs: {files}")
    apply_model_data = {}

    # feature = e.g. NDVI
    for feature in sorted(files.keys()):
        # metric = e.g. raw
        metric_filename = files[feature]
        if len(metric_filename) > 1:
            raise Exception(f"Only one metric is allowed, however, {len(metric_filename)} have been specified. {metric_filename}")
        for filename in metric_filename.values():
            if not isinstance(filename, str) or not filename.endswith(('.tif', '.tiff')):
                raise Exception(f"Input Filename: {filename} does not have tif extension")
            apply_model_data[feature] = filename

    print(f"files correctly formatted: {apply_model_data}")
    return apply_model_data


def call_apply_model(**kwargs):
    run_id = kwargs['dag_run'].run_id
    pid = f"{run_id}_{kwargs['task_instance'].try_number}"
    print(f"process id {pid}")

    model_path = get_data_from_payload("model_path", str, **kwargs)

    params = {"process_id": pid, "model_path": model_path}

    ti = kwargs['ti']
    results = ti.xcom_pull(key='tif_files', task_ids='calculate_feature_service')
    files = results["data"]
    print(f"files from cfs: {files}")
    formatted_files = format_filenames_from_cfs(files)

    acquisition_dates = results["metadata"]["acquisition_dates"] 
    print(f"acquisition_dates: {acquisition_dates}")
    print(f"number of acquisition dates: {len(acquisition_dates)}")

    scene_ids_by_index = get_data_from_payload("scene_ids_by_index", dict, **kwargs)

    data = {'inputs': formatted_files, 'acquisition_dates': acquisition_dates, 'scene_ids_by_index': scene_ids_by_index}

    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    service_url = APPLY_MODEL_URL
    request_url = f"http://{service_url}:5000/applymodel"

    res = requests.post(request_url, params=params, data=json.dumps(data), headers=headers)

    print(f"process id {pid}: {res.text}")
    res.raise_for_status()


##########################
##########################
##########################

dag = DAG(
    "apply_model_dag_testing",
    default_args=default_args,
    schedule=None,
    max_active_runs=2,
    concurrency=2
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
    dag=dag,
)

cfs >> apply_model