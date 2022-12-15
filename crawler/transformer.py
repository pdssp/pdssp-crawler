"""Transformator module."""

# import
from pydantic import BaseModel
from typing import Dict, List, Union, Optional

import crawler.schemas as schemas
from .extractor import Extractor
from .datastore import SourceCollectionModel

from pathlib import Path

import shapely.wkt
from datetime import datetime

import pystac


def Transformer(collection: SourceCollectionModel = None, source_schema=None, destination_schema='PDSSP_STAC'):
    """Transformer function serving as Transformer objects factory.
    """
    # set source_schema_str
    if collection:
        source_schema_str = collection.source_schema
    elif source_schema:
        source_schema_str = source_schema
    else:
        raise ValueError(
            'At least one of the `service_type` (str) or `service` (Service) keyword argument is required as input.')

    # check that source_schema is valid and create corresponding Transformer object.
    if source_schema_str in SOURCE_TRANSFORMERS.keys():
        TransformerClass = SOURCE_TRANSFORMERS[source_schema_str]
        transformer = TransformerClass(collection=collection, source_schema=source_schema,
                                       destination_schema=destination_schema)
        return transformer


class TransformerSchemaInputError(Exception):
    """Custom error that is raised when invalid schema name is passed.
    """

    def __int__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidModelObjectTypeError(Exception):
    """Custom error that is raised when invalid STAC object type is passed.
    """

    def __int__(self, object_type: str) -> None:
        self.object_type = object_type
        self.message = f"Invalid `{object_type}` type. Allowed object type: 'collection' or 'item'."
        super().__init__(self.message)


