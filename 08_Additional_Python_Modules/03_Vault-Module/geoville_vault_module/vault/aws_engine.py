from hvac.constants.aws import DEFAULT_MOUNT_POINT

from geoville_vault_module.vault_client import VaultClient


########################################################################################################################
# Method definition
########################################################################################################################

def aws_temp_creds(vault_client: VaultClient, aws_role: str, mount_point: str = DEFAULT_MOUNT_POINT) -> dict:
    """ Returns temporary AWS role credentials

    This method uses the previously created HVAC client object to access AWS IAM role credentials from the Hashicorp
    Vault server by specifying the desired AWS role. A dictionary with all credentials will be returned.

    Arguments:
        vault_client (VaultClient): HVAC client object
        aws_role (str): AWS role defined in Vault to create credentials for
        mount_point (str): Optional parameter to specify the mount point of the aws secret engine


    Returns:
        creds (dict): AWS IAM role credentials and lease ID

    """

    if not vault_client.client.is_authenticated():
        vault_client.client_reauthentication()

    creds = vault_client.client.secrets.aws.generate_credentials(name=aws_role, mount_point=mount_point)

    if 'session_token' in creds['data']:
        session_token = creds['data']['session_token']
    elif 'security_token' in creds['data']:
        session_token = creds['data']['security_token']

    return {
        'lease_id': creds['lease_id'],
        'access_key': creds['data']['access_key'],
        'secret_key': creds['data']['secret_key'],
        'security_token': session_token
    }
