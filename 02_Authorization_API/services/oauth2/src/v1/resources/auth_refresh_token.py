from fastapi import APIRouter
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakPostError

from src.error_handlers.class_http_error_400 import BadRequestError
from src.error_handlers.class_http_error_401 import UnauthorizedError
from src.init.init_variables import KC_CLIENT
from src.v1.models.model_auth import RequestRefreshToken, ResponseToken

########################################################################################################################
# Router object definition
########################################################################################################################

router_refresh_token = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_refresh_token.post('/oauth2/refresh_token',
                           response_model=ResponseToken,
                           status_code=200,
                           summary="Returns a refresh token for API usage",
                           description="Refresh token")
def refresh_token(payload: RequestRefreshToken):

    try:
        return KC_CLIENT.kc_connector.refresh_token(payload.refresh_token)

    except KeycloakAuthenticationError:
        raise UnauthorizedError('Invalid user credentials')

    except KeycloakPostError:
        raise BadRequestError('Invalid user request')
