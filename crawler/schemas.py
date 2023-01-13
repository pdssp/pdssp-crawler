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
    ssys_solar_longitude: Optional[float] = Field(alias='ssys:solar_longitude')
    ssys_solar_distance: Optional[float] = Field(alias='ssys:solar_distance')
    ssys_incidence_angle: Optional[float] = Field(alias='ssys:incidence_angle')
    ssys_emission_angle: Optional[float] = Field(alias='ssys:emission_angle')
    ssys_phase_angle: Optional[float] = Field(alias='ssys:phase_angle')
    # ssys_spatial_resolution: Optional[float] = Field(alias='ssys:spatial_resolution')
    # ssys_processing_level: Optional[str] = Field(alias='ssys:processing_level')
    # ssys_product_type: Optional[str] = Field(alias='ssys:product_type')

class PDSSP_STAC_Processing_Properties(BaseModel):
    processing_expression: Optional[object] = Field(alias='processing:expression')
    processing_lineage: Optional[str] = Field(alias='processing:lineage')
    processing_level: Optional[str] = Field(alias='processing:level')
    processing_facility: Optional[str] = Field(alias='processing:facility')
    processing_software: Optional[dict] = Field(alias='processing:software')

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
    """Product version."""

    Observation_id: Optional[str]
    """Identifies a scientific observation within a data set."""

    Observation_number: Optional[str]
    """Monotonically increasing ordinal counter of the EDRs generated for a particular OBSERVATION_ID."""

    Observation_type: Optional[str]
    """Identifies the general type of an observation."""

    Producer_id: Optional[str]
    """Producer id."""

    Producer_name: Optional[str]
    """Producer name."""

    Product_release_date: Optional[str]
    """Product release date."""

    Activity_id: Optional[str]
    """Label Activity id"""

    Predicted_dust_opacity: Optional[str]
    """Predicted dust opacity."""

    Predicted_dust_opacity_text: Optional[str]
    """Predicted dust opacity text."""

    Observation_time: Optional[str]
    """Observation time (mid-point between the start and end of the observation)."""

    SpaceCraft_clock_start_count: Optional[str]
    """Spacecraft clock start."""

    SpaceCraft_clock_stop_count: Optional[str]
    """Spacecraft clock stop."""

    Stop_orbit_number: Optional[str]
    """Stop orbit number."""

    UTC_start_time: str  # defined as mandatory for all observational data products
    """Observation start time in UTC."""

    UTC_stop_time: str  # defined as mandatory for all observational data products
    """Observation stop time in UTC."""

    Emission_angle: Optional[float]
    """Emission angle."""

    Emission_angle_text: Optional[str]
    """Emission angle text from the product label."""

    Phase_angle: Optional[float]
    """Phase angle."""

    Phase_angle_text: Optional[float]
    """Phase angle text from the product label."""

    Incidence_angle: Optional[float]
    """Incidence angle."""

    Incidence_angle_text: Optional[float]
    """Incidence angle text from the product label."""

    Map_resolution: Optional[float]
    """Map resolution."""

    Map_resolution_text: Optional[float]
    """Map resolution text from the product label."""

    Map_scale: Optional[float]
    """Map scale."""

    Map_scale_text: Optional[float]
    """Map scale text from the product label."""

    Solar_distance: Optional[float]
    """Solar distance."""

    Solar_distance_text: Optional[float]
    """Solar distance text from the product label."""

    Solar_longitude: Optional[float]
    """Solar longitude."""

    Center_georeferenced: Optional[str]
    """T if the product has a footprint center."""

    Center_latitude: Optional[str]
    """Planetocentric footprint center latitude."""

    Center_longitude: Optional[str]
    """Longitude 0-360 center longitude."""

    Center_latitude_text: Optional[str]
    """Text found in the center latitude label keyword if the center latitude is not a valid number."""

    Center_longitude_text: Optional[str]
    """Text found in the center longitude label keyword if the center longitude is not a valid number."""

    BB_georeferenced: Optional[str]
    """T if the product has a footprint bounding box."""

    Easternmost_longitude: Optional[str]
    """Longitude 0-360 Easternmost longitude of the footprint."""

    Maximum_latitude: Optional[str]
    """Planetocentric maximum latitude of the footprint."""

    Minimum_latitude: Optional[str]
    """Planetocentric minimum latitude of the footprint."""

    Westernmost_longitude: Optional[str]
    """Longitude 0-360 Westernmost longitude of the footprint."""

    Easternmost_longitude_text: Optional[str]
    """Text found in the easternmost longitude label keyword if the easternmost longitude is not a valid number."""

    Maximum_latitude_text: Optional[str]
    """Text found in the maximum latitude label keyword if the maximum latitude is not a valid number."""

    Minimum_latitude_text: Optional[str]
    """Text found in the minimum latitude label keyword if the minimum latitude is not a valid number."""

    Westernmost_longitude_text: Optional[str]
    """Text found in the westernmost longitude label keyword if the westernmost longitude is not a valid number."""

    Footprint_geometry: Optional[str]
    """Cylindrical projected planetocentric, longitude 0-360 product footprint in WKT format. Only if there is
     a valid footprint. Note - this is a cylindrical projected footprint. The footprint has been split into multiple
     polygons when crossing the 0/360 longitude line and any footprints that cross the poles have been adjusted to add
     points to and around the pole. It is meant for use in cylindrical projects and is not appropriate for spherical
     displays."""

    Footprint_C0_geometry: Optional[str]
    """Planetocentric, longitude -180-180 product footprint in WKT format. Only if there is a valid footprint. Note -
    this is a cylindrical projected footprint. The footprint has been split into multiple polygons when crossing the
    -180/180 longitude line and any footprints that cross the poles have been adjusted to add points to and around the
    pole. It is meant for use in cylindrical projects and is not appropriate for spherical displays."""

    Footprint_GL_geometry: Optional[str]
    """Planetocentric, longitude 0-360 product footprint in WKT format. Only if there is a valid footprint. This is
    not a projected footprint."""

    Footprint_NP_geometry: Optional[str]
    """Stereographic south polar projected footprint in WKT format. Only if there is a valid footprint. This footprint
    has been projected into meters in stereographic north polar projection."""

    Footprint_SP_geometry: Optional[str]
    """Stereographic south polar projected footprint in WKT format. Only if there is a valid footprint. This footprint
    has been projected into meters in stereographic south polar projection."""

    Footprints_cross_meridian: Optional[str]
    """T if the footprint crosses the 0/360 longitude line (anti-meridian)."""

    Pole_state: Optional[str]
    """String of "none", "north", or "south"."""

    Footprint_souce: Optional[str]
    """A brief description of where the footprint came from."""

    # USGS_Sites

    Comment: Optional[str]
    """Any associated comment."""

    Description: Optional[str]
    """Label description"""

    # ODE_notes

    External_url: Optional[str]
    """URL to an external reference to the product. Product type specific but usually something like the HiRISE site."""

    External_url2: Optional[str]
    """URL to an external reference to the product. Product type specific but usually something like the HiRISE site."""

    External_url3: Optional[str]
    """URL to an external reference to the product. Product type specific but usually something like the HiRISE site."""

    FilesURL: Optional[str]
    """"""

    ProductURL: Optional[str]
    """"""

    LabelURL: Optional[str]
    """"""

    Product_files: PDSODE_Product_file_key
    """Associated product files."""

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
    """Create a collection or item metadata object from an input metadata dictionary and schema name.
    """
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
"""Mapping of netadata schemas and their corresponding ``"collection"`` and ``"item"`` classes."""