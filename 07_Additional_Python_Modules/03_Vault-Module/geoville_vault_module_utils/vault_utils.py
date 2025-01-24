import requests
from hvac import Client, exceptions


########################################################################################################################
# Method definition
########################################################################################################################

def __get_dynamic_db_credentials(vault_url: str, vault_token: str, db_mount: str, db_role: str) -> dict:
    """ Returns the dynamic database credentials

    This method returns dynamic database credentials with the help of a database role.

    Arguments:
        vault_url (str): Vault server URL
        vault_token (str): Vault token
        db_mount (str): name of the mount endpoint for the database configuration
        db_role (str): Vault database role which has read access on the mount endpoint

    Returns:
        (dict)

    """

    headers = {'X-Vault-Token': vault_token}
    response = requests.request('GET', f"{vault_url}/v1/{db_mount}/creds/{db_role}", headers=headers)

    if response.status_code == 200:
        return {
            'user': response.json()['data']['username'],
            'password': response.json()['data']['password'],
        }

    elif response.status_code == 403:
        raise exceptions.Forbidden(message=f'Provided token does not have enough access right')

    else:
        raise exceptions.InvalidRequest(message=f"Bad request: {response.json()}")


########################################################################################################################
# Method definition
########################################################################################################################

def __get_db_connection_parameters(client: Client, mount: str, path: str) -> dict:
    """ Returns the database connection parameters from the key value store

    This method returns the database connection parameters from the key value store. The parameters in the key value
    store must be declared always as the following:
        db_host -> host
        db_port -> port
        db_name -> database

    Arguments:
        client (Client): HVAC client object
        mount (str): name of the mount endpoint for the key-value endpoint
        path (str): actual name of the mount endpoint for the key-value endpoint

    Returns:
        (dict): dictionary containing host port and database name

    """

    try:
        db_conn_params = client.secrets.kv.v2.read_secret_version(path=path, mount_point=mount)

        return {
            'host': db_conn_params['data']['data']['host'],
            'port': db_conn_params['data']['data']['port'],
            'database': db_conn_params['data']['data']['database'],
        }

    except Exception as err:
        print(f'Could not query the database connection parameter: {err}')
        return {}
