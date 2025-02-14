from fastapi import Request
from fastapi.responses import JSONResponse

from src.init.app_constructor import api


########################################################################################################################
# Class definition
########################################################################################################################

class BadRequestError(Exception):
    def __init__(self, message: str):
        """ Constructor method

        This method is the is constructor method for the API error handling base class

        Arguments:
            message (str): HTTP error code

        """
        self.message = message
        self.type = "Invalid user request"
        self.code = 400


########################################################################################################################
# Exception handler
########################################################################################################################

@api.exception_handler(BadRequestError)
def bad_request_exception_handler(request: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=exc.code,
        content={"error": {
                "message": exc.message,
                "type": exc.type,
                "code": exc.code
            }
        }
    )
