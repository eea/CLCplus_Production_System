import traceback
from http import HTTPStatus

from fastapi import APIRouter, Path, Query, Response, Security
from geoville_order_management_module.service_orders import aws_eventbridge_abort_airflow_job

from src.config import cnf
from src.error_handlers.class_http_error_400 import BadRequestError
from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.init.init_variables import VAULT_CLIENT
from src.lib.oauth2 import get_auth
from src.postgres_connector.postgres_connector import PostgresConnector

########################################################################################################################
# Router object definition
########################################################################################################################

router_order_abort = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_order_abort.put('/orders/{order_id}/abort',
                        status_code=204,
                        summary='PUT definition for aborting an order',
                        description="""
<b>Description:</b>
<p style="text-align: justify">This method defines...</p>

<br><b>Request headers:</b>
<ul>
<li><p><i>Authorization: Bearer token in the format "Bearer XXXX"</i></p></li>
</ul>

<br><b>Request payload:</b>
<ul>
<li><p><i>.... (...): ...</i></p></li>
</ul>

<br><b>Result:</b>
<p style="text-align: justify">After the request was successfully received by the GEMS API, ...</p>
""")
def abort_service_order(user_info=Security(get_auth, scopes=["admin user"]),
                        order_id: str = Path(..., description='Order ID to be queried'),
                        test: bool = Query(default=False, include_in_schema=False)):
    try:
        order_status = PostgresConnector(test).get_order_status((order_id,), user_info['sub'])

        if order_status['status'] == 'SUCCESS':
            raise BadRequestError('Order already successfully processed')
        elif order_status['status'] == 'FAILED':
            raise BadRequestError('Order has already been cancelled')

        try:
            aws_eventbridge_abort_airflow_job(VAULT_CLIENT, cnf.APP_CONFIG.SECRET_MOUNT, cnf.APP_CONFIG.SECRET_PATH,
                                              order_id, order_status['service_name'], runs_on_aws=True, is_test=test)
        except RuntimeError:
            PostgresConnector(test).insert_failed_abortion_orders((user_info['sub'], order_status['service_name'],
                                                                   order_id, "FAILED"))

        PostgresConnector(test).update_order_state((order_id,))

    except AttributeError as err:
        logger.error(f'abort_order: {err}\n{traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the backend server')

    except Exception as err:
        logger.error(f'abort_order: {err}\n{traceback.format_exc()}')
        raise InternalServerError('Unexpected application error')

    else:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
