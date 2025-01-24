########################################################################################################################
#
# Copyright (c) 2022, GeoVille Information Systems GmbH
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, is prohibited for all commercial
# applications without licensing by GeoVille GmbH.
#
# Date created: 01.08.2022
# Date last modified: 01.08.2022
#
########################################################################################################################

from pydantic import BaseModel


########################################################################################################################
# Response model for the POST service request
########################################################################################################################

class HTTPError503(BaseModel):
    message: str
    type: str
    code: str

    class Config:
        schema_extra = {
            "example": {
                "error": {
                    "message": "Microservice is not available",
                    "type": "SERVICE UNAVAILABLE",
                    "code": 503,
                }
            }
        }
