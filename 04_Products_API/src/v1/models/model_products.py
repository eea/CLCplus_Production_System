from typing import Optional

from pydantic import BaseModel

from src.config import cnf


########################################################################################################################
# Response model for writing a QA/QC result
########################################################################################################################

class ResponseProductResult(BaseModel):
    result: str

    class Config:
        schema_extra = {
            "example": {
                "result": "https://s3.waw2-1.cloudferro.com/swift/v1/AUTH_abc/clcplus-public/products/CLMS_CLCplus_RASTER_2018_010m_eu_03035_V1_1.tif"
            }
        }


########################################################################################################################
# Response model for writing a QA/QC result
########################################################################################################################

class LinksModel(BaseModel):
    href: str
    rel: str
    type: str


########################################################################################################################
# Response model for writing a QA/QC result
########################################################################################################################

class ResponseAsyncProductResult(BaseModel):
    message: str
    links: LinksModel

    class Config:
        schema_extra = {
            "example": {
                "message": "Your order has been successfully submitted",
                "links": {
                    "href": "/services/orders/<order-id>/status",
                    "rel": "services",
                    "type": "GET"
                }
            }
        }


########################################################################################################################
# Response model for writing a QA/QC result
########################################################################################################################

class RequestNationalProduct(BaseModel):
    product: str
    nation: str
    project: Optional[str] = cnf.APP_CONFIG.PROJECT
    test: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "product": "Raster",
                "nation": "Austria"
            }
        }


########################################################################################################################
# Response model for writing a QA/QC result
########################################################################################################################

class RequestEuropeanProduct(BaseModel):
    product: str
    project: Optional[str] = cnf.APP_CONFIG.PROJECT
    test: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "product": "Raster"
            }
        }


########################################################################################################################
# Response model for writing a QA/QC result
########################################################################################################################

class RequestProduct(BaseModel):
    product: str
    aoi: str
    send_mail: Optional[bool] = False
    project: Optional[str] = cnf.APP_CONFIG.PROJECT
    test: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "product": "Raster",
                "aoi": "MULTIPOLYGON (((17.227309445590443 46.668932137424534, 17.2371487027879 47.10769387054001, "
                       "18.217384701084143 47.095973145761874, 18.19278655809051 46.65458260506014, 17.227309445590443 "
                       "46.668932137424534)))",
                "send_mail": True,
            }
        }
