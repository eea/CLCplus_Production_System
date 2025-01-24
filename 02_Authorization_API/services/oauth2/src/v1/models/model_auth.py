from pydantic import BaseModel


########################################################################################################################
# Response model for refresh and bearer token
########################################################################################################################

class ResponseToken(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str
    session_state: str
    scope: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6",
                "expires_in": 300,
                "refresh_expires_in": 1800,
                "refresh_token": "eyJhbGciOiorwRY5RxTnjUzPhPLFoX3cHtn-9RWo3sIQCY",
                "token_type": "Bearer",
                "session_state": "fa93b6b0-154b-4154-842d-db42ef000ad2",
                "scope": "email profile"
            }
        }


########################################################################################################################
# Request model for generating a new access token via a refresh token
########################################################################################################################

class RequestRefreshToken(BaseModel):
    refresh_token: str

    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiorwRY5RxTnjUzPhPLFoX3cHtn-9RWo3sIQCY"
            }
        }
