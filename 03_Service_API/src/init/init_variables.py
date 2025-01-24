from geoville_keycloak_module.keycloak_client import KeycloakClient
from geoville_vault_module.vault.key_value_engine import get_kv_secret_list
from geoville_vault_module.vault_client import VaultClient

from src.config import cnf

########################################################################################################################
# Vault login and querying all available secrets at start up
########################################################################################################################

VAULT_CLIENT = VaultClient(cnf.VAULT_URL)

if cnf.VAULT_TOKEN:
    VAULT_CLIENT.token_login(cnf.VAULT_TOKEN)
else:
    VAULT_CLIENT.app_role_login(cnf.VAULT_ROLE_ID, cnf.VAULT_SECRET_ID, cnf.APP_CONFIG.VAULT_AUTH_MOUNT)

api_secrets = get_kv_secret_list(VAULT_CLIENT, cnf.APP_CONFIG.GENERAL_SECRET_PATH, cnf.APP_CONFIG.SECRET_MOUNT)

########################################################################################################################
# Setup up a keycloak client for token validation
########################################################################################################################

KC_CLIENT = KeycloakClient(api_secrets['keycloak_url'], api_secrets['keycloak_realm'],
                           api_secrets['keycloak_client_id'], api_secrets['keycloak_client_secret'])

########################################################################################################################
# Token URL endpoint
########################################################################################################################

TOKEN_URL = api_secrets[f'token_url']
