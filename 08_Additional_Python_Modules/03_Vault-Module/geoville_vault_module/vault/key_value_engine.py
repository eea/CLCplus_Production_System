from geoville_vault_module.vault_client import VaultClient


########################################################################################################################
# Method definition
########################################################################################################################

def get_kv_secret_dict(vault_client: VaultClient, secret_path: str, secret_mount: str) -> dict:
    """ Returns all secrets stored at the given path and mount

    This method uses the previously created HVAC client object to access credentials from the Hashicorp Vault server by
    specifying the secret mount and path within the Hashicorp Vault server itself. A dictionary with all existing
    credentials at this location will be returned.

    Arguments:
        vault_client (VaultClient): VaultClient object
        secret_path (str): Hashicorp Vault secret path
        secret_mount (str): Hashicorp Vault secret mount

    Returns:
        (dict): all secret stored at this mount and path combination and the current HVAC client object

    """

    return get_kv_secret_list(vault_client, secret_path, secret_mount)


########################################################################################################################
# Method definition
########################################################################################################################

def get_kv_secret_list(vault_client: VaultClient, secret_path: str, secret_mount: str) -> dict:
    """ Returns all secrets stored at the given path and mount

    This method uses the previously created HVAC client object to access credentials from the Hashicorp Vault server by
    specifying the secret mount and path within the Hashicorp Vault server itself. A dictionary with all existing
    credentials at this location will be returned.

    Arguments:
        vault_client (VaultClient): VaultClient object
        secret_path (str): Hashicorp Vault secret path
        secret_mount (str): Hashicorp Vault secret mount

    Returns:
        (dict): all secret stored at this mount and path combination and the current HVAC client object

    """

    if not vault_client.client.is_authenticated():
        vault_client.client_reauthentication()

    secret_version_response = vault_client.client.secrets.kv.v2.read_secret_version(
        path=secret_path,
        mount_point=secret_mount
    )
    return secret_version_response['data']['data']


########################################################################################################################
# Method definition
########################################################################################################################

def get_kv_secret(vault_client: VaultClient, secret_path: str, secret_mount: str, secret_name: str) -> str:
    """ Returns all secrets stored in Hashicorp Vault at the given location

    This method uses the previously created HVAC client object to access credentials from the Hashicorp Vault server by
    specifying the secret mount, path and name within the Hashicorp Vault server itself. A string with the specified
    secret at this location will be returned.

    Arguments:
        vault_client (VaultClient): VaultClient object
        secret_path (str): Hashicorp Vault secret path
        secret_mount (str): Hashicorp Vault secret mount
        secret_name (str): Name of the desired secret

    Returns:
        (str): Value of the secret to be retrieved

    """

    if not vault_client.client.is_authenticated():
        vault_client.client_reauthentication()

    secret_version_response = vault_client.client.secrets.kv.v2.read_secret_version(
        path=secret_path,
        mount_point=secret_mount
    )
    return secret_version_response['data']['data'][secret_name]
