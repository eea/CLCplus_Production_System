import traceback
from datetime import datetime

from fastapi import APIRouter, Security
from geoville_aws_module import AWSClient
from geoville_order_management_module.service_orders import aws_eventbridge_submit_order, generate_order_id

from src.config import cnf
from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.init.init_variables import EVENT_BUS, VAULT_CLIENT
from src.lib.oauth2 import get_auth
from src.v1.models.model_products import RequestNationalProduct, ResponseProductResult

########################################################################################################################
# Router object definition
########################################################################################################################

router_national_products = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_national_products.post('/national-products',
                               response_model=ResponseProductResult,
                               status_code=201,
                               summary="POST definition for requesting the specified product for a nation of choice",
                               description="This method defines the handler of the POST request for getting the "
                                           "specified product for a nation of choice. It is a synchronous call and "
                                           "thus, it returns the requested data immediately. To access the service it "
                                           "is necessary to generate a valid Bearer token with sufficient access "
                                           "rights, otherwise the request will return a HTTP status code 401 or 403. "
                                           "In case of those errors, please contact the GeoVille service team for any "
                                           "support.")
def national_products(payload: RequestNationalProduct, user_info=Security(get_auth, scopes=["admin user"])):

    national_info = {
        "ALBANIA": {"country_code": "AL", "epsg": "02462"},
        "AUSTRIA": {"country_code": "AT", "epsg": "31287"},
        "BOSNIA AND HERZEGOVINA": {"country_code": "BA", "epsg": "03908"},
        "BELGIUM": {"country_code": "BE", "epsg": "03812"},
        "BULGARIA": {"country_code": "BG", "epsg": "32635"},
        "SWITZERLAND": {"country_code": "CH", "epsg": "02056"},
        "CYPRUS": {"country_code": "CY", "epsg": "32636"},
        "CZECH REPUBLIC": {"country_code": "CZ", "epsg": "05514"},
        "GERMANY": {"country_code": "DE", "epsg": "32632"},
        "DENMARK": {"country_code": "DK", "epsg": "25832"},
        "ESTONIA": {"country_code": "EE", "epsg": "03301"},
        "SPAIN": {"country_code": "ES", "epsg": "25830"},
        "SPAIN (CANARIES)": {"country_code": "ES", "epsg": "32628"},
        "FINLAND": {"country_code": "FI", "epsg": "03067"},
        "FRANCE": {"country_code": "FR", "epsg": "02154"},
        "GREAT BRITAIN": {"country_code": "GB", "epsg": "27700"},
        "GUERNSEY (CHANNEL ISLANDS)": {"country_code": "GB", "epsg": "03108"},
        "GREECE": {"country_code": "GR", "epsg": "02100"},
        "CROATIA": {"country_code": "HR", "epsg": "03765"},
        "HUNGARY": {"country_code": "HU", "epsg": "23700"},
        "IRELAND": {"country_code": "IE", "epsg": "02157"},
        "ICELAND": {"country_code": "IS", "epsg": "05325"},
        "ITALY": {"country_code": "IT", "epsg": "32632"},
        "JERSEY (CHANNEL ISLANDS)": {"country_code": "GB", "epsg": "03109"},
        "LIECHTENSTEIN": {"country_code": "LI", "epsg": "02056"},
        "LITHUANIA": {"country_code": "LT", "epsg": "03346"},
        "LUXEMBOURG": {"country_code": "LU", "epsg": "02169"},
        "LATVIA": {"country_code": "LV", "epsg": "03059"},
        "MONTENEGRO": {"country_code": "ME", "epsg": "25834"},
        "FYR OF MACEDONIA": {"country_code": "MK", "epsg": "06204"},
        "MALTA": {"country_code": "MT", "epsg": "23033"},
        "NORTHERN IRELAND": {"country_code": "NI", "epsg": "29903"},
        "NETHERLANDS": {"country_code": "NL", "epsg": "28992"},
        "NORWAY": {"country_code": "NO", "epsg": "25833"},
        "POLAND": {"country_code": "PL", "epsg": "02180"},
        "PORTUGAL": {"country_code": "PT", "epsg": "03763"},
        "PORTUGAL (AZORES CENTRAL AND EASTERN GROUP)": {"country_code": "PT", "epsg": "05015"},
        "PORTUGAL (AZORES WESTERN GROUP)": {"country_code": "PT", "epsg": "05014"},
        "PORTUGAL (MADEIRA)": {"country_code": "PT", "epsg": "05016"},
        "ROMANIA": {"country_code": "RO", "epsg": "03844"},
        "SERBIA": {"country_code": "RS", "epsg": "25834"},
        "SWEDEN": {"country_code": "SE", "epsg": "03006"},
        "SLOVENIA": {"country_code": "SI", "epsg": "03912"},
        "SLOVAKIA": {"country_code": "SK", "epsg": "05514"},
        "TURKEY": {"country_code": "TR", "epsg": "00000"},
        "KOSOVO UNDER UNSCR 1244/99": {"country_code": "KS", "epsg": "03909"},
    }

    try:
        service_dag_name = "clc_backbone_national_product"

        country, epsg = national_info[payload.nation.upper()].values()
        if payload.product == "Raster":
            bucket_path = f"national_products/Raster/CLMS_CLCplus_RASTER_2018_010m_{country.lower()}_{epsg}_V1_1.zip"
        else:
            bucket_path = f"national_products/Vector/CLMS_CLCplus_VECTOR_2018_{country.upper()}_{epsg}_V1_1.zip"

        aws = AWSClient(VAULT_CLIENT)
        url = aws.s3_generated_presigned_url("gv-clc-backbone-service-result-bucket", bucket_path)

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
        logger.error(f'clc_backbone_national_product: Unexpected error occurred {err} \n {traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the database server')

    except Exception as err:
        logger.error(f'clc_backbone_national_product: Unexpected error occurred {err} \n {traceback.format_exc()}')
        raise InternalServerError(f'Unexpected error occurred')

    else:
        return {"result": url}
