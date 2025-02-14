from pydantic import BaseModel


########################################################################################################################
# Error response model
########################################################################################################################

class HTTPError400(BaseModel):
    message: str
    type: str
    code: str

    class Config:
        schema_extra = {
            "example": {
                "error": {
                    "message": "Invalid user data",
                    "type": "BAD_REQUEST",
                    "code": 400,
                }
            }
        }
