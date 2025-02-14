from fastapi import APIRouter

from src.v1.models.model_health import ResponseAPIHealth

########################################################################################################################
# Router object definition
########################################################################################################################

router_health_api = APIRouter()


########################################################################################################################
# Resource definition
########################################################################################################################

@router_health_api.get('/api',
                       response_model=ResponseAPIHealth,
                       status_code=200,
                       summary='GET definition for requesting the API health status',
                       description="This method defines ..."
                       )
def health_api():
    return {
        'api_status': 'online'
    }
