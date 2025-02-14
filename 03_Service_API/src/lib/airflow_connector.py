import requests
from geoville_keycloak_module_utils.keycloak_utils import get_bearer_token
from geoville_vault_module.vault.key_value_engine import get_kv_secret_list

from src.config import cnf
from src.init.init_variables import KC_CLIENT, VAULT_CLIENT

########################################################################################################################
# Constant definitions
########################################################################################################################

header_content_type = "application/json"


########################################################################################################################
# Method definition for triggering a DAG run on the Airflow scheduler via its API
########################################################################################################################

def create_order(user_id: str, service_dag_name: str, payload: dict):
    """ Creates a service order in Airflow

    This method submits a job to Airflow via Airflow Connector API

    Arguments:
        user_id (str): user ID that triggered the request
        service_dag_name (str): name of the service and DAG to be triggered
        payload (dict): payload of the request sent to the API

    Returns:
        dag_run_id (str): DAG run id of the submitted job

    """
    secrets = get_kv_secret_list(VAULT_CLIENT, cnf.APP_CONFIG.API_SECRET_PATH, cnf.APP_CONFIG.SECRET_MOUNT)

    response = requests.post(f"{secrets['airflow_connector_url']}/dag/run",
                             headers={
                                 "Authorization": get_bearer_token(KC_CLIENT,
                                                                   secrets['api_kc_user'], secrets['api_kc_password']),
                                 "Content-Type": header_content_type
                             },
                             json={
                                 "user_id": user_id,
                                 "dag_service_name": service_dag_name,
                                 "service_payload": payload
                             })

    return response


########################################################################################################################
# Method definition for querying the status of a DAG run
########################################################################################################################

def get_order_status(dag_run_id) -> dict:
    """ Submits a job to Airflow

    This method submits a job to Airflow via its API

    Arguments:
        dag_run_id (str): payload of the request sent to the API

    Returns:
        dag_run_id (str): DAG run id of the submitted job

    """

    secrets = get_kv_secret_list(VAULT_CLIENT, cnf.APP_CONFIG.API_SECRET_PATH, cnf.APP_CONFIG.SECRET_MOUNT)

    response = requests.get(f"{secrets['airflow_connector_url']}/dag/run/{dag_run_id}/status",
                            headers={
                                "Authorization": get_bearer_token(KC_CLIENT,
                                                                  secrets['api_kc_user'], secrets['api_kc_password']),
                                "Content-Type": header_content_type
                            })

    return response.json()


########################################################################################################################
# Method definition for aborting a DAG run
########################################################################################################################

def abort_order(dag_run_id) -> None:
    """ Aborts a job to Airflow

    This method aborts a job on Airflow via its API

    Arguments:
        dag_run_id (str): payload of the request sent to the API

    """
    secrets = get_kv_secret_list(VAULT_CLIENT, cnf.APP_CONFIG.API_SECRET_PATH, cnf.APP_CONFIG.SECRET_MOUNT)

    requests.put(f"{secrets[f'airflow_connector_url_{cnf.ENV_STATE}']}/dag/run/{dag_run_id}/abort",
                 headers={
                     "Authorization": get_bearer_token(KC_CLIENT, secrets['api_kc_user'], secrets['api_kc_password']),
                     "Content-Type": "application/json"
                 })
