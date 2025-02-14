import json
import traceback

from fastapi import APIRouter, Security
from geoville_order_management_module.service_orders import aws_eventbridge_submit_airflow_job, generate_order_id

from src.config import cnf
from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.init.init_variables import VAULT_CLIENT
from src.lib.oauth2 import get_auth
from src.lib.spatial_operations import calculate_aoi_size
from src.postgres_connector.postgres_connector import PostgresConnector
from src.v1.models.model_products import RequestProduct, ResponseAsyncProductResult

########################################################################################################################
# Router object definition
########################################################################################################################

router_get_products = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_get_products.post('/products',
                          response_model=ResponseAsyncProductResult,
                          status_code=201,
                          summary="POST definition for requesting the get-products workflow",
                          description="""
This method defines the handler of the POST request for starting off the get-products processing chain within the GEMS 
service architecture. It is an asynchronous call and thus, it does not return the requested data immediately but 
generates an order ID. After the request has been submitted successfully, a message to a RabbitMQ queue will be send. A 
listener in the backend triggers the further procedure, starting with the job scheduling of the order. The final result 
will be stored in a database in form of a link and can be retrieved via the browser. To access the service it is 
necessary to generate a valid Bearer token with sufficient access rights, otherwise the request will return a HTTP 
status code 401 or 403. In case of those errors, please contact the GeoVille service team for any support."""
                          )
def products(payload: RequestProduct, user_info=Security(get_auth, scopes=["admin user"])):
    calculate_aoi_size(payload.aoi)

    try:
        service_dag_name = "get_product"
        order_id = generate_order_id(service_dag_name, user_info['sub'], payload.dict())

        try:
            aws_eventbridge_submit_airflow_job(service_dag_name, order_id, payload.dict(), VAULT_CLIENT,
                                               cnf.APP_CONFIG.SECRET_MOUNT, cnf.APP_CONFIG.SECRET_PATH,
                                               runs_on_aws=True, is_test=payload.test)
        except RuntimeError:
            PostgresConnector(payload.test).insert_failed_order_states((user_info['sub'], service_dag_name,
                                                                        user_info['email'], order_id,
                                                                        "RECEIVED", json.dumps(payload.dict())))
        else:
            PostgresConnector(payload.test).insert_order_states((user_info['sub'], service_dag_name, user_info['email'],
                                                                 order_id, "RECEIVED", json.dumps(payload.dict())))

    except AttributeError as err:
        logger.error(f'write_qa_qc_result: Unexpected error occurred {err} \n {traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the database server')

    except Exception as err:
        logger.error(f'write_qa_qc_result: Unexpected error occurred {err} \n {traceback.format_exc()}')
        raise InternalServerError(f'Unexpected error occurred')

    else:
        return {'message': 'Your order has been successfully submitted',
                'links': {
                    'href': f'services/orders/{order_id}/status',
                    'rel': 'services',
                    'type': 'GET'
                }
                }
