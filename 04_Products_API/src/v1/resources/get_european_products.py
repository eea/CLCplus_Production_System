import traceback
from datetime import datetime

from fastapi import APIRouter, Security
from geoville_aws_module import AWSClient
from geoville_order_management_module.service_orders import aws_eventbridge_submit_order, generate_order_id

from src.config import cnf
from src.error_handlers.class_http_error_400 import BadRequestError
from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.init.init_variables import EVENT_BUS, VAULT_CLIENT
from src.lib.oauth2 import get_auth
from src.v1.models.model_products import RequestEuropeanProduct, ResponseProductResult

########################################################################################################################
# Router object definition
########################################################################################################################

router_european_products = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_european_products.post('/european-products',
                               response_model=ResponseProductResult,
                               status_code=201,
                               summary="POST definition for requesting the specified product for entire Europe",
                               description="""
This method defines the handler of the POST request for getting the specified product for entire Europe. It is a 
synchronous call and thus, it returns the requested data immediately. To access the service it is necessary to generate 
a valid Bearer token with sufficient access rights, otherwise the request will return a HTTP status code 401 or 403. In 
case of those errors, please contact the GeoVille service team for any support."""
                               )
def european_products(payload: RequestEuropeanProduct, user_info=Security(get_auth, scopes=["admin user"])):
    if payload.product != "Raster":
        logger.error(f'get_european_products: Wrong product choice')
        raise BadRequestError('Only product type "Raster" is allowed.')

    try:
        service_dag_name = "clc_backbone_european_products"

        aws = AWSClient(VAULT_CLIENT)
        url = aws.s3_generated_presigned_url("gv-clc-backbone-service-result-bucket",
                                             "europe/CLMS_CLCplus_RASTER_2018_010m_eu_03035_V1_1.tif")

        message = {
            "order_id": generate_order_id(service_dag_name, user_info['sub'], payload.dict()),
            "user_id": user_info['sub'],
            "service_dag_name": service_dag_name,
            "status": "SUCCESS",
            "result": url,
            "order_json": payload.dict(),
            "order_started": str(datetime.now()),
            "order_finished": str(datetime.now())
        }

        message_detail = "GEMS-Service-Order-Triggered"
        aws_eventbridge_submit_order(VAULT_CLIENT, EVENT_BUS, message, message_detail, cnf.APP_CONFIG.EVENT_SOURCE,
                                     runs_on_aws=True, is_test=payload.test)

    except AttributeError as err:
        logger.error(f'clc_backbone_european_products: Unexpected error occurred {err} \n {traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the database server')

    except Exception as err:
        logger.error(f'clc_backbone_european_products: Unexpected error occurred {err} \n {traceback.format_exc()}')
        raise InternalServerError(f'Unexpected error occurred')

    else:
        return {'result': url}
