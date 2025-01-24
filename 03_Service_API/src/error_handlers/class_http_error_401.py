from fastapi import Request
from fastapi.responses import JSONResponse

from src.init.app_constructor import api


########################################################################################################################
# Class definition
########################################################################################################################

class UnauthorizedError(Exception):
    def __init__(self, message: str):
        """ Constructor method

        This method is the is constructor method for the API error handling base class

        Arguments:
            message (str): HTTP error code

        """
        self.message = message
        self.type = "Authorization error"
        self.code = 401


########################################################################################################################
# Exception handler
########################################################################################################################

@api.exception_handler(UnauthorizedError)
def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=exc.code,
        content={"error": {
                "message": exc.message,
                "type": exc.type,
                "code": exc.code,
            }
        },
        headers={"WWW-Authenticate": "Bearer"}
    )
