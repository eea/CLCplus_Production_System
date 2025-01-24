from datetime import datetime

from pydantic.main import ModelMetaclass

from src.error_handlers.class_http_error_400 import BadRequestError


########################################################################################################################
# Checks if a given start date is greater than a given end date
########################################################################################################################

def date_range_validation(cls: ModelMetaclass, values: dict) -> dict:
    if values['start_date'] > values['end_date']:
        raise BadRequestError('Start date is greater than end date')
    return values


########################################################################################################################
# Checks if a given date is in the correct format
########################################################################################################################

def date_validation(in_date: str) -> str:
    try:
        datetime.strptime(in_date, "%Y-%m-%d")
    except ValueError:
        raise BadRequestError('Date is not of the format %Y-%m-%d')

    return in_date
