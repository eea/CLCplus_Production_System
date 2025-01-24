from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from geoville_keycloak_module_utils.keycloak_utils import get_access_token
from keycloak.exceptions import KeycloakAuthenticationError

from src.error_handlers.class_http_error_401 import UnauthorizedError
from src.init.init_variables import KC_CLIENT
from src.v1.models.model_auth import ResponseToken

########################################################################################################################
# Router object definition
########################################################################################################################

router_oauth_token = APIRouter()


########################################################################################################################
# Endpoint definition
########################################################################################################################

@router_oauth_token.post('/oauth2/token',
                         response_model=ResponseToken,
                         status_code=200,
                         summary="Returns an access token for API usage",
                         description="Access token retrieval")
def oauth_token(form_data: OAuth2PasswordRequestForm = Depends()):

    try:
        return get_access_token(KC_CLIENT, form_data.username, form_data.password)

    except KeycloakAuthenticationError:
        raise UnauthorizedError('Invalid User credentials')