class AbstractTransformer:
    def __init__(self, collection=None, source_schema=None, destination_schema='PDSSP_STAC'):
        # automatically set extractor service type from inheriting Extractor class.
        self.source_schema = None
        class_name = self.__class__.__name__
        for schema_name in SOURCE_TRANSFORMERS.keys():
            if class_name == SOURCE_TRANSFORMERS[schema_name].__name__:
                self.schema_name = schema_name

        # if source_schema not in SOURCE_TRANSFORMERS.keys():
        #     raise TransformerSchemaInputError(value=source_schema, message=f'Allowed schema names: {list(SOURCE_TRANSFORMERS.keys())}')

        # init transformer properties
        self.destination_schema = destination_schema
        self.collection = None
        self.transformed = False
        self.stac_dir = ''

        # set source_schema and collection properties
        if source_schema and not collection:
            self.set_source_schema(source_schema)
        elif collection and not source_schema:
            self.set_source_collection(collection)
        else:
            raise ValueError('Only one of the `source_schema` or `collection` input keyword arguments can be used.')

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}> "
            f"source_schema: {self.source_schema} | "
            f"destination_schema: {self.destination_schema} | "
            f"transformed: {self.transformed} | "
            f"stac_dir: {self.stac_dir}"
        )

    def set_source_schema(self, source_schema):
        # check that input source metadata matches with the transformer metadata schema.
        if source_schema == self.source_schema:
            # check that a schema is defined for the input source schema.
            schema_names = schemas.get_schema_names()
            if source_schema in schemas.get_schema_names():
                self.source_schema = source_schema
            else:
                raise ValueError(
                    f'There is no schema defined for input `{source_schema}`. Defined schemas are: {schema_names}')
        else:
            raise ValueError(f'Input `{source_schema}` does not match any Transformer source schema.')

    def set_source_collection(self, collection: SourceCollectionModel):
        """Set transformed source collection from input SourceCollectionModel object and derive Transfornmer properties from it.
        """
        # set extract collection
        self.collection = collection

        # set source metadata
        self.source_schema = collection.source_schema

        # set output STAC file path
        self.stac_dir = collection.stac_dir

    def get_id(self, source_metadata: BaseModel, object_type='item') -> str:
        pass

    def get_stac_version(self) -> str:
        return schemas.STAC_VERSION

    def get_links(self, source_metadata: BaseModel, object_type='item') -> list[BaseModel]:
        pass

    def get_assets(self, source_metadata: BaseModel, object_type='item') -> Dict[str, schemas.PDSSP_STAC_Asset]:
        return {}

    def get_stac_extensions(self, source_metadata: BaseModel) -> list[str]: # collection only
        pass

    def get_title(self, source_metadata: BaseModel) -> str:
        pass

    def get_description(self, source_metadata: BaseModel) -> str:
        pass

    def get_keywords(self, source_metadata: BaseModel) -> list[str]:
        pass

    def get_geometry(self, source_metadata: BaseModel) -> list[BaseModel]:  # GeoJSON Geometry ??
        pass

    def get_extent(self, source_metadata: BaseModel) -> list[BaseModel]:
        pass

    def get_bbox(self, source_metadata: BaseModel) -> list[float]:
        pass

    def get_providers(self, source_metadata: BaseModel) -> list[BaseModel]:
        pass

    def get_licence(self, source_metadata: BaseModel) -> str:
        return 'Default CC-BY-SA-4.0 license [TBC]'

    def get_summaries(self, source_metadata: BaseModel) -> dict:
        pass

    def get_properties(self, source_metadata: BaseModel) -> BaseModel:  # PDSSP_STAC_Properties
        pass

    def get_extension_properties(self, source_metadata: BaseModel, stac_extension, object_type='item') -> BaseModel:
        if stac_extension == 'ssys':
            return self.get_ssys_properties(source_metadata, object_type=object_type)
        elif stac_extension == 'proj':
            return self.get_proj_properties(source_metadata, object_type=object_type)
        else:
            raise Exception(f'Undefined {stac_extension} STAC extension.')

    def get_extension_fields(self, source_metadata: BaseModel, stac_extension, object_type='item') -> BaseModel:
        if stac_extension == 'ssys':
            return self.get_ssys_fields(source_metadata, object_type=object_type)
        elif stac_extension == 'proj':
            return self.get_proj_fields(source_metadata, object_type=object_type)
        else:
            raise Exception(f'Undefined {stac_extension} STAC extension.')

    def get_ssys_properties(self, source_metadata: BaseModel, object_type='item') -> BaseModel:
        if object_type == 'item':
            return {}
        elif object_type == 'collection':
            return {}
        else:
            raise InvalidModelObjectTypeError(object_type)

    def get_ssys_fields(self, source_metadata: BaseModel, object_type='item') -> dict:
        return {}

    def get_proj_properties(self, source_metadata: BaseModel, object_type='item') -> BaseModel:
        if object_type == 'item':
            pass
        elif object_type == 'collection':
            pass
        else:
            raise InvalidModelObjectTypeError(object_type)

    def get_stac_collection_dict(self, source_metadata, stac_extensions=[]) -> dict:
        if not stac_extensions:
            stac_extensions = self.get_stac_extensions(source_metadata)  # from collection metadata, retrieved from collection service `extra_params` JSON attribute.

        stac_collection_dict = {
            'type': 'Collection',  # REQUIRED
            'stac_version': self.get_stac_version(),  # REQUIRED
            'stac_extensions': stac_extensions,
            'id': self.get_id(source_metadata, object_type='collection'),  # REQUIRED
            'title': self.get_title(source_metadata),
            'description': self.get_description(source_metadata),  # REQUIRED
            'keywords': self.get_keywords(source_metadata),
            'licence': self.get_licence(source_metadata),  # REQUIRED
            'providers': self.get_providers(source_metadata),
            'extent': self.get_extent(source_metadata),  # REQUIRED
            'summaries': self.get_summaries(source_metadata),  # STRONGLY RECOMMENDED
            'links': self.get_links(source_metadata, object_type='collection'),  # REQUIRED
            'assets': self.get_assets(source_metadata, object_type='collection'),
            'extra_fields': {}
        }
        for stac_extension in stac_extensions:
            stac_collection_dict['extra_fields'].update(self.get_extension_fields(source_metadata, stac_extension, object_type='collection'))
            # For example:
            # { 'ssys_targets': ['Mars'] }
        return stac_collection_dict

    def get_stac_item_dict(self, source_metadata, stac_extensions=[]) -> dict:
        stac_item_dict = {
            'type': 'Feature',  # REQUIRED
            'stac_version': self.get_stac_version(),  # REQUIRED
            'stac_extensions': stac_extensions,
            'id': self.get_id(source_metadata, object_type='item'),  # REQUIRED
            'geometry': self.get_geometry(source_metadata),  # REQUIRED
            'bbox': self.get_bbox(source_metadata),  # REQUIRED
            'properties': self.get_properties(source_metadata, stac_extensions=stac_extensions),  # REQUIRED
            'links': self.get_links(source_metadata, object_type='item'),  # REQUIRED
            'assets': self.get_assets(source_metadata, object_type='item'),  # REQUIRED
            'collection': '',
            'extra_fields': {}
        }
        # add STAC extensions extra fields
        for stac_extension in stac_extensions:
            stac_item_dict['extra_fields'].update(self.get_extension_fields(source_metadata, stac_extension, object_type='item'))

        return stac_item_dict

    def transform_source_metadata(self, source_metadata: BaseModel, object_type='item', stac_extensions=[]) -> Union[schemas.PDSSP_STAC_Item, schemas.PDSSP_STAC_Collection]:
        """Transform input source metadata into output PDSSP STAC metadata schema object.
        """
        # TODO: `object_type` should be derived from the `source_metadata` object class.
        if object_type == 'item':
            stac_dict = self.get_stac_item_dict(source_metadata, stac_extensions=stac_extensions)
        elif object_type == 'collection':
            stac_dict = self.get_stac_collection_dict(source_metadata, stac_extensions=stac_extensions)
        else:
            raise InvalidModelObjectTypeError(object_type)

        # Attempt to create destination STAC metadata object
        # print(stac_dict)
        stac_metadata = schemas.create_schema_object(stac_dict, self.destination_schema, object_type)
        # print(stac_metadata)
        # print()

        return stac_metadata

    def transform(self, source_collection_file_path='', output_dir_path='', stac_extensions=[], overwrite=False) -> None:
        """Transform (extracted) source collection files into PDSSP STAC catalog.

        Destination STAC catalog may contain one or several collections, related to only one reference target.
        """
        # TODO: Some methods currently require a source collection model object.
        #   - properly implement this,
        #   - implement `source_collection_file_path` and `output_dir_path`.

        # set destination STAC catalog path, based on source collection related target.
        if not output_dir_path:
            output_dir_path = self.stac_dir
        stac_catalog_dirpath = Path(output_dir_path, self.collection.target.lower())

        # set destination STAC catalog file
        stac_catalog_filepath = Path(stac_catalog_dirpath, 'catalog.json')

        # if destination STAC catalog file exists, create catalog STAC object from file.
        if Path.is_file(stac_catalog_filepath):
            stac_catalog = pystac.Catalog.from_file(str(stac_catalog_filepath))
        else:
            # else create STAC catalog from scratch.
            stac_catalog = pystac.Catalog(
                id=f'pdssp-{self.collection.target.lower()}-catalog',
                title=f'{self.collection.target.title()} STAC Catalog holding one or several PDSSP-compliant data products collections.',
                description=f'This catalog was generated by the PDSSSP Crawler on {datetime.utcnow()}.',
                stac_extensions=['ssys'],
                extra_fields={'ssys:targets': [self.collection.target.upper()]}
            )

        # check that input source collection haven't been transformed and exists in destination STAC catalog.
        stac_catalog_collections = stac_catalog.get_all_collections()
        for stac_catalog_collection in stac_catalog_collections:
            if stac_catalog_collection.id == self.collection.collection_id:
                if overwrite:
                    # remove destination STAC catalog collection
                    print(f'removing child: {self.collection.collection_id}')
                    stac_catalog.remove_child(self.collection.collection_id)
                else:
                    raise Exception(f'{stac_catalog.id} destination STAC catalog already hold a collection with the {self.collection.collection_id} collection ID.')


        # set extractor
        extractor = Extractor(self.collection)

        # read and transform source collection metadata, into destination `PDSSP_STAC_Collection` metadata.
        source_collection_metadata = extractor.read_collection_metadata()
        stac_collection_metadata = self.transform_source_metadata(source_collection_metadata, object_type='collection', stac_extensions=stac_extensions)

        # create destination PySTAC Collection object
        #
        # set STAC collection ID
        stac_collection_id = stac_collection_metadata.id

        # set empty collection spatial and temporal extent
        # stac_extent = pystac.Extent(
        #     pystac.SpatialExtent(bboxes=stac_collection_metadata.extent.spatial.bbox),
        #     pystac.TemporalExtent(intervals=stac_collection_metadata.extent.temporal.interval)
        # )
        stac_extent = pystac.Extent(pystac.SpatialExtent(bboxes=[[]]), pystac.TemporalExtent(intervals=[[]]))

        # set STAC collection and items extensions
        if not stac_extensions:
            stac_extensions = stac_collection_metadata.stac_extensions

        stac_collection = pystac.Collection(
            id=stac_collection_id,
            stac_extensions=stac_extensions,
            title=stac_collection_metadata.title,
            description=stac_collection_metadata.description,
            extent=stac_extent,
            license=stac_collection_metadata.licence,
            extra_fields=stac_collection_metadata.extra_fields  # {'ssys:targets': 'MARS'}
        )

        # read and transform source collection products metadata, into destination `PDSSP_STAC_Item` metadata, then
        # create and add the corresponding PySTAC Item object to the PySTAC Collection.
        #
        while extractor.file_idx < extractor.n_extracted_files:  # TODO: improve mechanism to loop over all products.
            source_product_metadata = extractor.read_product_metadata()
            stac_item_metadata = self.transform_source_metadata(source_product_metadata, object_type='item', stac_extensions=stac_extensions)

            print(stac_item_metadata.properties['datetime'])
            # create PySTAC Item
            stac_item = pystac.Item(
                id=stac_item_metadata.id,
                stac_extensions=stac_extensions,
                geometry=stac_item_metadata.geometry,
                bbox=stac_item_metadata.bbox,
                datetime=datetime.fromisoformat(stac_item_metadata.properties['datetime']),
                properties=stac_item_metadata.properties,  # .dict(exclude_unset=True), # include={'datetime', 'platform', 'start_datetime'}),
                # assets=stac_assets,
                extra_fields=stac_item_metadata.extra_fields,  # {'ssys:targets': stac_item_metadata.ssys_targets},
                collection=stac_collection_id
            )

            # add assets to pySTAC item
            for key in stac_item_metadata.assets:
                asset_metadata = stac_item_metadata.assets[key]
                stac_item.add_asset(
                    key=key,
                    asset=pystac.Asset(
                        href=asset_metadata.href,
                        title=asset_metadata.title,
                        description=asset_metadata.description,
                        media_type=asset_metadata.type,
                        roles=asset_metadata.roles
                    )
                )
            # add item to PySTAC Collection
            stac_collection.add_item(stac_item)

        # update collection extent from items
        stac_collection.update_extent_from_items()

        # add collection to the output STAC catalog
        stac_catalog.add_child(stac_collection)

        # save STAC catalog files
        print(f'Writing STAC JSON files in {stac_catalog_dirpath} directory...')
        Path.mkdir(stac_catalog_dirpath, parents=True, exist_ok=overwrite)
        stac_catalog.normalize_hrefs(str(stac_catalog_dirpath))
        stac_catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

        # set transformer status attributes
        self.transformed = True
        self.stac_dir = stac_catalog_dirpath

    def _geometry_from_wkt(self, wkt):
        pass


