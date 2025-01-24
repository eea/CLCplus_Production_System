from geoville_vault_module.vault_client import VaultClient


########################################################################################################################
# Method definition
########################################################################################################################

def revoke_credentials(vault_client: VaultClient, lease_id: str) -> None:
    """ Revokes a lease immediately

    This method uses the previously created HVAC client object to immediately revoke any lease in the Hashicorp Vault
    server by specifying the ID of the actual lease.

    Arguments:
        vault_client (VaultClient): VaultClient object
        lease_id (str): Specifies the ID of the lease to revoke

    """

    if not vault_client.client.is_authenticated():
        vault_client.client_reauthentication()

    vault_client.client.sys.revoke_lease(
        lease_id=lease_id,
    )
