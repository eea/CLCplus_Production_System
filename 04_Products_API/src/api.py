import uvicorn

from src.init.app_constructor import api
from src.init.namespace_constructor import router_health, router_nations, router_orders, router_products
from src.v1.resources.get_european_products import router_european_products
from src.v1.resources.get_national_products import router_national_products
from src.v1.resources.get_nations import router_get_nations
from src.v1.resources.get_products import router_get_products
from src.v1.resources.health_api import router_health_api
from src.v1.resources.order_abort import router_order_abort
from src.v1.resources.order_status import router_order_status
from src.v1.resources.order_update import router_order_update

########################################################################################################################
# Adding endpoint routers to the corresponding namespaces
########################################################################################################################

router_nations.include_router(router_get_nations)
router_products.include_router(router_get_products)
router_products.include_router(router_european_products)
router_products.include_router(router_national_products)
router_orders.include_router(router_order_update)
router_orders.include_router(router_order_abort)
router_orders.include_router(router_order_status)
router_health.include_router(router_health_api)

########################################################################################################################
# Adding all routers to the API
########################################################################################################################

api.include_router(router_products)
api.include_router(router_nations)
api.include_router(router_orders)
api.include_router(router_health)

########################################################################################################################
# Run the app locally from the code
########################################################################################################################

if __name__ == "__main__":
    uvicorn.run(app="api:api", host="127.0.0.1", port=8080, reload=True)
