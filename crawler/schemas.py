"""Schemas module for the definition and retrieval of ``"collection"`` and ``"item"``-type metadata dictionary
compliant to the following schemas/models:

==============  ===============================================  ============================================
Schema          Collection metadata                              Item metadata
==============  ===============================================  ============================================
``PDSSP_STAC``  :class:`crawler.schemas.PDSSP_STAC_Collection`   :class:`crawler.schemas.PDSSP_STAC_Item`
``PDSSP_WFS``   :class:`crawler.schemas.PDSSP_WFS_Layer`         :class:`crawler.schemas.PDSSP_WFS_Feature`
``PDSODE``      :class:`crawler.schemas.PDSODE_IIPTSet`          :class:`crawler.schemas.PDSODE_Product`
``EPNTAP``      :class:`crawler.schemas.EPNTAP_Collection`       :class:`crawler.schemas.EPNTAP_Granule`
``MARSSI_WFS``  :class:`crawler.schemas.MARSSI_WFS_Layer`        :class:`crawler.schemas.MARSSI_WFS_Feature`
==============  ===============================================  ============================================

References/examples:

- https://github.com/radiantearth/stac-spec/blob/master/item-spec
- https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md
- https://github.com/ivoa-std/EPNTAP/blob/master/example-record.xml
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Union, Optional
# from datetime import datetime

STAC_VERSION = '1.0.0'

# PDSSP_STAC -> "proxy" schema to STAC model

class PDSSP_STAC_SpatialExtent(BaseModel):
    bbox: list[list[float]]
    """Potential spatial extents covered by the Collection."""

class PDSSP_STAC_TemporalExtent(BaseModel):
    interval: list[list[str]]
    """Potential temporal extents covered by the Collection."""

class PDSSP_STAC_Extent(BaseModel):
    spatial: PDSSP_STAC_SpatialExtent
    """Potential spatial extents covered by the Collection."""
    temporal: PDSSP_STAC_TemporalExtent
    """Potential temporal extents covered by the Collection."""

class PDSSP_STAC_Provider(BaseModel):
    name: str
    """The name of the organization or the individual."""
    description: Optional[str]
    """Multi-line description to add further provider information such as processing details for processors and
    producers, hosting details for hosts or basic contact information. CommonMark 0.29 syntax MAY be used for
    rich text representation."""
    roles: Optional[list[str]]
    """Roles of the provider. Any of licensor, producer, processor or host."""

class PDSSP_STAC_Link(BaseModel):
    href: str
    """The actual link in the format of an URL. Relative and absolute links are both allowed."""
    rel: str
    """ Relationship between the current document and the linked document."""
    type: Optional[str]
    """Media type of the referenced entity."""
    title: Optional[str]
    """A human readable title to be used in rendered displays of the link."""

class PDSSP_STAC_Collection(BaseModel):
    type: str
    stac_version: str = STAC_VERSION
    stac_extensions: Optional[list[str]]
    id: str
    title: Optional[str]
    description: str
    keywords: Optional[list[str]]
    licence: str
    providers: Optional[list[PDSSP_STAC_Provider]]
    extent: PDSSP_STAC_Extent
    summaries: Optional[dict]
    links: Optional[list[PDSSP_STAC_Link]]  # WARNING: NOT optional following STAC standard -> created automatically by PySTAC.
    assets: Optional[dict]  ## Map<string, PDSSP_STAC_Asset>: dictionary of asset objects that can be downloaded, each with a unique key
    extra_fields: Optional[dict]

class PDSSP_STAC_Asset(BaseModel):
    href: str
    title: Optional[str]
    description: Optional[str]
    type: Optional[str]
    roles: Optional[list[str]]

class PDSSP_STAC_Properties(BaseModel): # STAC Common Metadata
    title: Optional[str] #
    description: Optional[str]
    datetime: str  # ISO 8601 format
    created: Optional[str]  # ISO 8601 format
    updated: Optional[str]  # ISO 8601 format
    start_datetime: Optional[str]  # ISO 8601 format
    end_datetime: Optional[str]  # ISO 8601 format
    license: Optional[str]
    platform: Optional[str] # PDS instrument_host_id
    instruments: Optional[list[str]] # PDS instrument_id
    constellation: Optional[str]  # ?
    mission: Optional[str]   # PDS mission_id
    gsd: Optional[float]
    # ssys_targets: Optional[list[str]] = Field(None, alias='ssys:targets')
    # ssys_solar_longitude: Optional[float]
    # ssys_instrument_host: Optional[str]

class PDSSP_STAC_Item(BaseModel):
    type: str
    stac_version: str = STAC_VERSION
    stac_extensions: Optional[list[str]]
    id: str
    geometry: object  # GeoJSON Geometry
    bbox: Union[list[float], None]
    properties: dict  # PDSSP_STAC_Properties
    links: Optional[list[PDSSP_STAC_Link]]  # WARNING: NOT optional following STAC standard -> created automatically by PySTAC.
    assets: dict  ## Map<string, PDSSP_STAC_Asset>: dictionary of asset objects that can be downloaded, each with a unique key.
    collection: Optional[str]
    extra_fields: Optional[dict]

class PDSSP_STAC_SSYS_Properties(BaseModel):
    ssys_targets: Optional[list[str]] = Field(alias='ssys:targets')
#     ssys_target_class:
#     ssys_westernmost_longitude: Optional[float]
#     ssys_easternmost_longitude: Optional[float]
#     ssys_instrument_host_name: Optional[str]
#     ssys_instrument_name: Optional[str]

class PDSSP_WFS_Layer(BaseModel):
    pass

class PDSSP_WFS_Feature(BaseModel):
    pass

# PDS ODE Metadata Schemas
#
class PDSODE_ValidTargets(BaseModel):
    ValidTarget: Union[str, list[str]]

class PDSODE_IIPTSet(BaseModel):
    ODEMetaDB: str
    IHID: str
    IHName: str
    IID: str
    IName: str
    PT: str
    PTName: str
    DataSetId: str
    ValidTargets: PDSODE_ValidTargets
    NumberProducts: int

class PDSODE_Collection(BaseModel):
    iiptset: PDSODE_IIPTSet
    stac_extensions: Optional[list[str]]

class PDSODE_Product_file(BaseModel):
    Description: str  # eg" 'MAP PROJECTION FILE'",'
    FileName: str  # "DSMAP.CAT",
    KBytes: str  # "7",
    Type: str  # "Referenced",
    URL: str # "https://hirise.lpl.arizona.edu/PDS/CATALOG/DSMAP.CAT"

class PDSODE_Product_file_key(BaseModel):
    Product_file: list[PDSODE_Product_file]

class PDSODE_Product(BaseModel):
    ode_id: str
    """An internal ODE product identifier."""

    pdsid: str
    """PDS Product Id."""

    ihid: str
    """Instrument host id."""

    iid: str
    """Instrument id."""

    pt: str
    """ODE Product type."""

    Label_Product_Type: Optional[str]
    """Label product type (if it exists in the label and is different from the ODE_Product_Type)."""

    Data_Set_Id: str
    """PDS Data Set Id."""

    PDSVolume_Id: str
    """Volume Id."""

    RelativePathtoVol: str
    """The relative path from the volume root to the product label file."""

    LabelFileName: str
    """The file name of the product label."""

    Product_creation_time: str
    """Product creation time (UTC)."""

    Target_name: str
    """Product target (example: Mars)."""

    Product_version_id: Optional[str]
    """Product version"""

    Observation_id: Optional[str]
    """Identifies a scientific observation within a data set."""

    Product_files: PDSODE_Product_file_key
    """Associated product files."""

    Footprint_C0_geometry: Optional[str]
    UTC_start_time: str
    UTC_stop_time: str
    #
    # "BB_georeferenced": "True",
    # "Center_georeferenced": "True",
    # "Center_latitude": "-14.285",
    # "Center_longitude": "240.051",
    # "Comment": "Pit crater chain south of Arsia Mons",
    # "Data_Set_Id": "MRO-M-HIRISE-3-RDR-V1.1",
    # "Description": "HiRISE projected and mosaicked product  HiRISE RDR V1.1 files has map projection data embedded in the header - please see SIS for more details.",
    # "Easternmost_longitude": "240.114",
    # "Emission_angle": "3.713668",
    # "External_url": "http://www.uahirise.org/ESP_012600_1655",
    # "External_url2": "jpip://hijpip.lpl.arizona.edu:8064/PDS/RDR/ESP/ORB_012600_012699/ESP_012600_1655/ESP_012600_1655_RED.JP2",
    # "FilesURL": "https://ode.rsl.wustl.edu/mars/productfiles.aspx?product_id=ESP_012600_1655_RED&product_idGeo=13005453",
    # "Footprint_C0_geometry": "POLYGON ((-119.886 -14.4381, -119.973 -14.4483, -120.012 -14.132, -119.925 -14.1218, -119.886 -14.4381))",
    # "Footprint_geometry": "POLYGON ((240.114 -14.4381, 240.027 -14.4483, 239.988 -14.132, 240.075 -14.1218, 240.114 -14.4381))",
    # "Footprint_GL_geometry": "POLYGON ((240.114 -14.4381, 240.027 -14.4483, 239.988 -14.132, 240.075 -14.1218, 240.114 -14.4381))",
    # "Footprint_NP_geometry": "MULTIPOLYGON EMPTY",
    # "Footprint_souce": "PDS Archive Index Table",
    # "Footprint_SP_geometry": "MULTIPOLYGON EMPTY",
    # "Footprints_cross_meridian": "False",
    # "ihid": "MRO",
    # "iid": "HIRISE",
    # "Incidence_angle": "49.904166",
    # "LabelFileName": "esp_012600_1655_red.lbl",
    # "LabelURL": "https://hirise.lpl.arizona.edu/PDS/RDR/ESP/ORB_012600_012699/ESP_012600_1655/ESP_012600_1655_RED.LBL",
    # "Map_resolution": "118528.17278819",
    # "Map_scale": "0.5",
    # "Maximum_latitude": "-14.1218",
    # "Minimum_latitude": "-14.4483",
    # "Observation_id": "ESP_012600_1655",
    # "Observation_time": "2009-04-04T07:13:46.356",
    # "ODE_notes": {
    #     "ODE_note": [
    #         "NOTE: Product Type set by ODE",
    #         "NOTE: Label keyword Orbit number value used for start orbit number value",
    #         "NOTE: Label keyword Orbit number value used for stop orbit number value",
    #         "NOTE: Map Resolution set from label map projection object",
    #         "NOTE: Map scale from the label map projection object",
    #         "NOTE: Observation time set to mid-point between start time and stop time",
    #         "NOTE: Index Record:",
    #         "\"MROHR_0001\",\"RDR/ESP/ORB_012600_012699/ESP_012600_1655/ESP_012600_1655_RED.JP2  \",\"MRO\",\"HIRISE\",\"ESP_012600_1655\",\"ESP_012600_1655_RED  \",\"1  \",\"MARS                            \", 12600,\"Extended Science Phase        \",\"Pit crater chain south of Arsia Mons                                       \",\"2009-04-04T07:13:43     \",\"923296444:63762 \",\"2009-04-04T07:13:43     \",\"923296445:06824 \",\"2009-04-04T07:13:49     \",\"923296451:03746 \", 38702, 14754, 3.71414,49.9040, 53.5430, 252.320,3656.72, 252.623,  270.0000,  163.7660,  -21.6699,  187.9300,  -14.2643,  240.3150,   1.38343,   240.167,   15.4747,\"YES\",  -14.4483,  -14.1218,  239.9880,  240.1140, 0.50,118528.000,\"EQUIRECTANGULAR    \",-10.0, 180.000,  -1673830.0,  -7002200.0,  -14.4381,  240.1140,  -14.4483,  240.0270,  -14.1320,  239.9880,  -14.1218,  240.0750",
    #         "NOTE: HIRISE location data updated from index table entry"
    #     ]
    # },
    # "pdsid": "ESP_012600_1655_RED",
    # "PDSVolume_Id": "MROHR_0001",
    # "Phase_angle": "53.549941",
    # "Pole_state": "none",
    # "Producer_id": "UA",
    # "Product_creation_time": "2009-08-18T00:14:05.000",
    # "Product_files": {
    #     "Product_file": [
    #         {
    #             "Description": "MAP PROJECTION FILE",
    #             "FileName": "DSMAP.CAT",
    #             "KBytes": "7",
    #             "Type": "Referenced",
    #             "URL": "https://hirise.lpl.arizona.edu/PDS/CATALOG/DSMAP.CAT"
    #         },
    #
    # "Product_version_id": "1.0",
    # "ProductURL": "https://ode.rsl.wustl.edu/mars/indexproductpage.aspx?product_id=ESP_012600_1655_RED&product_idGeo=13005453",
    # "pt": "RDRV11",
    # "RelativePathtoVol": "rdr\\esp\\orb_012600_012699\\esp_012600_1655\\",
    # "Solar_longitude": "240.166542",
    # "Solar_time": "15.47471",
    # "SpaceCraft_clock_start_count": "923296445:06824",
    # "SpaceCraft_clock_stop_count": "923296451:03746",
    # "Start_orbit_number": "12600",
    # "Stop_orbit_number": "12600",
    # "Target_name": "MARS",
    # "UTC_start_time": "2009-04-04T07:13:43.380",
    # "UTC_stop_time": "2009-04-04T07:13:49.333",
    # "Westernmost_longitude": "239.988"


class EPNTAP_Collection(BaseModel):
    pass

class EPNTAP_Granule(BaseModel):
    granule_uid: str
    granule_gid: str
    obs_id: str
    dataproduct_type: str
    target_name: str
    target_class: str
    time_min: str
    time_max: str
    time_sampling_step_min: str
    time_sampling_step_max: str
    time_exp_min: str
    time_exp_max: str
    spectral_range_min: str
    spectral_range_max: str
    spectral_sampling_step_min: str
    spectral_sampling_step_max: str
    spectral_resolution_min: str
    spectral_resolution_max: str
    c1min: str
    c1max: str
    c2min: str
    c2max: str
    c3min: str
    c3max: str
    s_region: str
    c1_resol_min: str
    c1_resol_max: str
    c2_resol_min: str
    c2_resol_max: str
    c3_resol_min: str
    c3_resol_max: str
    spatial_frame_type: str
    incidence_min: str
    incidence_max: str
    emergence_min: str
    emergence_max: str
    phase_min: str
    phase_max: str
    instrument_host_name: str
    instrument_name: str
    measurement_type: str
    processing_level: str
    creation_date: str
    modification_date: str
    release_date: str
    service_title: str
    access_url: str
    access_format: str
    access_estsize: str
    file_name: str
    publisher: str


class MARSSI_WFS_Layer(BaseModel):
    pass

class MARSSI_WFS_Feature(BaseModel):
    pass


def get_schema_names() -> list[str]:
    schema_names = []
    for name in METADATA_SCHEMAS.keys():
        name += ' ' + str(list(METADATA_SCHEMAS[name].keys()))
        schema_names.append(name)
    return schema_names

def get_schema_json(name: str, object_type: str) -> Optional[BaseModel]:
    """Function serving as Schema objects factory.

    :param name:
    :param object_type: can be 'collection', 'item', or 'catalog', 'asset', 'link' for STAC schemas.
    :return:
    """

    if name in METADATA_SCHEMAS.keys():
        if object_type in METADATA_SCHEMAS[name].keys():
            BaseModelClass = METADATA_SCHEMAS[name][object_type]
            schema_json = BaseModelClass.schema_json(indent=2)  # BaseModelClass()
            return schema_json
        else:
            print(f'No schema defined for `{METADATA_SCHEMAS[name]}` schema `{object_type}` object type.')
            return None
    else:
        print(f'Unknown metadata schema: {name}.')
        return None

def create_schema_object(metadata: dict, name: str, object_type: str) -> Optional[BaseModel]:
    if name in METADATA_SCHEMAS.keys():
        if object_type in METADATA_SCHEMAS[name].keys():
            BaseModelClass = METADATA_SCHEMAS[name][object_type]
            schema_object = BaseModelClass(**metadata)
            return schema_object
        else:
            print(f'No schema defined for `{METADATA_SCHEMAS[name]}` schema `{object_type}` object type.')
            return None
    else:
        print(f'Unknown metadata schema: {name}.')
        return None

METADATA_SCHEMAS = {
    'PDSSP_STAC': {'collection': PDSSP_STAC_Collection, 'item': PDSSP_STAC_Item},
    'PDSSP_WFS': {'collection': PDSSP_WFS_Layer, 'item': PDSSP_WFS_Feature},
    'PDSODE': {'collection': PDSODE_IIPTSet,'item': PDSODE_Product},
    'EPNTAP': {'collection': EPNTAP_Collection,'item': EPNTAP_Granule},
    'MARSSI_WFS': {'collection': MARSSI_WFS_Layer, 'item': MARSSI_WFS_Feature}
}
"""Metadata schemas and their corresponding ``"collection"`` and ``"item"``-type classes."""