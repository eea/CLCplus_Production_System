from pydantic import BaseModel


########################################################################################################################
# Model for the Link element
########################################################################################################################

class LinksModel(BaseModel):
    href: str
    rel: str
    type: str


########################################################################################################################
# Generic response model
########################################################################################################################

class ResponseServices(BaseModel):
    message: str
    links: LinksModel

    class Config:
        schema_extra = {
            "example": {
                "message": "Your order has been successfully received",
                "links": {
                    "href": "/orders/status/{order_id}",
                    "rel": "orders",
                    "type": "GET"
                }
            }
        }