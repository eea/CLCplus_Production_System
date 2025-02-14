from typing import List

from pydantic import BaseModel


########################################################################################################################
# Response model for writing a QA/QC result
########################################################################################################################

class ResponseNationalProduct(BaseModel):
    nations: List[str]

    class Config:
        schema_extra = {
            "example": {
                "nations": [
                    "Austria",
                    "Germany"
                ]
            }
        }
