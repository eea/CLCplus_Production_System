import traceback

from fastapi import APIRouter, Security

from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.lib.airflow_connector import create_order
from src.lib.oauth2 import get_auth
from src.v1.models.model_gaf_services import RequestPrepareSamplesTesting
from src.v1.models.model_generic_service_response import ResponseServices

########################################################################################################################
# Router object definition
########################################################################################################################

router_gaf_prepare_samples_testing = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_gaf_prepare_samples_testing.post('/gaf-prepare-samples-testing',
                                         response_model=ResponseServices,
                                         status_code=201,
                                         summary='POST definition for triggering the prepare samples testing workflow '
                                                 'for GAF',
                                         description="""
<p style="text-align: justify">This method defines the handler of the POST request for starting the VLCC apply model 
service for GAF processing chain within the GEMS service architecture. It is an asynchronous call and thus it does
not return the requested data immediately but generates an order ID. With this ID the progress of the order 
can be monitored and in case of successful completion, the result can be accessed.<br>
To access the service it is necessary to generate a valid Bearer token with sufficient access rights, 
otherwise the request will return a HTTP status code 401 or 403. In case of those errors, please contact the GeoVille 
service team for any support.
""")
def gaf_prepare_samples_testing(payload: RequestPrepareSamplesTesting,
                                user_info=Security(get_auth, scopes=["admin gaf"])):
    service_dag_name = 'prepare_samples_dag_testing'

    try:
        if payload.test:
            order_id = '67c76c7a-ee32-4864-8e00-fd27a0282e6e:20221019T160731051934'

        else:
            api_response = create_order(user_info['sub'], service_dag_name, payload.dict())

            if api_response.status_code == 201:
                order_id = api_response.json()['dag_run_id']
            else:
                raise RuntimeError

    except SystemError as err:
        logger.error(f'prepare_samples_testing: {err}\n{traceback.format_exc()}')
        raise ServiceUnavailableError('Communication with the backend server failed')

    except AttributeError as err:
        logger.error(f'prepare_samples_testing: {err}\n{traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the backend server')

    except Exception as err:
        logger.error(f'prepare_samples_testing: {err}\n{traceback.format_exc()}')
        raise InternalServerError('Unexpected application error')

    else:
        return {
            'message': 'Your order has been successfully received',
            'links': {
                'href': f'/orders/status/{order_id}',
                'rel': 'orders',
                'type': 'GET'
            }
        }
