import uvicorn

from src.init.app_constructor import api
from src.init.namespace_constructor import router_services, router_health, router_orders
from src.v1.resources.gaf_apply_model import router_gaf_apply_model
from src.v1.resources.gaf_apply_model_testing import router_gaf_apply_model_testing
from src.v1.resources.gaf_prepare_samples import router_gaf_prepare_samples
from src.v1.resources.gaf_prepare_samples_testing import router_gaf_prepare_samples_testing
from src.v1.resources.gaf_sample_extraction import router_gaf_sample_extraction
from src.v1.resources.gaf_sample_extraction_testing import router_gaf_sample_extraction_testing
from src.v1.resources.health_status import router_health_api
from src.v1.resources.order_abort import router_order_abort
from src.v1.resources.order_status import router_order_status


########################################################################################################################
# Adding routers for the endpoints to the corresponding namespaces
########################################################################################################################

router_health.include_router(router_health_api)
router_orders.include_router(router_order_status)
router_orders.include_router(router_order_abort)
router_services.include_router(router_gaf_apply_model)
router_services.include_router(router_gaf_apply_model_testing)
router_services.include_router(router_gaf_prepare_samples)
router_services.include_router(router_gaf_prepare_samples_testing)
router_services.include_router(router_gaf_sample_extraction)
router_services.include_router(router_gaf_sample_extraction_testing)

########################################################################################################################
# Adding all routers to the API
########################################################################################################################

api.include_router(router_services)
api.include_router(router_orders)
api.include_router(router_health)

########################################################################################################################
# Run the app locally from the code
########################################################################################################################

if __name__ == "__main__":
    uvicorn.run("api:api", host="127.0.0.1", port=8080, reload=True)
