from typing import Any, Optional

from pydantic import BaseModel


########################################################################################################################
# GET response model for requesting the order status
########################################################################################################################

class ResponseResultStatus(BaseModel):
    order_id: str
    status: Any
    result: Optional[Any]
    expiration_in_days: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "order_id": "391d3b45f059f9fb74b79868f6e8511e",
                "status": "SUCCESS",
                "result": "https://gems-demo.s3.amazonaws.com",
                "expiration_in_days": 30
            }
        }
