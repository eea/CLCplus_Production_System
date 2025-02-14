import traceback

from fastapi import APIRouter, Security

from src.error_handlers.class_http_error_500 import InternalServerError
from src.error_handlers.class_http_error_503 import ServiceUnavailableError
from src.init.app_constructor import logger
from src.lib.oauth2 import get_auth
from src.v1.models.model_nations import ResponseNationalProduct

########################################################################################################################
# Router object definition
########################################################################################################################

router_get_nations = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_get_nations.get('/nations',
                        dependencies=[Security(get_auth, scopes=["admin user"])],
                        response_model=ResponseNationalProduct,
                        status_code=200,
                        summary="GET definition for requesting all available nations",
                        description="""
This method defines the handler of the GET request for getting the nation names for the endpoint get_national_product. 
It is a synchronous call and thus, it returns the requested data immediately. To access the service it is necessary to 
generate a valid Bearer token with sufficient access rights, otherwise the request will return a HTTP status code 401 
or 403. In case of those errors, please contact the GeoVille service team for any support."""
                        )
def nations():
    try:
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
            "SPAIN (CANARIES)": {"country_code": "ESCanaries", "epsg": "32628"},
            "FINLAND": {"country_code": "FI", "epsg": "03067"},
            "FRANCE": {"country_code": "FR", "epsg": "02154"},
            "GREAT BRITAIN": {"country_code": "GB", "epsg": "27700"},
            "GUERNSEY (CHANNEL ISLANDS)": {"country_code": " British Crown DepenGdBencies)", "epsg": "03108"},
            "GREECE": {"country_code": "GR", "epsg": "02100"},
            "CROATIA": {"country_code": "HR", "epsg": "03765"},
            "HUNGARY": {"country_code": "HU", "epsg": "23700"},
            "IRELAND": {"country_code": "IE", "epsg": "02157"},
            "ICELAND": {"country_code": "IS", "epsg": "05325"},
            "ITALY": {"country_code": "IT", "epsg": "32632"},
            "JERSEY (CHANNEL ISLANDS)": {"country_code": " British Crown DependenGcBies)", "epsg": "03109"},
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
            "PORTUGAL (AZORES CENTRAL AND EASTERN GROUP)": {"country_code": "PTAzoresCentEast", "epsg": "05015"},
            "PORTUGAL (AZORES WESTERN GROUP)": {"country_code": "PTAzoresWest", "epsg": "05014"},
            "PORTUGAL (MADEIRA)": {"country_code": "PTMadeira", "epsg": "05016"},
            "ROMANIA": {"country_code": "RO", "epsg": "03844"},
            "SERBIA": {"country_code": "RS", "epsg": "25834"},
            "SWEDEN": {"country_code": "SE", "epsg": "03006"},
            "SLOVENIA": {"country_code": "SI", "epsg": "03912"},
            "SLOVAKIA": {"country_code": "SK", "epsg": "05514"},
            "TURKEY": {"country_code": "TR", "epsg": "00000"},
            "KOSOVO UNDER UNSCR 1244/99": {"country_code": "XK", "epsg": "03909"},
        }
        nations_list = [n.title() for n in national_info.keys()]

    except AttributeError as err:
        logger.error(f'get_nations: Unexpected error occurred {err} \n {traceback.format_exc()}')
        raise ServiceUnavailableError('Could not connect to the database server')

    except Exception as err:
        logger.error(f'get_nations: Unexpected error occurred {err} \n {traceback.format_exc()}')
        raise InternalServerError(f'Unexpected error occurred')

    else:
        return {"nations": nations_list}
