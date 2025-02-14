import os

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
    VAULT_CLIENT.aws_iam_login(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'),
                               session_token=os.environ.get('AWS_SESSION_TOKEN'), role=cnf.VAULT_AWS_ROLE,
                               mount_point=cnf.VAULT_LOGIN_MOUNT)
vault_api_secrets = get_kv_secret_list(VAULT_CLIENT, cnf.APP_CONFIG.SECRET_PATH, cnf.APP_CONFIG.SECRET_MOUNT)

########################################################################################################################
# Retrieves the Keycloak public key at API start up
########################################################################################################################

KC_CLIENT = KeycloakClient(vault_api_secrets['keycloak_url'], vault_api_secrets['keycloak_realm'],
                           vault_api_secrets['keycloak_client_id'], vault_api_secrets['keycloak_client_secret'])

########################################################################################################################
# Token URL endpoint
########################################################################################################################

TOKEN_URL = vault_api_secrets['token_url']

########################################################################################################################
# GEMS event bus
########################################################################################################################

EVENT_BUS = vault_api_secrets['gems_event_bus']
