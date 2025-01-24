import traceback
from http import HTTPStatus

from fastapi import APIRouter, Path, Query, Security, Response

from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.lib.airflow_connector import abort_order
from src.lib.oauth2 import get_auth
from src.lib.order_helper import check_permissions

########################################################################################################################
# Router object definition
########################################################################################################################

router_order_abort = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_order_abort.put('/{order_id}/abort',
                        dependencies=[Security(get_auth, scopes=["admin geoville gaf"])],
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
def abort_service_order(user_info=Security(get_auth, scopes=["admin geoville gaf"]),
                        order_id: str = Path(..., description='Order ID to be queried'),
                        test: bool = Query(default=False, include_in_schema=False)):

    if test:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    check_permissions(user_info, order_id)

    try:
        abort_order(order_id)
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    except SystemError as err:
        logger.error(f'test-service: {err}\n{traceback.format_exc()}')
        raise ServiceUnavailableError('Communication with the backend server failed')

    except AttributeError as err:
        logger.error(f'abort_order: {err}\n{traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the backend server')

    except Exception as err:
        logger.error(f'abort_order: {err}\n{traceback.format_exc()}')
        raise InternalServerError('Unexpected application error')
