from fastapi.security import SecurityScopes

from geoville_keycloak_module.keycloak_client import KeycloakClient


########################################################################################################################
# Validates the Keycloak scopes with the ones defined
########################################################################################################################

def validate_token(scopes: SecurityScopes, token: str, keycloak_client: KeycloakClient) -> dict:
    """ Validates and checks an input token against FastAPI's security scopes

    This method checks in a first step a Keycloak token for validity. In a second step it validates

    Arguments:
        scopes (SecurityScopes): unique identifier of a client
        token (str): access token received by an HTTP request
        keycloak_client (KeycloakClient):

    Returns:
        (dict): access token

    """

    value = keycloak_client.kc_connector.decode_token(
        token,
        key=keycloak_client.kc_pub_key,
        options={
            "verify_signature": True,
            "verify_aud": False,
            "exp": True
        }
    )

    keycloak_scope_list = value['scope'].split(" ")
    endpoint_scope_list = scopes.scopes[0].split(" ")

    for scope in keycloak_scope_list:
        if scope in endpoint_scope_list:
            return value


########################################################################################################################
# Generates a Keycloak access token for the defined user
########################################################################################################################

def get_access_token(keycloak_client: KeycloakClient, user: str, password: str) -> dict:
    """ Generates a Keycloak access token

    This method generates a Keycloak access token for the specified user and password combination under the
    configured Keycloak client.

    Arguments:
        keycloak_client (KeycloakClient): Keycloak client object
        user (str): user in the realm
        password (str): user password for the realm

    Returns:
        (dict): access token dictionary

    """

    if keycloak_client.kc_access_token is None or not keycloak_client.validate_access_token_expiration():
        keycloak_client.kc_access_token = keycloak_client.kc_connector.token(user, password)

    return keycloak_client.kc_access_token


########################################################################################################################
# Generates a Keycloak access token for the defined user
########################################################################################################################

def get_bearer_token(keycloak_client: KeycloakClient, user: str, password: str) -> str:
    """ Generates a Keycloak bearer token

    This method generates a Keycloak bearer token for the specified user and password combination under the
    configured Keycloak client.

    Arguments:
        keycloak_client (KeycloakClient): Keycloak client object
        user (str): user in the realm
        password (str): user password for the realm

    Returns:
        (str): bearer token

    """

    if keycloak_client.kc_bearer_token is None or not keycloak_client.validate_bearer_token_expiration():
        keycloak_client.kc_bearer_token = keycloak_client.kc_connector.token(user, password)['access_token']

    return f"Bearer {keycloak_client.kc_bearer_token}"
