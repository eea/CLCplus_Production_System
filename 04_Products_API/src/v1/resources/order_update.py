import traceback
from http import HTTPStatus

from fastapi import APIRouter, Response, Security
from geoville_order_management_module.service_orders import aws_eventbridge_submit_order

from src.config import cnf
from src.error_handlers.class_http_error_401 import UnauthorizedError
from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.init.init_variables import EVENT_BUS, VAULT_CLIENT
from src.lib.oauth2 import get_auth
from src.postgres_connector.postgres_connector import PostgresConnector
from src.v1.models.model_orders import RequestOrderUpdate

########################################################################################################################
# Router object definition
########################################################################################################################

router_order_update = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_order_update.put("/orders",
                         dependencies=[Security(get_auth, scopes=["admin"])],
                         status_code=204,
                         summary="PUT definition for updating the status of an order",
                         description="")
def order_status(payload: RequestOrderUpdate):
    try:
        order = PostgresConnector(payload.test).update_result_order_state((payload.status,
                                                                           payload.result, payload.order_id))

        if 'send_mail' in order['order_json'] and order['order_json']['send_mail']:
            message_detail = "GEMS-Notification-Triggered"
            aws_eventbridge_submit_order(VAULT_CLIENT, EVENT_BUS, order, message_detail, cnf.APP_CONFIG.EVENT_SOURCE,
                                         runs_on_aws=True, is_test=payload.test)

        message_detail = "GEMS-Service-Order-Triggered"
        aws_eventbridge_submit_order(VAULT_CLIENT, EVENT_BUS, order, message_detail, cnf.APP_CONFIG.EVENT_SOURCE,
                                     runs_on_aws=True, is_test=payload.test)

    except AttributeError as err:
        logger.error(f'order_status: {err}\n{traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the backend server')

    except UnauthorizedError as err:
        logger.error(f'order_status: {err}\n{traceback.format_exc()}')
        raise UnauthorizedError('The user is not authorized to request this resource')

    except Exception as err:
        logger.error(f'order_status: {err}\n{traceback.format_exc()}')
        raise InternalServerError('Unexpected application error')

    else:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
