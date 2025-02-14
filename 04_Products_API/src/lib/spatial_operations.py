import pyproj
import shapely.wkt
from shapely.ops import transform

from src.error_handlers.class_http_error_400 import BadRequestError
from src.init.app_constructor import logger


########################################################################################################################
# Calculates the area of a GeoJSON
########################################################################################################################

def calculate_aoi_size(aoi: str) -> None:
    """ Calculates the area of a GeoJSON

    This method calculates the area of a GeoJSON by reprojecting it first to EPSG code 3857.

    Arguments:
        aoi (GeoJSON): Scopes coming from the REST endpoint through dependency injection

    """

    reproject = pyproj.Transformer.from_crs(pyproj.CRS('EPSG:4326'), pyproj.CRS('EPSG:3857'), always_xy=True).transform
    aoi_metric = transform(reproject, shapely.wkt.loads(aoi))
    aoi_area = aoi_metric.area * 1.0E-6

    if aoi_area > 5000000:
        logger.error(f'write_qa_qc_result: Requested size to big')
        raise BadRequestError("The requested AOI is too big (> 5 Mio. km²). Please note that countries and entire "
                              "Europe can be requested with other endpoints.")
