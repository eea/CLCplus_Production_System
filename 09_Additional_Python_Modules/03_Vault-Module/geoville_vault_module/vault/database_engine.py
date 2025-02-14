from geoville_vault_module.vault_client import VaultClient
from geoville_vault_module_utils.vault_utils import __get_db_connection_parameters, __get_dynamic_db_credentials


########################################################################################################################
# Method definition
########################################################################################################################

def get_static_db_credentials(vault_client: VaultClient, mount: str, path: str) -> dict:
    """ Returns static database connection parameters from the key value store

    This method returns the static database connection parameters from the key value store. The parameters in the key
    value store must be declared always as the following in order to work properly.
        db_host -> host
        db_port -> port
        db_name -> database
        db_user -> user
        db_pass -> password

    Arguments:
        vault_client (VaultClient): VaultClient object
        mount (str): name of the mount point for the key-value endpoint
        path (str): name of the path for the key-value endpoint

    Returns:
        (dict): dictionary containing required db connection parameters

    """

    if not vault_client.client.is_authenticated():
        vault_client.client_reauthentication()

    db_conn_params = vault_client.client.secrets.kv.v2.read_secret_version(path=path, mount_point=mount)

    return {
        'host': db_conn_params['data']['data']['host'],
        'port': db_conn_params['data']['data']['port'],
        'database': db_conn_params['data']['data']['database'],
        'user': db_conn_params['data']['data']['user'],
        'password': db_conn_params['data']['data']['password']
    }


########################################################################################################################
# Method definition
########################################################################################################################

def get_dynamic_db_credentials(vault_client: VaultClient, db_mount: str, db_role: str, kv_mount: str,
                               kv_path: str) -> dict:
    """ Returns dynamic database credentials under the given input paths

    This method returns the dynamic database connection parameters from the Hashicorp Vault server. A database
    connection, a role to read from the connection and a key value store are required in Vault to use this
    functionality.

    Arguments:
        vault_client (VaultClient): VaultClient object
        db_mount (str): name of the mount endpoint for the database configuration
        db_role (str): Vault database role which has read access on the mount endpoint
        kv_mount (str): name of the mount endpoint for the key-value endpoint
        kv_path (str): actual name of the mount endpoint for the key-value endpoint

    Returns:
        (dict): database connection parameters retrieved from the Vault server

    """

    if not vault_client.client.is_authenticated():
        vault_client.client_reauthentication()

    db_user_pass = __get_dynamic_db_credentials(vault_client.client.url, vault_client.client.token, db_mount, db_role)
    db_conn = __get_db_connection_parameters(vault_client.client, kv_mount, kv_path)
    return {**db_user_pass, **db_conn}
