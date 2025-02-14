from src.config import cnf
from src.error_handlers.class_http_error_403 import ForbiddenError


########################################################################################################################
# Method to check if a request to the Airflow-connector API is permitted
########################################################################################################################
def check_permissions(token_info, order_id):
    # check if order belongs to user or user is admin
    if (token_info['sub'] != order_id.split('_')[0]) and ('admin' not in token_info['scope']):
        raise ForbiddenError('Order ID does not correspond to this user')


########################################################################################################################
# Method to generate the content of the result value
########################################################################################################################

def get_service_result_value(service, order_id, status):
    if status == "success":
        if service == 'test-service' or service == 'test-service-gaf':
            result = f'Order {order_id} successfully completed'
        elif service == 'harmonics':
            if cnf.ENV_STATE.lower() == 'dev':
                result = f's3://s3.waw3-1.cloudferro.com/dev-harmonics/{order_id}'
            else:
                result = f's3://s3.waw3-1.cloudferro.com/harmonics/{order_id}'
        else:
            result = f'Result provision not implemented for service {service}'
    elif status == "failed":
        result = "Service failed. Further information can be retrieved from service logs in airflow"
    elif status == "running" or status == "queued":
        result = None
    else:
        raise Exception("Not able to retrieve result: Unknown order status")

    return result