class PDSODE_STAC(AbstractTransformer):
    def __init__(self, collection=None, source_schema=None, destination_schema='PDSSP_STAC'):
        super().__init__(collection=collection, source_schema=source_schema, destination_schema=destination_schema)

    def get_id(self, source_metadata: BaseModel, object_type='item') -> str:
        if object_type == 'item':
            return source_metadata.pdsid
        elif object_type == 'collection':
            return f'{source_metadata.iiptset.IHID}_{source_metadata.iiptset.IID}_{source_metadata.iiptset.PT}'
        else:
            raise InvalidModelObjectTypeError(object_type)

    #
    # def get_links(self, source_metadata: BaseModel, object_type='item') -> list[BaseModel]:
    #     pass

    def get_assets(self, source_metadata: BaseModel, object_type='item') -> Dict[str, schemas.PDSSP_STAC_Asset]:
        if object_type == 'item':
            assets = {}
            for product_file in source_metadata.Product_files.Product_file:
                # set PDSSP_STAC_Asset object input arguments
                href = product_file.URL
                title = product_file.FileName
                description = product_file.Description
                media_type = ''
                roles = []
                ext = product_file.FileName.split('.')[-1].upper()
                if ext == 'LBL':
                    media_type = 'text/plain'
                    roles = ['metadata']
                elif ext == 'JP2':
                    media_type = 'image/jp2'
                    roles = ['data']
                elif ext == 'PNG':
                    media_type = 'image/png'
                elif ext == 'JPG' or ext == 'JPEG':
                    media_type = 'image/jpeg'

                if product_file.Type == 'Product':
                    roles = ['data']
                elif product_file.Type == 'Browse':
                    roles = ['thumbnail']
                else:
                    roles = [product_file.Type]

                # create PDSSP_STAC_Asset object
                asset = schemas.PDSSP_STAC_Asset(
                    href=href,
                    title=title,
                    description=description,
                    media_type=media_type,
                    roles=roles
                )

                # add PDSSP_STAC_Asset object to assets dictionary
                key = title
                assets.update({key: asset})

            return assets
        elif object_type == 'collection':
            return []
        else:
            raise InvalidModelObjectTypeError(object_type)

    def get_stac_extensions(self, source_metadata: BaseModel) -> list[str]: # for PDSODE collection metadata only
        return source_metadata.stac_extensions

    def get_title(self, source_metadata: BaseModel) -> str:
        title = f'{source_metadata.iiptset.IHID}/{source_metadata.iiptset.IID} {source_metadata.iiptset.PTName}'
        return title

    def get_description(self, source_metadata: BaseModel) -> str:
        description = f'Collection of {source_metadata.iiptset.IHID}/{source_metadata.iiptset.IID}/{source_metadata.iiptset.PT} ({source_metadata.iiptset.PTName})  PDS data products.'
        return description

    def get_keywords(self, source_metadata: BaseModel) -> list[str]:
        pass

    def get_geometry(self, source_metadata: BaseModel) -> list[BaseModel]:  # GeoJSON Geometry ??
        footprint_wkt = source_metadata.Footprint_C0_geometry
        if not footprint_wkt:
            return None
        footprint_shape = shapely.wkt.loads(footprint_wkt)
        footprint_bbox = list(footprint_shape.bounds)
        footprint_geometry = shapely.geometry.mapping(footprint_shape)
        return footprint_geometry

    def get_extent(self, source_metadata: BaseModel) -> schemas.PDSSP_STAC_Extent:
        collection_extent = schemas.PDSSP_STAC_Extent(
            spatial=schemas.PDSSP_STAC_SpatialExtent(bbox=[[]]),
            temporal=schemas.PDSSP_STAC_TemporalExtent(interval=[[]])
        )
        return collection_extent

    def get_bbox(self, source_metadata: BaseModel) -> list[float]:
        footprint_wkt = source_metadata.Footprint_C0_geometry
        if not footprint_wkt:
            return None
        footprint_shape = shapely.wkt.loads(footprint_wkt)
        footprint_bbox = list(footprint_shape.bounds)
        return footprint_bbox

    def get_providers(self, source_metadata: BaseModel) -> list[BaseModel]:
        name = f'{source_metadata.iiptset.IID} team via PDS ODE'
        providers = [schemas.PDSSP_STAC_Provider(name=name)]
        return providers

    def get_licence(self, source_metadata: BaseModel) -> str:
        return 'Default CC-BY-SA-4.0 license for PDS ODE collections [TBC]'

    def get_summaries(self, source_metadata: BaseModel) -> dict:
        pass

    def get_properties(self, source_metadata: BaseModel, stac_extensions=['ssys']) -> dict:
        datetime_format = '%Y-%m-%dT%H:%M:%S.%f'
        properties = schemas.PDSSP_STAC_Properties(
            datetime=datetime.strptime(source_metadata.UTC_start_time, datetime_format).isoformat(timespec='milliseconds'),
            created=datetime.strptime(source_metadata.Product_creation_time, datetime_format).isoformat(),
            start_datetime=datetime.strptime(source_metadata.UTC_start_time, datetime_format).isoformat(),
            end_datetime=datetime.strptime(source_metadata.UTC_stop_time, datetime_format).isoformat(),
            platform=source_metadata.ihid,
            instruments=[source_metadata.iid]
        )
        properties_dict = properties.dict(exclude_unset=True)
        for stac_extension in stac_extensions:
            properties_dict.update(self.get_extension_properties(source_metadata, stac_extension, object_type='item'))

        return properties_dict

    def get_ssys_properties(self, source_metadata: BaseModel, object_type='item') -> dict:
        if object_type == 'item':
            ssys_properties = schemas.PDSSP_STAC_SSYS_Properties(**{'ssys:targets':[source_metadata.Target_name.upper()]})
        elif object_type == 'collection':
            ssys_properties = schemas.PDSSP_STAC_SSYS_Properties(**{'ssys:targets':[source_metadata.iiptset.ODEMetaDB.upper()]})
        else:
            raise InvalidModelObjectTypeError(object_type)
        return ssys_properties.dict(by_alias=True)

    def get_ssys_fields(self, source_metadata: BaseModel, object_type='item') -> dict:
        if object_type == 'item':
            ssys_fields = {}
        elif object_type == 'collection':
            ssys_fields = { 'ssys:targets': source_metadata.iiptset.ODEMetaDB.upper() }
        else:
            raise InvalidModelObjectTypeError(object_type)
        return ssys_fields

    def get_proj_properties(self, source_metadata: BaseModel, object_type='item') -> dict:
        if object_type == 'item':
            pass
        elif object_type == 'collection':
            pass
        else:
            raise InvalidModelObjectTypeError(object_type)


