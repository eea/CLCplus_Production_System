import logging
from datetime import timedelta
import requests
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException
import time

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(7),
    "retry_delay": timedelta(seconds=60),
    "catchup_by_default": False,
    'retries': 2,
    'email': ['elena.jung@gaf.de'],
    'email_on_failure': True,
    'email_on_retry': False,
    'execution_timeout': timedelta(hours=2.5),
    'queue': 'clc_test_sample_extract_queue'
}

SAMPLE_EXTRACTION_URL = "sample-extraction-service.gaf-test"


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


def call_sample_extraction_service(index, **kwargs):
    pid = f"{kwargs['dag_run'].run_id}_{kwargs['task_instance'].try_number}"
    print(f"process id {pid}")

    s2_params_list = get_data_from_payload("s2_parameter_list", list, **kwargs)
    
    param_list_length = len(s2_params_list)
    
    if param_list_length > 10:
        raise Exception(f"the parameter list for sample extraction contains more than 10 elements: {param_list_length}")

    if param_list_length < index + 1:
        raise AirflowSkipException

    s2_params = s2_params_list[index]

    if ("product_id" or "bands") not in s2_params.keys():
        raise Exception(f"product_id or bands not defined in params: {s2_params}")

    product_id = s2_params["product_id"]
    bands = s2_params["bands"]

    service_url = SAMPLE_EXTRACTION_URL
    req_url = f"http://{service_url}:5000/extract_sentinel_2"
    params = {
        "process_id": pid,
        "product_id": product_id,
        "bands": bands
    }
    logging.info(f"params: {params}")
    start = time.time()
    try:
        res = requests.post(req_url, params=params)
        res.raise_for_status()
    except requests.exceptions.HTTPError as httperror:
        print(f"sample extraction exception text: {res.reason}")
        print(f"sample extraction exception text: {res.text}")
        raise httperror
    except Exception as e:
        raise e
    print(f"post request took: {int(time.time() - start)} seconds")

def call_sample_extraction_service_1(**kwargs):
    index = 0
    call_sample_extraction_service(index, **kwargs)


def call_sample_extraction_service_2(**kwargs):
    index = 1
    call_sample_extraction_service(index, **kwargs)


def call_sample_extraction_service_3(**kwargs):
    index = 2
    call_sample_extraction_service(index, **kwargs)


def call_sample_extraction_service_4(**kwargs):
    index = 3
    call_sample_extraction_service(index, **kwargs)


def call_sample_extraction_service_5(**kwargs):
    index = 4
    call_sample_extraction_service(index, **kwargs)


def call_sample_extraction_service_6(**kwargs):
    index = 5
    call_sample_extraction_service(index, **kwargs)


def call_sample_extraction_service_7(**kwargs):
    index = 6
    call_sample_extraction_service(index, **kwargs)


def call_sample_extraction_service_8(**kwargs):
    index = 7
    call_sample_extraction_service(index, **kwargs)


def call_sample_extraction_service_9(**kwargs):
    index = 8
    call_sample_extraction_service(index, **kwargs)


def call_sample_extraction_service_10(**kwargs):
    index = 9
    call_sample_extraction_service(index, **kwargs)


##########################
##########################
##########################

dag = DAG(
    "sample_extraction_dag_testing",
    default_args=default_args,
    schedule=None,
    max_active_runs=10,
    concurrency=10
)

sample_extraction_task_1 = PythonOperator(
    task_id="sample_extraction_1",
    provide_context=True,
    python_callable=call_sample_extraction_service_1,
    dag=dag,
)

sample_extraction_task_2 = PythonOperator(
    task_id="sample_extraction_2",
    provide_context=True,
    python_callable=call_sample_extraction_service_2,
    dag=dag,
)

sample_extraction_task_3 = PythonOperator(
    task_id="sample_extraction_3",
    provide_context=True,
    python_callable=call_sample_extraction_service_3,
    dag=dag,
)

sample_extraction_task_4 = PythonOperator(
    task_id="sample_extraction_4",
    provide_context=True,
    python_callable=call_sample_extraction_service_4,
    dag=dag,
)

sample_extraction_task_5 = PythonOperator(
    task_id="sample_extraction_5",
    provide_context=True,
    python_callable=call_sample_extraction_service_5,
    dag=dag,
)

sample_extraction_task_6 = PythonOperator(
    task_id="sample_extraction_6",
    provide_context=True,
    python_callable=call_sample_extraction_service_6,
    dag=dag,
)

sample_extraction_task_7 = PythonOperator(
    task_id="sample_extraction_7",
    provide_context=True,
    python_callable=call_sample_extraction_service_7,
    dag=dag,
)

sample_extraction_task_8 = PythonOperator(
    task_id="sample_extraction_8",
    provide_context=True,
    python_callable=call_sample_extraction_service_8,
    dag=dag,
)

sample_extraction_task_9 = PythonOperator(
    task_id="sample_extraction_9",
    provide_context=True,
    python_callable=call_sample_extraction_service_9,
    dag=dag,
)

sample_extraction_task_10 = PythonOperator(
    task_id="sample_extraction_10",
    provide_context=True,
    python_callable=call_sample_extraction_service_10,
    dag=dag,
)

sample_extraction_task_1 >> sample_extraction_task_2 >> sample_extraction_task_3 >> \
    sample_extraction_task_4 >> sample_extraction_task_5 >> sample_extraction_task_6 >> \
    sample_extraction_task_7 >> sample_extraction_task_8 >> sample_extraction_task_9 >> \
    sample_extraction_task_10