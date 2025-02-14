import traceback

from fastapi import APIRouter, Path, Query, Security

from src.error_handlers.class_http_error_401 import UnauthorizedError
from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.lib.oauth2 import get_auth
from src.postgres_connector.postgres_connector import PostgresConnector
from src.v1.models.model_orders import ResponseResultStatus

########################################################################################################################
# Router object definition
########################################################################################################################

router_order_status = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_order_status.get("/orders/{order_id}/status",
                         response_model=ResponseResultStatus,
                         status_code=200,
                         summary="GET definition for retrieving the result status of a submitted order",
                         description="")
def order_status(user_info=Security(get_auth, scopes=["admin user"]),
                 order_id: str = Path(..., description="Order ID to be queried"),
                 test: bool = Query(default=False, include_in_schema=False)):
    try:
        return PostgresConnector(test).get_order_status((order_id,), user_info['sub'])

    except AttributeError as err:
        logger.error(f'order_status: {err}\n{traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the backend server')

    except UnauthorizedError as err:
        logger.error(f'order_status: {err}\n{traceback.format_exc()}')
        raise UnauthorizedError('The user is not authorized to request this resource')

    except Exception as err:
        logger.error(f'order_status: {err}\n{traceback.format_exc()}')
        raise InternalServerError('Unexpected application error')
