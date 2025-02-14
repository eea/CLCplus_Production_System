import hvac
from hvac import exceptions
from hvac.api.auth_methods.aws import AWS_DEFAULT_MOUNT_POINT
from hvac.api.auth_methods.userpass import DEFAULT_MOUNT_POINT as USER_PASS_DEFAULT
from hvac.constants.approle import DEFAULT_MOUNT_POINT as APP_ROLE_DEFAULT


########################################################################################################################
# Vault client class definition
########################################################################################################################

class VaultClient:
    """ Class definition

    The class for authenticating with Hashicorp Vault.

    """

    def __init__(self, vault_url: str):
        """ Constructor method

        This method definition is the constructor method of the class and takes two required input parameters.

        Arguments:
            vault_url (str): Vault server URL

        """
        self.__vault_url = vault_url
        self.login_method = None
        self.client = None

    def token_login(self, token: str) -> None:
        """ Hashicorp Vault token login mechanism

        This method authenticates with the Hashicorp Vault server via an access token.

        Arguments:
            token (str): Vault access token

        """

        hv_client = hvac.Client(url=self.__vault_url)
        hv_client.token = token

        if hv_client.is_authenticated():
            self.login_method = lambda: token
            self.client = hv_client
        else:
            raise exceptions.Unauthorized(message='Client is not authorized via the token login method')

    def app_role_login(self, role_id: str, secret_id: str, mount_point: str = APP_ROLE_DEFAULT) -> None:
        """ Hashicorp Vault app role login mechanism

        This method authenticates with the Hashicorp Vault server via an app role

        Arguments:
            role_id (str): Role ID belonging to the app role login mechanism
            secret_id (str): Secret ID belonging to the app role login mechanism
            mount_point (str): Optional parameter to specify the mount point of the app role login

        """

        hv_client = hvac.Client(url=self.__vault_url)
        hv_client.auth.approle.login(role_id=role_id, secret_id=secret_id, mount_point=mount_point)

        if hv_client.is_authenticated():
            self.login_method = lambda: hv_client.auth.approle.login(role_id=role_id, secret_id=secret_id,
                                                                     mount_point=mount_point)
            self.client = hv_client

        else:
            raise exceptions.Unauthorized(message='Client is not authorized via app role login method')

    def user_pass_login(self, user_name: str, password: str, mount_point: str = USER_PASS_DEFAULT) -> None:
        """ Hashicorp Vault user password login mechanism

        This method authenticates with the Hashicorp Vault server via a user and password combination

        Arguments:
            user_name (str): Vault user name
            password (str): Vault password
            mount_point (str): Optional parameter to specify the mount point of the app role login

        """

        hv_client = hvac.Client(url=self.__vault_url)
        hv_client.auth.userpass.login(user_name, password, mount_point=mount_point)

        if hv_client.is_authenticated():
            self.login_method = lambda: hv_client.auth.userpass.login(user_name, password, mount_point=mount_point)
            self.client = hv_client

        else:
            raise exceptions.Unauthorized(message='Client is not authorized via user/pass login method')

    def aws_iam_login(self, access_key_id: str, secret_access_key: str, session_token: str = None, role: str = None,
                      mount_point: str = AWS_DEFAULT_MOUNT_POINT) -> None:
        """ Hashicorp Vault AWS auth backend login

        This method authenticates with the Hashicorp Vault server via the AWS authentication backend setup in Vault.
        This authentication method can be used for AWS ECS or AWS Lambda functions.

        Arguments:
            access_key_id (str): AWS access key ID
            secret_access_key (str): AWS secret access key
            session_token (str): Optional parameter to specify the AWS session token
            role (str): Optional parameter to specify the Vault AWS backend role
            mount_point (str): Optional parameter to specify the mount point of the AWS auth backend

        """

        hv_client = hvac.Client(url=self.__vault_url)
        hv_client.auth.aws.iam_login(access_key_id, secret_access_key, session_token=session_token, role=role,
                                     mount_point=mount_point)

        if hv_client.is_authenticated():
            self.login_method = lambda: hv_client.auth.aws.iam_login(access_key_id, secret_access_key,
                                                                     session_token=session_token, role=role,
                                                                     mount_point=mount_point)
            self.client = hv_client

        else:
            raise exceptions.Unauthorized(message='Client is not authorized via AWS IAM login method')

    def client_logout(self) -> None:
        """ Vault server logout mechanism

        This method logs out the actual client connected to Vault server by invalidating the access token


        """

        self.client.logout()

    def client_reauthentication(self) -> None:
        """ Vault server logout mechanism

        This method logs out the actual client connected to Vault server by invalidating the access token


        """

        self.login_method()
