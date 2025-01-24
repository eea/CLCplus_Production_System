import json
import logging
import time
from datetime import timedelta

import airflow
import requests
from airflow import DAG
from airflow.exceptions import AirflowFailException
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(7),
    "retry_delay": timedelta(seconds=120),
    "catchup_by_default": False,
    "retries": 6,
    "email": ["christian.siegert@gaf.de", "christian.koehler@gaf.de"],
    "email_on_failure": True,
    "email_on_retry": False,
    "execution_timeout": timedelta(hours=2.5),
    "queue": "clc_prod_prepare_samples_queue",
}

SAMPLE_EXTRACTION_URL = "sample-extraction-service.gaf-prod"


def get_data_from_payload(param_name: str, data_type, **kwargs):
    try:
        data = kwargs["dag_run"].conf[param_name]
        print(f"{param_name} from api: {data}")
    except KeyError:
        msg = f"The following parameter is missing in the payload: {param_name!r}!"
        raise AirflowFailException(msg) from None
    except Exception as e:
        msg = f"something went wrong with retrieving the {param_name!r}!"
        raise Exception(msg) from e

    if not isinstance(data, data_type):
        raise AirflowFailException(f"{param_name} is not of type {data_type}")

    return data


def call_prepare_samples(**kwargs):
    pid = f"{kwargs['dag_run'].run_id}_{kwargs['task_instance'].try_number}"
    print(f"process id: {pid}")

    start_date = get_data_from_payload("start_date", str, **kwargs)
    end_date = get_data_from_payload("end_date", str, **kwargs)
    include_url = get_data_from_payload("include_url", str, **kwargs)
    out_path = get_data_from_payload("out_path", str, **kwargs)

    data = get_data_from_payload("data", dict, **kwargs)

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    service_url = SAMPLE_EXTRACTION_URL
    req_url = f"http://{service_url}:5000/prepare_samples"
    params = {
        "process_id": pid,
        "start_date": start_date,
        "end_date": end_date,
        "out_path": out_path,
        "include_url": include_url,
    }
    logging.info(f"params: {params}")
    start = time.perf_counter()
    try:
        res = requests.post(req_url, params=params, data=json.dumps(data), headers=headers)
        res.raise_for_status()
    except requests.exceptions.HTTPError as httperror:
        if res.status_code in {400, 404}:
            # no need to retry, if there is nothing available ...
            raise AirflowFailException(res.text) from httperror
        print(f"sample extraction exception reason: {res.reason}")
        print(f"sample extraction exception text: {res.text}")
        raise httperror

    print(f"post request took: {time.perf_counter() - start:.2f} seconds.")


##########################
##########################
##########################

dag = DAG(
    "prepare_samples_dag",
    default_args=default_args,
    schedule=None,
    max_active_runs=12,
    max_active_tasks=10,
)

prepare_samples_task = PythonOperator(
    task_id="prepare_samples",
    provide_context=True,
    python_callable=call_prepare_samples,
    dag=dag,
)


prepare_samples_task
