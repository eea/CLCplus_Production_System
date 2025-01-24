from typing import Optional

from pydantic import BaseSettings, Field, BaseModel


########################################################################################################################
#
########################################################################################################################

class AppConfig(BaseModel):
    """Application configurations."""

    # URL path for API specs
    OAS_PATH: str = "/v1"

    # Hashicorp Vault static secret paths
    VAULT_AUTH_MOUNT: str = "approle-clcplus_rasterupdate"

    SECRET_MOUNT: str = "projects"
    GENERAL_SECRET_PATH: str = "clcplus_rasterupdate/apis/general_secrets"
    API_SECRET_PATH: str = "clcplus_rasterupdate/apis/services"


########################################################################################################################
#
########################################################################################################################

class GlobalConfig(BaseSettings):
    """ Global configurations

    These variables will be loaded from the .env file. However, if there is a shell environment variable having the same
    name, that will take precedence.

    """

    APP_CONFIG: AppConfig = AppConfig()

    # define global variables with the Field class
    ENV_STATE: Optional[str] = Field(None, env="ENV_STATE")

    # Hashicorp Vault relevant variables loaded from environment variables
    VAULT_URL: Optional[str]
    VAULT_TOKEN: Optional[str]
    VAULT_ROLE_ID: Optional[str]
    VAULT_SECRET_ID: Optional[str]

    class Config:
        """Loads the dotenv file."""

        env_file: str = ".env"


########################################################################################################################
#
########################################################################################################################

class DevConfig(GlobalConfig):
    """Development configurations."""

    class Config:
        env_prefix: str = "dev_"


########################################################################################################################
#
########################################################################################################################

class ProdConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "prod_"


########################################################################################################################
#
########################################################################################################################

class FactoryConfig:
    """Returns a config instance depending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


########################################################################################################################
# Instantiation of configuration object
########################################################################################################################

cnf = FactoryConfig(GlobalConfig().ENV_STATE)()
