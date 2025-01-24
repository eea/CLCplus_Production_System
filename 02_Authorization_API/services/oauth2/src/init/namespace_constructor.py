from fastapi import APIRouter

from src.v1.models.model_http_error_400 import HTTPError400
from src.v1.models.model_http_error_401 import HTTPError401
from src.v1.models.model_http_error_403 import HTTPError403
from src.v1.models.model_http_error_500 import HTTPError500
from src.v1.models.model_http_error_503 import HTTPError503

########################################################################################################################
# Constant definitions
########################################################################################################################

const_400_desc = "Invalid user request"
const_401_desc = "Authorization error"
const_403_desc = "Forbidden"
const_500_desc = "Internal Server Error"
const_503_desc = "Service Unavailable"

########################################################################################################################
# Definition of the various metadata tags for the OpenAPI UI for the API
########################################################################################################################

tags_auth = [
    {
        "name": "auth",
        "description": "Authentication related operations",
    }
]

tags_health = [
    {
        "name": "health",
        "description": "Operations to retrieve the health status of the API",
    }
]

########################################################################################################################
# Definition of the various routers for the OpenAPI UI of the API
########################################################################################################################

router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        400: {"model": HTTPError400, "description": const_400_desc},
        401: {"model": HTTPError401, "description": const_401_desc},
        403: {"model": HTTPError403, "description": const_403_desc},
        500: {"model": HTTPError500, "description": const_500_desc},
        503: {"model": HTTPError503, "description": const_503_desc}
    }
)

router_health = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={
        400: {"model": HTTPError400, "description": const_400_desc},
        401: {"model": HTTPError401, "description": const_401_desc},
        403: {"model": HTTPError403, "description": const_403_desc},
        500: {"model": HTTPError500, "description": const_500_desc},
        503: {"model": HTTPError503, "description": const_503_desc}
    }
)
