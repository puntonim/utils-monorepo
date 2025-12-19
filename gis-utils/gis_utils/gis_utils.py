"""
** GIS UTILS **
===============

```py
import gis_utils

white_house = (38.898, -77.037)
eiffel_tower = (48.858, 2.294)
dist = gis_utils.compute_euclidean_distance(*white_house, *eiffel_tower)
assert dist == 6454.2071214371235
```
"""

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "polyline_str_to_coords",
    "compute_great_circle_distance",
    "compute_euclidean_distance",
]

from math import asin, cos, radians, sin, sqrt


def _trans_polyline(value, index):
    # Used in polyline_str_to_coords().

    byte = None
    result = 0
    shift = 0
    comp = None
    while byte is None or byte >= 0x20:
        byte = ord(value[index]) - 63
        index += 1
        result |= (byte & 0x1F) << shift
        shift += 5
        comp = result & 1

    return ~(result >> 1) if comp else (result >> 1), index


def polyline_str_to_coords(
    polyline_str: str,
    # nimiq: I removed the `precision` arg because confusing.
    # precision: int = 5,
    # nimiq: I removed the `geojson` arg because useless.
    # geojson: bool = False,
) -> tuple[tuple[float, float]]:
    r"""
    Source: https://github.com/frederickjansen/polyline/blob/master/src/polyline/polyline.py#L47
    Online polyline decoder: https://polylinedecoder.online/

    Decode a polyline string into a tuple of coordinates.

    Args:
        polyline_str: polyline string, e.g. r"u{~vFvyys@fS]".

    Returns: tuple of tuples in (lat, lon) order.

    Example:
        # Strava segment Re Stelvio Mapei, segment-id 15104529341.
        polyline = r"abszGqhh~@s@nD{F~I{HbE_@AQeAzBqIYk@qGpEiEn@sPmBlG{EeGeAmBiCqIdF{IAgCdBwAdDeEdC}A~CiEi@cC_BwKpHqPlC}CvDuAdDgC`@gB~CBlC]bA{DbCuDbEcBXmA~AoBEkNxAqClCiCt@}GQqDpAuAc@uEoNoGiLVSfEtEwDeIaE}OeGcMNQ|D`FyDsJAwE}@kED}AcC}EmAc@}BsD_@yIeC_IUqDfBvEk@eF^lB`AhBZAqAoEQoEHeBvAqAPkSdAgH[_Lf@cDmBoQ@uDf@uBuAgCGyEoB_Ja@mJsCwD}AuEoCcEeDyLwEaH?e@l@BlD`DXOoBmCcA}CkByAxBj@nAvBR[yGiMgDCzByByEp@zFmFyFt@aCjB~AmD`EmCG[gGlAyCxFpBeJbFqCf@eAkInCoAbCsF|DSg@bA}F`EsCcL|B}LwB{BoA}D|CiCs@sLlBuAOiFwD{CMqElAqKw@aKuEkDeG{FOyCmDwE}@cKeQsA_EgDex@f@oJx@_GtBoGhIsI}GhAdJeKgE`@kCrAtAaEfHeEjByFdGmFs@{BjNyAdHiDgFaMC{AbBgDtEyB`AiDu@y@kGv@Wa@LkAdDcIb@iGzE\jC~CZcAsAyEpGeAy@gLuA[tGeJ~EE@cC}@}BtAwKFjA{ApIv@~APxBu@rAmDs@kHzIzAt@`AnKuGhAjAtEWbAcCwCaFg@c@pGgDjIIfAZj@dGw@r@h@aAhD_FjCuAxCNpBtElLmGzC{N|Al@fCcGbFcBzFcHbE}BlETd@hCqBjEi@iJzJTd@lGeBsIvIwAzDmAzGi@`MpCvt@x@dEdLpSjFhA`DvDvFJdDtFtKjF~Jj@`FoAtCPvGjEhMyBhCx@`E_D|AlAlMtBbLiCuDzAuAzHVn@rFoDvBmDnGcBaG|DqBxI`@TpCsFzFwAoE~CyAfCDl@dKcDcGnFbFi@}BrB~DXpGpLyAiBmCc@hBhB|@rCvBtCqDuCw@IKj@`FhH~DnNjBpBhBnF`ChCTfJdAjC~DfT_ArAApB`AtM?hLx@vEa@hEy@zAc@hMcBhNNdDxAdFaCaFr@dFkBwETxE|BlGb@bJdCfE`GrBaAfB?bBdAxEAfEzD|JsDeFYVpG`NdDxMlEjJkEyEU^lElHpFzMp@zC|Ad@hDwA~GL`Cu@dCoCrNwAlBNrD{B|JyIJsDpB_EzBSlFwIhPiC|K{HxCfBzDf@dBmDfEcChAmCtBeBjJIfH}ElAJjAdB~FlAyBxBiC`APz@pSpAdCs@lF_EJx@yBfIN|@n@@hGsCjGiJbAwBl@sIxBsDbD]fIfFk@qCv@_FtHeB"
        coords = gis_utils.polyline_str_to_coords(polyline)
        assert len(coords) == 349
        assert coords[0] == (46.46961, 10.36953)
        assert coords[348] == (46.46477, 10.37296)

    """
    if not isinstance(polyline_str, str):
        raise TypeError("polyline_str must be a string")

    result = []
    index = 0
    lat = 0
    lng = 0
    length = len(polyline_str)
    # nimiq: I removed the `precision` arg because confusing. It is the # decimal
    #  digits. But it didn't change the total number of digits, it just shifted the dot.
    #  Eg. 46.46961 with precision=5, 4.646961 with precision=6.
    #  The most used precision is 5, so better stick to it or it gets confusing.
    #  Google Maps uses 5, OpenStreetMap uses 6.
    #  Eg, with precision 5:
    #      white_house = (38.898, -77.037)
    #      eiffel_tower = (48.858, 2.294)
    #      bsas = (-34.83333, -58.5166646)  # Ezeiza Airport (Buenos Aires, Argentina).
    #      paris = (49.0083899664, 2.53844117956)  # C. de Gaulle Airport (Paris, France).
    precision = 5
    factor = float(10**precision)

    while index < length:
        lat_change, index = _trans_polyline(polyline_str, index)
        lng_change, index = _trans_polyline(polyline_str, index)
        lat += lat_change
        lng += lng_change
        result.append((lat / factor, lng / factor))

    # nimiq: this would just reverse the order from (lat, lon) to (lon, lat).
    #  I don't need this, so I commented it out.
    # if geojson is True:
    #     result = [t[::-1] for t in result]

    return tuple(result)


