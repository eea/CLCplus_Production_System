from geoville_keycloak_module.keycloak_client import KeycloakClient
from geoville_vault_module.vault.key_value_engine import get_kv_secret_list
from geoville_vault_module.vault_client import VaultClient

from src.config import cnf

########################################################################################################################
# Vault login and querying all available secrets at start up
########################################################################################################################

vault_client = VaultClient(cnf.VAULT_URL)

if cnf.VAULT_TOKEN:
    vault_client.token_login(cnf.VAULT_TOKEN)
else:
    vault_client.app_role_login(cnf.VAULT_ROLE_ID, cnf.VAULT_SECRET_ID, cnf.APP_CONFIG.VAULT_AUTH_MOUNT)

vault_api_secrets = get_kv_secret_list(vault_client, cnf.APP_CONFIG.SECRET_PATH, cnf.APP_CONFIG.SECRET_MOUNT)

########################################################################################################################
# Retrieves the Keycloak public key at API start up
########################################################################################################################

KC_CLIENT = KeycloakClient(vault_api_secrets['keycloak_url'], vault_api_secrets['keycloak_realm'],
                           vault_api_secrets['keycloak_client_id'], vault_api_secrets['keycloak_client_secret'])
