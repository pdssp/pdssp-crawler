"""Transformator module."""

# import
from pydantic import BaseModel

from crawler.schemas import get_schema_names, create_schema_object, STAC_VERSION
from .extractor import Extractor
from .datastore import SourceCollectionModel

from pathlib import Path

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
        raise ValueError('At least one of the `service_type` (str) or `service` (Service) keyword argument is required as input.')

    # check that source_schema is valid and create corresponding Transformer object.
    if source_schema_str in SOURCE_TRANSFORMERS.keys():
        TransformerClass = SOURCE_TRANSFORMERS[source_schema_str]
        transformer = TransformerClass(collection=collection, source_schema=source_schema, destination_schema=destination_schema)
        return transformer

class TransformerSchemaInputError(Exception):
    """Custom error that is raised when invalid schema name is passed.
    """
    def __int__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


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
            f"stac_dir: {self.stac_dir}"
        )

    def set_source_schema(self, source_schema):
        # check that input source metadata matches with the transformer metadata schema.
        if source_schema == self.source_schema:
            # check that a schema is defined for the input source schema.
            schema_names = get_schema_names()
            if source_schema in get_schema_names():
                self.source_schema = source_schema
            else:
                raise ValueError(f'There is no schema defined for input `{source_schema}`. Defined schemas are: {schema_names}')
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

    def get_stac_collection_dict(self, source_metadata):
        return {
            'type': 'Collection',  # REQUIRED
            'stac_version': STAC_VERSION,  # REQUIRED
            'stac_extensions': self.get_stac_extensions(source_metadata, object_type='collection'),
            'id': self.get_id(source_metadata, object_type='collection'),  # REQUIRED
            'title': self.get_title(source_metadata),
            'description': self.get_description(source_metadata),  # REQUIRED
            'keywords': self.get_keywords(source_metadata),
            'licence': self.get_licence(source_metadata),  # REQUIRED
            'providers': self.get_providers(source_metadata),
            'extent': self.get_extent(source_metadata),  # REQUIRED
            'summaries': self.get_summaries(source_metadata),  # STRONGLY RECOMMENDED
            'links': self.get_links(source_metadata, object_type='collection'),  # REQUIRED
            'assets': self.get_assets(source_metadata, object_type='collection')
        }

    def get_stac_item_dict(self, source_metadata):
        return {
            'type': 'Item',  # REQUIRED
            'stac_version': STAC_VERSION,  # REQUIRED
            'stac_extensions': self.get_stac_extensions(source_metadata, object_type='item'),
            'id': self.get_id(source_metadata, object_type='item'),  # REQUIRED
            'geometry': self.get_geometry(source_metadata),  # REQUIRED
            'bbox': self.get_bbox(source_metadata),  # REQUIRED
            'properties': self.get_properties(source_metadata),  # REQUIRED
            'links': self.get_links(source_metadata, object_type='item'),  # REQUIRED
            'assets': self.get_assets(source_metadata, object_type='item'),  # REQUIRED
            'collection': self.get_collection(source_metadata)
        }

    def transform_source_metadata(self, source_metadata: BaseModel, object_type='item') -> BaseModel:
        """Transform input source metadata into output PDSSP STAC metadata schema object.
        """
        # TODO: `object_type` should be derived from the `source_metadata` object class.
        stac_item_dict = self.get_stac_item_dict(source_metadata)
        stac_item_metadata = create_schema_object(stac_item_dict, self.destination_schema, object_type)

        return stac_item_metadata

    def transform(self, source_collection_file_path='', stac_dir='', overwrite=False) -> None:
        """Transform (extracted) source collection files into PDSSP STAC catalog.
        """
        # set extractor
        extractor = Extractor(self.collection)
        # TODO: Method currently requires a source collection model object.
        #   `source_collection_file_path` and `stac_dir` must be implemented.

        # read and transform source collection metadata, into destination `PDSSP_STAC_Collection` metadata.
        source_collection_metadata = extractor.read_collection_metadata()
        stac_collection_metadata = self.transform_source_metadata(source_collection_metadata, object_type='collection')

        # create destination PySTAC Collection object
        stac_collection_extent = pystac.Extent(pystac.SpatialExtent(bboxes=[[]]), pystac.TemporalExtent(intervals=[[]]))
        stac_collection = pystac.Collection(id=source_collection_metadata.id,
                                       title=source_collection_metadata.id,
                                       description=source_collection_metadata.id,
                                       extent=stac_collection_extent,
                                       license='CC-BY-SA-4.0')  # temporary

        # read and transform source collection products metadata, into destination `PDSSP_STAC_Item` metadata, then
        # create and add the corresponding PySTAC Item object to the PySTAC Collection.
        #
        while extractor.file_idx < extractor.n_extracted_files:  # TODO: improve mechanism to loop over all products.
            source_product_metadata = extractor.read_product_metadata()
            stac_item_metadata = self.transform_source_metadata(source_product_metadata, object_type='item')

            # create PySTAC Item
            stac_item = pystac.Item(
                id=stac_item_metadata.id,
                geometry=stac_item_metadata.geometry,
                bbox=stac_item_metadata.bbox,
                datetime=stac_item_metadata.datetime,
                properties=stac_item_metadata.properties,
                assets=stac_item_metadata.assets
            )

            # add to PySTAC Collection
            stac_collection.add_item(stac_item)

        # update collection extent from items
        stac_collection.update_extent_from_items()

        # add collection to the output STAC catalog
        stac_catalog = pystac.Catalog(
            id='pdssp-catalog'+'_'+stac_collection.id,
            title=f'STAC Catalog holding PDSSP-compliant {stac_collection.id} collection.',
            description='This catalog was generated by the PDSSSP Crawler.')
        stac_catalog.add_child(stac_collection)

        # save STAC catalog files
        output_stac_dir = Path(self.stac_dir, self.collection.collection_id)
        Path.mkdir(output_stac_dir, parents=True, exist_ok=overwrite)
        stac_catalog.normalize_hrefs(self.stac_dir)
        stac_catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)


    def get_geometry_from_wkt(self, wkt):
        pass


class PDSODE_STAC(AbstractTransformer):
    def __init__(self, collection=None, source_schema=None, destination_schema='PDSSP_STAC'):
        super().__init__(collection=collection, source_schema=source_schema, destination_schema=destination_schema)


class EPNTAP_STAC(AbstractTransformer):
    def __init__(self, collection=None, source_schema=None, destination_schema='PDSSP_STAC'):
        super().__init__(collection=collection, source_schema=source_schema, destination_schema=destination_schema)

    def get_id(self, source_metadata, object_type='item'):
        if object_type == 'item':
            return source_metadata.granule_uid
        else:
            return

    def get_geometry(self, source_metadata):
        return self.geometry_from_wkt(source_metadata.s_region)

    def get_bbox(self, source_metadata):
        return [source_metadata.c1min, source_metadata.c2min, source_metadata.c1max, source_metadata.c2max]


class MARSSI_STAC(AbstractTransformer):
    def __init__(self, collection=None, source_schema=None, destination_schema='PDSSP_STAC'):
        super().__init__(collection=collection, source_schema=source_schema, destination_schema=destination_schema)

SOURCE_TRANSFORMERS = {
    'PDSODE': PDSODE_STAC,
    'EPNTAP': EPNTAP_STAC,
    'MARSSI_WFS': MARSSI_STAC
}