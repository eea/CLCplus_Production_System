from pydantic import BaseModel


########################################################################################################################
# Error response model
########################################################################################################################

class HTTPError503(BaseModel):
    message: str
    type: str
    code: str

    class Config:
        schema_extra = {
            "example": {
                "error": {
                    "message": "The microservice is not available",
                    "type": "SERVICE UNAVAILABLE",
                    "code": 503,
                }
            }
        }
