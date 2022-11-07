"""Transformator module."""

# import
from pydantic import BaseModel

from crawler.schemas import create_schema_object  # create_metadata_object ?

SOURCE_TRANSFORMERS = {
    'PDSODE': PDSODE_STAC,
    'EPNTAP': EPNTAP_STAC},
    'MARSSI': MARSSI_STAC}
}

def Transformer(source_schema, destination_schema='PDSSP_STAC'):
    """Transformer function serving as Transformer objects factory.
    """
    if source_schema in SOURCE_TRANSFORMERS.keys():
        TransformerClass = SOURCE_TRANSFORMERS[source_schema]
        transformer = TransformerClass(source_schema, destination_schema=destination_schema)
        return transformer
    else:
        print(f'Unknown schema name: `{source_schema}`.')
        return None
    pass


class TransformerSchemaInputError(Exception):
    """Custom error that is raised when invalid schema name is passed.
    """
    def __int__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class AbstractTransformer:
    def __init__(self, source_schema, destination_schema='PDSSP_STAC'):
        if source_schema not in SOURCE_TRANSFORMERS.keys():
            raise TransformerSchemaInputError(value=source_schema, message=f'Allowed schema names: {list(SOURCE_TRANSFORMERS.keys())}')
        self.source_schema = source_schema
        self.destination_schema = 'PDSSP_STAC'

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}> "
            f"source_schema: {self.source_schema} | "
            f"destination_schema: {self.destination_schema}"
        )

    def transform_source_metadata(self, src_metadata: BaseModel) -> BaseModel:
        return src_metadata

    def transform_source_file(self, src_file_path: str, dst_file_path: str) -> None:
        pass


class PDSODE_STAC(AbstractTransformer):
    def __init__(self, source_schema, destination_schema='PDSSP_STAC'):
        super().__init__(source_schema, destination_schema=destination_schema)

    def get_stac_item_dict(self, src_metadata):
        return {
            'type': type,
            'stac_version': stac_version,
            'stac_extensions': stac_extensions,
            'id': src_metadata.granule_uid,
            'geometry': geometry_from_wkt(source_item.s_region),
            'bbox': [source_item.c1min, source_item.c2min, source_item.c1max, source_item.c2max],
            'properties': properties_dict,
            'links': links_dict,
            'assets': assets_dict,
            'collection': ''
        }

    def transform_source_metadata(self, src_metadata: BaseModel) -> BaseModel:  # PDSSP_STAC_Item or PDSSP_STAC_Collection
        # check that input source metadata object class (schema model, eg: EPNTAP_Granule -> EPNTAP Item) is valid for
        # the transformer, given its source schema name (self.source_schema).

        pdssp_stac_item_dict = self.get_stac_item_dict(src_metadata)
        pdssp_stac_item = create_schema_object(pdssp_stac_item_dict, 'PDSSP_STAC', 'item')
        return pdssp_stac_item


class EPNTAP_STAC(AbstractTransformer):
    def __init__(self, source_schema, destination_schema='PDSSP_STAC'):
        super().__init__(source_schema, destination_schema=destination_schema)


class MARSSI_STAC(AbstractTransformer):
    def __init__(self, source_schema, destination_schema='PDSSP_STAC'):
        super().__init__(source_schema, destination_schema=destination_schema)
