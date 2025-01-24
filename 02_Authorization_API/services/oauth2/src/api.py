import uvicorn

from src.init.app_constructor import api
from src.init.namespace_constructor import router_auth, router_health
from src.v1.resources.auth_access_token import router_oauth_token
from src.v1.resources.auth_refresh_token import router_refresh_token
from src.v1.resources.health_api import router_health_api

########################################################################################################################
# Adding routers for the endpoints to the corresponding namespaces
########################################################################################################################

router_auth.include_router(router_oauth_token)
router_auth.include_router(router_refresh_token)
router_health.include_router(router_health_api)

########################################################################################################################
# Adding all routers to the API
########################################################################################################################

api.include_router(router_auth)
api.include_router(router_health)

########################################################################################################################
# Run the app locally from the code
########################################################################################################################

if __name__ == "__main__":
    uvicorn.run("api:api", host="127.0.0.1", port=8080, reload=True)
