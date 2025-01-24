import logging
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.config import cnf
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

api = FastAPI(title='CLC Backbone Authentication Service API',
              description='CLC Backbone Authentication Service API based on a Microservice architecture',
              version='23.1',
              openapi_url=f'/openapi.json',
              docs_url=cnf.APP_CONFIG.DOCS_PATH,
              redoc_url=cnf.APP_CONFIG.REDOCS_PATH,
              root_path="/authentication-service",
              swagger_ui_parameters={"defaultModelsExpandDepth": -1}
              )


########################################################################################################################
# Automatic redirect to OpenAPI docs
########################################################################################################################

@api.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url=f"/authentication-service{cnf.APP_CONFIG.DOCS_PATH}")


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
