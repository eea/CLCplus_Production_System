from pydantic import BaseModel


########################################################################################################################
# Error response model
########################################################################################################################

class HTTPError500(BaseModel):
    message: str
    type: str
    code: str

    class Config:
        schema_extra = {
            "example": {
                "error": {
                    "message": "Application error",
                    "type": "INTERNAL SERVER ERROR",
                    "code": 500,
                }
            }
        }
