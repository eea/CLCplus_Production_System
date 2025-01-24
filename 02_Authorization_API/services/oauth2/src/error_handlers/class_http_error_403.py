from fastapi import Request
from fastapi.responses import JSONResponse

from src.init.app_constructor import api


########################################################################################################################
# Class definition
########################################################################################################################

class ForbiddenError(Exception):
    def __init__(self, message: str):
        """ Constructor method

        This method is the is constructor method for the API error handling base class

        Arguments:
            message (str): HTTP error code

        """
        self.message = message
        self.type = "Permission denied"
        self.code = 403


########################################################################################################################
# Exception handler
########################################################################################################################

@api.exception_handler(ForbiddenError)
def unauthorized_exception_handler(request: Request, exc: ForbiddenError):
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
