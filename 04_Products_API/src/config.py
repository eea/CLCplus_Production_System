from typing import Optional

from pydantic import BaseSettings, Field, BaseModel


########################################################################################################################
#
########################################################################################################################

class AppConfig(BaseModel):
    """Application configurations."""

    # Generic configuration
    PROJECT: str = "CLC-Backbone-Products"
    EVENT_SOURCE: str = "Backbone-Products-API-Order-Service"

    # Hashicorp Vault static secret paths
    SECRET_MOUNT: str = "gems"
    SECRET_PATH: str = "apis/general_secrets"

    OWNCLOUD_MOUNT: str = "infrastructure"
    OWNCLOUD_PATH: str = "nextcloud"

    DB_PATH_STATIC: str = "apis/backbone_products/database"

    TEST_DB_MOUNT: str = "infrastructure"
    TEST_DB_PATH: str = "bitbucket_pipelines/tests/database"


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
    VAULT_AWS_ROLE: Optional[str]
    VAULT_LOGIN_MOUNT: Optional[str] = "aws-gems"

    # AWS Load Balancer path prefix. For local development can randomly set. In production, it will be set by Terraform.
    PATH_PREFIX: Optional[str] = "/backbone-products"

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

