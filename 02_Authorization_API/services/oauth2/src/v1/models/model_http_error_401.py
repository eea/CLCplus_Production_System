from pydantic import BaseModel


########################################################################################################################
# Error response model
########################################################################################################################

class HTTPError401(BaseModel):
    message: str
    type: str
    code: str

    class Config:
        schema_extra = {
            "example": {
                "error": {
                    "message": "Wrong credentials supplied",
                    "type": "UNAUTHORIZED",
                    "code": 401,
                }
            }
        }
