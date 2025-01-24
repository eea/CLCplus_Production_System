import traceback

from fastapi import APIRouter, Path, Query, Security

from src.error_handlers.class_http_error_400 import BadRequestError
from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.lib.airflow_connector import get_order_status
from src.lib.oauth2 import get_auth
from src.lib.order_helper import check_permissions, get_service_result_value
from src.v1.models.model_orders import ResponseResultStatus

########################################################################################################################
# Router object definition
########################################################################################################################

router_order_status = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_order_status.get("/{order_id}/status",
                         dependencies=[Security(get_auth, scopes=["admin geoville gaf"])],
                         response_model=ResponseResultStatus,
                         status_code=200,
                         summary="GET definition for retrieving the result status of a submitted order",
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
def order_status(user_info=Security(get_auth, scopes=["admin geoville gaf"]),
                 order_id: str = Path(..., description="Order ID to be queried"),
                 test: bool = Query(default=False, include_in_schema=False)):
    if test:
        return {
            "order_id": order_id,
            "status": "test-status"
        }

    check_permissions(user_info, order_id)

    expiration_in_days = None
    try:
        order_status_response = get_order_status(order_id)
        if "dag_run_status" in order_status_response:
            status = order_status_response['dag_run_status']
        else:
            status = None
        expiration_in_days = None
        if "dag_name" in order_status_response:
            result = get_service_result_value(order_status_response['dag_name'], order_id, status)
        if status == "success":
            expiration_in_days = 30

    except SystemError as err:
        logger.error(f'test-service: {err}\n{traceback.format_exc()}')
        raise ServiceUnavailableError('Communication with the backend server failed')

    except AttributeError as err:
        logger.error(f'order_status: {err}\n{traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the backend server')

    except Exception as err:
        logger.error(f'order_status: {err}\n{traceback.format_exc()}')
        raise InternalServerError('Unexpected application error')

    if status is None:
        raise BadRequestError('No order metadata could be retrieved. Wrong order ID?')

    return {
        "order_id": order_id,
        "status": status,
        "result": result,
        "expiration_in_days": expiration_in_days
    }
