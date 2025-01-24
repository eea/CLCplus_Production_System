import json
import logging
from datetime import timedelta
import requests
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
import time

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(7),
    "retry_delay": timedelta(seconds=120),
    "catchup_by_default": False,
    'retries': 6,
    'email': ['elena.jung@gaf.de'],
    'email_on_failure': True,
    'email_on_retry': False,
    'execution_timeout': timedelta(hours=2.5),
    'queue': 'clc_test_prepare_samples_queue'
}

SAMPLE_EXTRACTION_URL = "sample-extraction-service.gaf-test"


def get_data_from_payload(param_name: str, data_type, **kwargs):
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


def call_prepare_samples(**kwargs):
    pid = f"{kwargs['dag_run'].run_id}_{kwargs['task_instance'].try_number}"
    print(f"process id {pid}")
    
    start_date = get_data_from_payload("start_date", str, **kwargs)
    end_date = get_data_from_payload("end_date", str, **kwargs)
    include_url = get_data_from_payload("include_url", str, **kwargs)
    out_path = get_data_from_payload("out_path", str, **kwargs)
    
    data = get_data_from_payload("data", dict, **kwargs)
    
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    
    service_url = SAMPLE_EXTRACTION_URL
    req_url = f"http://{service_url}:5000/prepare_samples"
    params = {
        "process_id": pid,
        "start_date": start_date,
        "end_date": end_date,
        "out_path": out_path,
        "include_url": include_url
    }
    logging.info(f"params: {params}")
    start = time.time()
    try:
        res = requests.post(req_url, params=params, data=json.dumps(data), headers=headers)
        res.raise_for_status()
    except requests.exceptions.HTTPError as httperror:
        print(f"sample extraction exception reason: {res.reason}")
        print(f"sample extraction exception text: {res.text}")
        raise httperror
    except Exception as e:
        raise e
    print(f"post request took: {int(time.time() - start)} seconds")


##########################
##########################
##########################

dag = DAG(
    "prepare_samples_dag_testing",
    default_args=default_args,
    schedule=None,
    max_active_runs=10,
    concurrency=10
)

prepare_samples_task = PythonOperator(
    task_id="prepare_samples",
    provide_context=True,
    python_callable=call_prepare_samples,
    dag=dag,
)


prepare_samples_task