from urllib.parse import urlparse
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakInvalidTokenError


########################################################################################################################
# Keycloak module class definition
########################################################################################################################

class KeycloakClient:
    """ Class definition

    The class connecting to a specified Keycloak realm.

    """

    def __init__(self, url: str, realm: str, client_id: str, client_secret: str):
        """ Constructor method

        This method definition is the constructor method of the class and takes four required input parameters.

        Arguments:
            url (str): Keycloak server URL
            realm (str): Keycloak realm
            client_id (str): Keycloak realm client ID
            client_secret (str): Keycloak realm client secret

        """

        path = get_url_path(url)
        if path:
            url = url + path

        self.kc_connector = KeycloakOpenID(
            server_url=url,
            client_id=client_id,
            realm_name=realm,
            client_secret_key=client_secret,
            verify=True
        )

        self.kc_pub_key = self.__get_public_key()
        self.kc_access_token = None
        self.kc_bearer_token = None

    def __get_public_key(self) -> str:
        """ Retrieves the public key for the given Keycloak realm

        This method returns the public key for the specified Keycloak realm

        Returns:
            (str): Keycloak public key

        """

        return (
            "-----BEGIN PUBLIC KEY-----\n"
            f"{self.kc_connector.public_key()}"
            "\n-----END PUBLIC KEY-----"
        )

    def validate_access_token_expiration(self) -> bool:
        """ Validates a Keycloak access token

        This method validates a Keycloak access token for a previously generated access token.

        Returns:
            (bool): True or False

        """

        try:
            self.kc_connector.decode_token(
                self.kc_access_token['access_token'],
                key=self.kc_pub_key,
                options={
                    "verify_signature": True,
                    "verify_aud": False,
                    "exp": True
                }
            )

        except KeycloakInvalidTokenError:
            return False
        else:
            return True

    def validate_bearer_token_expiration(self) -> bool:
        """ Validates a Keycloak bearer token

        This method validates a Keycloak bearer token for a previously generated bearer token.

        Returns:
            (bool): True or False

        """

        try:
            self.kc_connector.decode_token(
                self.kc_bearer_token,
                key=self.kc_pub_key,
                options={
                    "verify_signature": True,
                    "verify_aud": False,
                    "exp": True
                }
            )

        except KeycloakInvalidTokenError:
            return False
        else:
            return True


def get_url_path(url):
    parsed_url = urlparse(url)
    return parsed_url.path if parsed_url.path else None