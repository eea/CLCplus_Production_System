from typing import Any, List, Optional

from pydantic import BaseModel


########################################################################################################################
# Sample extraction request model
########################################################################################################################

class RequestSampleExtraction(BaseModel):
    s2_parameter_list: List[Any]
    test: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "s2_parameter_list": [
                    {"product_id": "S2A_MSIL2A_20180416T100031_N0207_R122_T33TWM_20180416T120451",
                     "bands": "B01,B03,B04,B05,B08,B09,B11,B12"},

                    {"product_id": "S2A_MSIL2A_20220302T100031_N0207_R122_T33TWM_20220302T100031",
                     "bands": "B01,B03,B04,B05,B08,B09,B11,B12,SCL"},

                    {"product_id": "S2A_MSIL2A_20190221T100031_N0207_R122_T33TWM_20190221T120451",
                     "bands": "B01,B03,B04,B05,B08,B09,B11"}]
            }
        }


class RequestSampleExtractionTesting(BaseModel):
    s2_parameter_list: List[Any]
    test: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "s2_parameter_list": [
                    {"product_id": "S2A_MSIL2A_20180416T100031_N0207_R122_T33TWM_20180416T120451",
                     "bands": "B01,B03,B04,B05,B08,B09,B11,B12"},

                    {"product_id": "S2A_MSIL2A_20220302T100031_N0207_R122_T33TWM_20220302T100031",
                     "bands": "B01,B03,B04,B05,B08,B09,B11,B12,SCL"},

                    {"product_id": "S2A_MSIL2A_20190221T100031_N0207_R122_T33TWM_20190221T120451",
                     "bands": "B01,B03,B04,B05,B08,B09,B11"}]
            }
        }


########################################################################################################################
# Apply model request model
########################################################################################################################

class RequestApplyModel(BaseModel):
    epsg: int
    resampling: str
    cloudmask_type: str
    model_path: str
    data: Any
    scene_ids_by_index: Any
    data_type: str
    path_prefix: str
    use_cache: bool
    data_source: str
    test: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "epsg": 4326,
                "resampling": "",
                "cloudmask_type": "",
                "model_path": "",
                "data": {
                    "key_1": "value_1",
                    "key_2": "value_2"
                },
                "scene_ids_by_index": {
                    "key_1": "value_1",
                    "key_2": "value_2"
                },
                "data_type": "",
                "path_prefix": "",
                "use_cache": False,
                "data_source": ""
            }
        }


class RequestApplyModelTesting(BaseModel):
    epsg: int
    resampling: str
    cloudmask_type: str
    model_path: str
    data: Any
    scene_ids_by_index: Any
    data_type: str
    path_prefix: str
    use_cache: bool
    data_source: str
    test: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "epsg": 4326,
                "resampling": "",
                "cloudmask_type": "",
                "model_path": "",
                "data": {
                    "key_1": "value_1",
                    "key_2": "value_2"
                },
                "scene_ids_by_index": {
                    "key_1": "value_1",
                    "key_2": "value_2"
                },
                "data_type": "",
                "path_prefix": "",
                "use_cache": False,
                "data_source": ""
            }
        }


########################################################################################################################
# Prepare samples request model
########################################################################################################################

class RequestPrepareSamples(BaseModel):
    start_date: str
    end_date: str
    include_url: str
    out_path: str
    data: dict
    test: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "start_date": "2022-01-01",
                "end_date": "2023-01-01",
                "include_url": False,
                "out_path": "/path",
                "data": {"type": "FeatureCollection",
                         "features": [
                             {"id": "5105",
                              "type": "Feature",
                              "properties": {
                                  "Name": "31UFU"
                              },
                              "geometry":
                                  {"type": "Polygon",
                                   "coordinates": [
                                       [
                                           [4.498460428000044, 53.240208349000056, 0.0],
                                           [6.141769904000057, 53.208201372000076, 0.0],
                                           [6.071678487000042, 52.22256603300008, 0.0],
                                           [4.4649803670000665, 52.25345680600003, 0.0],
                                           [4.498460428000044, 53.240208349000056, 0.0]
                                       ]
                                   ]
                                   }
                              }
                         ]
                         }
            }
        }


class RequestPrepareSamplesTesting(BaseModel):
    start_date: str
    end_date: str
    include_url: str
    out_path: str
    data: dict
    test: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "start_date": "2022-01-01",
                "end_date": "2023-01-01",
                "include_url": False,
                "out_path": "/path",
                "data": {"type": "FeatureCollection",
                         "features": [
                             {"id": "5105",
                              "type": "Feature",
                              "properties": {
                                  "Name": "31UFU"
                              },
                              "geometry":
                                  {"type": "Polygon",
                                   "coordinates": [
                                       [
                                           [4.498460428000044, 53.240208349000056, 0.0],
                                           [6.141769904000057, 53.208201372000076, 0.0],
                                           [6.071678487000042, 52.22256603300008, 0.0],
                                           [4.4649803670000665, 52.25345680600003, 0.0],
                                           [4.498460428000044, 53.240208349000056, 0.0]
                                       ]
                                   ]
                                   }
                              }
                         ]
                         }
            }
        }