def compute_euclidean_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Compute the Euclidean distance (flat-earth distance) in km between two points on
     Earth (specified in decimal degrees). It's a gross approximation that assumes a
     flat-Earth surface and works well for distances <100km. For longer distances use
     compute_great_circle_distance().

    Theory: https://en.wikipedia.org/wiki/Euclidean_distance
            https://en.wikipedia.org/wiki/Geographical_distance

    Args: lat and long of the 2 location.
     Examples of lat and long:
       white_house = (38.898, -77.037)
       eiffel_tower = (48.858, 2.294)
       bsas = (-34.83333, -58.5166646)  # Ezeiza Airport (Buenos Aires, Argentina).
       paris = (49.0083899664, 2.53844117956)  # C. de Gaulle Airport (Paris, France).
       newport_ri = (41.49008, -71.312796)
       cleveland_oh = (41.499498, -81.695391)

    Returns (float): distance in km.

    Example:
        import gis_utils
        white_house = (38.898, -77.037)
        eiffel_tower = (48.858, 2.294)
        dist = gis_utils.compute_euclidean_distance(*white_house, *eiffel_tower)
        assert dist == 6454.2071214371235
    """
    # Convert all decimal degrees to radians.
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    avg_lat = (lat1 + lat2) / 2
    x = dlon * cos(avg_lat)
    y = dlat
    r = 6371  # Avg radius of Earth in km.

    # Use the Pythagorean theorem to find the straight-line distance.
    return r * sqrt(x**2 + y**2)


def compute_great_circle_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Compute the great circle distance in km between two points on Earth (specified in
     decimal degrees). It uses the Haversine formula. It's an approximation, but quite
     precise. For an even more precise approximation use:
     https://en.wikipedia.org/wiki/Geodesics_on_an_ellipsoid
     which is included in geopy, see: https://github.com/geopy/geopy?tab=readme-ov-file#measuring-distance.

    Source: https://stackoverflow.com/a/4913653/1969672
    Theory: https://en.wikipedia.org/wiki/Haversine_formula

    Args: lat and long of the 2 location.
     Examples of lat and long:
       white_house = (38.898, -77.037)
       eiffel_tower = (48.858, 2.294)
       bsas = (-34.83333, -58.5166646)  # Ezeiza Airport (Buenos Aires, Argentina).
       paris = (49.0083899664, 2.53844117956)  # C. de Gaulle Airport (Paris, France).
       newport_ri = (41.49008, -71.312796)
       cleveland_oh = (41.499498, -81.695391)

    Returns (float): distance in km.

    Example:
        import gis_utils
        white_house = (38.898, -77.037)
        eiffel_tower = (48.858, 2.294)
        dist = gis_utils.compute_great_circle_distance(*white_house, *eiffel_tower)
        assert dist == 6161.438034825137
    """
    # Convert all decimal degrees to radians.
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula.
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Avg radius of Earth in km.
    return c * r
