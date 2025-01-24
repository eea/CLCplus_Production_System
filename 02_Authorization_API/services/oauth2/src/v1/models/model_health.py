from pydantic import BaseModel


########################################################################################################################
# Response model for the API health endpoint
########################################################################################################################

class ResponseAPIHealth(BaseModel):
    api_status: str

    class Config:
        schema_extra = {
            "example": {
                "api_status": "online"
            }
        }