class EPNTAP_STAC(AbstractTransformer):
    def __init__(self, collection=None, source_schema=None, destination_schema='PDSSP_STAC'):
        super().__init__(collection=collection, source_schema=source_schema, destination_schema=destination_schema)

    def get_id(self, source_metadata: BaseModel, object_type='item') -> str:
        if object_type == 'item':
            return source_metadata.granule_uid
        elif object_type == 'collection':
            return source_metadata.collection_id  # not defined yet in schema
        else:
            raise InvalidModelObjectTypeError(object_type)

    # def get_stac_extensions(self, source_metadata: BaseModel, object_type='item') -> list[str]:
    #     pass

    def get_links(self, source_metadata: BaseModel, object_type='item') -> list[BaseModel]:
        pass

    def get_assets(self, source_metadata: BaseModel, object_type='item') -> list[BaseModel]:
        pass

    def get_title(self, source_metadata: BaseModel) -> str:
        pass

    def get_description(self, source_metadata: BaseModel) -> str:
        pass

    def get_keywords(self, source_metadata: BaseModel) -> list[str]:
        pass

    def get_geometry(self, source_metadata: BaseModel) -> list[BaseModel]:  # GeoJSON Geometry ??
        return self._geometry_from_wkt(source_metadata.s_region)

    def get_extent(self, source_metadata: BaseModel) -> list[BaseModel]:
        pass

    def get_bbox(self, source_metadata: BaseModel) -> list[float]:
        return [source_metadata.c1min, source_metadata.c2min, source_metadata.c1max, source_metadata.c2max]

    def get_summaries(self, source_metadata: BaseModel) -> dict:
        pass

    def get_properties(self, source_metadata: BaseModel) -> BaseModel:  # PDSSP_STAC_Properties
        pass

    def get_providers(self, source_metadata: BaseModel) -> list[BaseModel]:
        pass

    def get_licence(self, source_metadata: BaseModel) -> str:
        pass

    def get_collection(self, source_metadata: BaseModel) -> str:
        pass


