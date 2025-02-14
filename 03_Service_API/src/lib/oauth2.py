from fastapi import Security
from fastapi.security import SecurityScopes
from geoville_keycloak_module_utils.keycloak_utils import validate_token
from jose.exceptions import ExpiredSignatureError
from keycloak.exceptions import KeycloakInvalidTokenError

from src.error_handlers.class_http_error_401 import UnauthorizedError
from src.error_handlers.class_http_error_403 import ForbiddenError
from src.init.app_constructor import oauth2_scheme
from src.init.init_variables import KC_CLIENT


########################################################################################################################
# Validates the Keycloak scopes with the ones defined
########################################################################################################################

def get_auth(scopes: SecurityScopes, token: str = Security(oauth2_scheme)) -> dict:
    """ Validates the generated token against the Keycloak instance

    This method proves in a first step the validity of the access token by verifying it with Keycloak public key. In a
    second step, it compares the scopes from the REST endpoint and the token returned by Keycloak. If they match, the
    user is granted to access the endpoint.

    Arguments:
        scopes (SecurityScopes): Scopes coming from the REST endpoint through dependency injection
        token (str): Access token returned from token URL if the user is authenticated

    Returns:
        access_token (dict): Access token dictionary with all required privileges

    """
    try:
        token = validate_token(scopes, token, KC_CLIENT)
        if token:
            return token
        raise ForbiddenError('Permission denied')

    except ExpiredSignatureError:
        raise UnauthorizedError('Token signature expired')

    except KeycloakInvalidTokenError:
        raise UnauthorizedError('Invalid authentication credentials')
