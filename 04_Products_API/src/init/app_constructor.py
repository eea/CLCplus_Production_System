import logging
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

from src.config import cnf
from src.init.init_variables import TOKEN_URL
from src.logger.logger_config import log_config_dev, log_config_prod

########################################################################################################################
# Definition of logger object depending on the env state
########################################################################################################################

if cnf.ENV_STATE == 'dev':
    dictConfig(log_config_dev)

elif cnf.ENV_STATE == 'prod':
    dictConfig(log_config_prod)

logger = logging.getLogger('app_logger')

########################################################################################################################
# Definition of the OpenAPI documentation UI for the API
########################################################################################################################

api = FastAPI(title='CLC+ Backbone API',
              description='CLC+ Backbone Products API powered by GeoVille',
              version='23.7',
              openapi_url=f'{cnf.PATH_PREFIX}/openapi.json',
              docs_url=f"{cnf.PATH_PREFIX}/v1",
              redoc_url=f'{cnf.PATH_PREFIX}/redoc/v1',
              swagger_ui_parameters={"defaultModelsExpandDepth": -1}
              )


########################################################################################################################
# Automatic redirect to OpenAPI docs
########################################################################################################################

@api.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url=f"{cnf.PATH_PREFIX}/v1")


########################################################################################################################
# CORS definition for the app object
########################################################################################################################

origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

########################################################################################################################
# OAuth2 schema definition for the OpenAPI documentation
########################################################################################################################

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