class MARSSI_STAC(AbstractTransformer):
    def __init__(self, collection=None, source_schema=None, destination_schema='PDSSP_STAC'):
        super().__init__(collection=collection, source_schema=source_schema, destination_schema=destination_schema)

    def get_id(self, source_metadata: BaseModel, object_type='item') -> str:
        pass

    def get_stac_extensions(self, source_metadata: BaseModel, object_type='item') -> list[str]:
        pass

    def get_links(self, source_metadata: BaseModel, object_type='item') -> list[BaseModel]:
        pass

    def get_assets(self, source_metadata: BaseModel, object_type='item') -> list[BaseModel]:
        pass

    def get_title(self, source_metadata: BaseModel) -> str:
        pass

    def get_description(self, source_metadata: BaseModel) -> str:
        pass

    def get_keywords(self, source_metadata: BaseModel) -> list[str]:
        pass

    def get_geometry(self, source_metadata: BaseModel) -> list[BaseModel]:  # GeoJSON Geometry ??
        pass

    def get_extent(self, source_metadata: BaseModel) -> list[BaseModel]:
        pass

    def get_bbox(self, source_metadata: BaseModel) -> list[float]:
        pass

    def get_summaries(self, source_metadata: BaseModel) -> dict:
        pass

    def get_properties(self, source_metadata: BaseModel) -> BaseModel:  # PDSSP_STAC_Properties
        pass

    def get_providers(self, source_metadata: BaseModel) -> list[BaseModel]:
        pass

    def get_licence(self, source_metadata: BaseModel) -> str:
        pass

    def get_collection(self, source_metadata: BaseModel) -> str:
        pass


SOURCE_TRANSFORMERS = {
    'PDSODE': PDSODE_STAC,
    'EPNTAP': EPNTAP_STAC,
    'MARSSI_WFS': MARSSI_STAC
}
