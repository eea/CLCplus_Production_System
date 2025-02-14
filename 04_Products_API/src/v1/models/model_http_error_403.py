from pydantic import BaseModel


########################################################################################################################
# Error response model
########################################################################################################################

class HTTPError403(BaseModel):
    message: str
    type: str
    code: str

    class Config:
        schema_extra = {
            "example": {
                "error": {
                    "message": "Not sufficient access rights",
                    "type": "Forbidden",
                    "code": 403,
                }
            }
        }
