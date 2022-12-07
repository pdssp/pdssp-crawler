"""PDSSP Crawler Definitions module."""
from typing import Optional
from pydantic import BaseModel
import yaml
from pathlib import Path

# Definitions

class ServiceDefinition(BaseModel):
    type: str
    url: str
    params: dict


class SourceDefinition(BaseModel):
    service: ServiceDefinition
    metadata_schema: str
    file_format: str


class CollectionDefinition(BaseModel):
    id: str
    title: str
    description: str
    extensions: list[str]  # eg: ['ssys', 'proj']
    source: SourceDefinition
    path: str

class CatalogDefinition(BaseModel):
    id: str
    title: str
    description: str
    extensions: list[str]

    catalogs: list[str]
    """List of catalog ids."""

    collections: list[str]
    """List of collection ids."""

    path: str
    """Catalog path relative to root catalog."""


class AbstractDefinitions:
    """AbstractDefinitions class defining an common interface/methods for any types of registry.
    """
    def __init__(self, path=''):
        # assign registry interface type
        self.type = ''
        for type in REGISTRY_TYPES.keys():
            if self.__class__.__name__ == REGISTRY_TYPES[type].__name__:
                self.type = type
        # set path
        self.path = path

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}> "
            f"Type: {self.type} | "
            f"Path: {self.path}"
        )

    def get_collections_ids(self, id='', path='') -> list[str]:
        return []

    def get_collections(self, id='', path='') -> list[CollectionDefinition]:
        return []

    def get_collection(self, id) -> CollectionDefinition:
        return None

    def get_catalog_ids(self) -> list[str]:
        return []

    def get_catalogs(self, id) -> list[CatalogDefinition]:
        return None

    def get_catalog(self, id, path='') -> CatalogDefinition:
        return None

def Definitions(type: str, path='') -> AbstractDefinitions:
    """Function serving as Definitions objects factory.

    Example:
        registry = Definitions('YAML', path='/path/to/stac_catalog/model/catalog.yaml')
    """
    if type in REGISTRY_TYPES.keys():
        DefinitionsClass = REGISTRY_TYPES[type]
        registry = DefinitionsClass(path=path)
        return registry
    else:
        print(f'Unknown registry type: {type}.')
        return None

    #
    # def __init__(self, parameters, geoevt=None, silent=None):
    #     super().__init__(parameters, geoevt=geoevt, silent=silent)
    #

class YAMLInvalidDefinition(Exception):
    """Invalid YAML Definitions definition."""

class YAMLDefinitions(AbstractDefinitions):
    """YAMLDefinitions class
    """
    def __init__(self, path=''):
        super().__init__(path=path)
        self.catalogs = [] # : list[CatalogDefinition]
        self.collections = [] #: list[CollectionDefinition]
        self.services = []  # : list[ServiceDefinition]

        # TODO: check that registry YAML file exists

        # parse YAML registry (root) catalog file
        yaml_catalog_dict = self.parse_yaml_catalog_file(self.path)
        self.add_catalog(yaml_catalog_dict, '.')
        self.catalogs.reverse()
        self.collections.reverse()

    def add_catalog(self, yaml_catalog_dict, relpath):
        #print(f'catalog_relpath = {relpath}')
        # raise exception if required YAML `catalog` attributes are missing
        for yaml_attr in ['id', 'title', 'description']:
            if yaml_attr not in yaml_catalog_dict.keys():
                raise Exception(f'Missing YAML catalog `{yaml_attr}` attribute: {yaml_catalog_dict}')

        # set default YAML `extensions` attribute value to empty list if missing
        extensions = []
        if 'extensions' in yaml_catalog_dict.keys():
            extensions = yaml_catalog_dict['extensions']

        # set default YAML `catalogs` attribute value to empty list if missing
        catalogs_relpaths = []
        catalogs_ids = []
        if 'catalogs' in yaml_catalog_dict.keys():
            catalogs_relpaths = yaml_catalog_dict['catalogs']
            for catalogs_relpath in catalogs_relpaths:
                catalog_relpath = Path(relpath, catalogs_relpath)
                abspath = str(Path(Path(self.path).parent, catalog_relpath))
                catalog_dict = self.parse_yaml_catalog_file(abspath)
                self.add_catalog(catalog_dict, str(catalog_relpath.parent))
                if self.last_added_catalog_id():
                    catalogs_ids.append(self.last_added_catalog_id())
                else:
                    raise YAMLInvalidDefinition('Invalid YAML collection catalog: {catalog_dict}')

        # set default YAML `collections` attribute value to empty list if missing
        collections_relpaths = []
        collections_ids = []
        if 'collections' in yaml_catalog_dict:
            collections_relpaths = yaml_catalog_dict['collections']
            for collections_relpath in collections_relpaths:
                collections_relpath = Path(relpath, collections_relpath)
                abspath = str(Path(Path(self.path).parent, collections_relpath))
                yaml_collection_dict = self.parse_yaml_collection_file(abspath)
                self.add_collection(yaml_collection_dict, str(collections_relpath.parent))
                if self.last_added_collection_id():
                    collections_ids.append(self.last_added_collection_id())
                else:
                    raise YAMLInvalidDefinition('Invalid YAML collection definition: {collection_dict}')

        # create and add catalog
        catalog = CatalogDefinition(
            id=yaml_catalog_dict['id'],
            title=yaml_catalog_dict['title'],
            description=yaml_catalog_dict['description'],
            extensions=extensions,
            catalogs=catalogs_ids,
            collections=collections_ids,
            path=relpath
        )
        self.catalogs.append(catalog)

    def add_collection(self, yaml_collection_dict, relpath):
        #print(f'collection_relpath = {relpath}')
        # raise exception if required YAML `collection` attributes are missing
        for yaml_attr in ['id', 'title', 'description', 'source']:
            if yaml_attr not in yaml_collection_dict.keys():
                raise Exception(f'Missing YAML collection `{yaml_attr}` attribute in: {yaml_collection_dict}')

        # set default YAML `extensions` attribute value to empty list if missing
        extensions = []
        if 'extensions' in yaml_collection_dict.keys():
            extensions = yaml_collection_dict['extensions']

        yaml_source_dict = yaml_collection_dict['source']
        service = ServiceDefinition(**yaml_source_dict['service'])
        self.add_service(service)

        metadata_schema = ''
        if 'metadata_schema' in yaml_source_dict.keys():
            metadata_schema = yaml_source_dict['metadata_schema']

        file_format = ''
        if 'file_format' in yaml_source_dict.keys():
            file_format = yaml_source_dict['file_format']

        source = SourceDefinition(service=service, metadata_schema=metadata_schema, file_format=file_format)

        # create and add catalog to registry
        collection = CollectionDefinition(
            id=yaml_collection_dict['id'],
            title=yaml_collection_dict['title'],
            description=yaml_collection_dict['description'],
            extensions=extensions,
            source=source,
            path=relpath
        )
        self.collections.append(collection)


    def add_service(self, service: ServiceDefinition):
        self.services.append(service)

    def parse_yaml_catalog_file(self, yaml_catalog_relpath):
        with open(yaml_catalog_relpath, mode='r') as file:
            yaml_catalog_dict = (yaml.safe_load(file))
        catalog_dict = {}
        if 'catalog' in yaml_catalog_dict.keys():
            catalog_dict = yaml_catalog_dict['catalog']
        return catalog_dict

    def parse_yaml_collection_file(self, yaml_collection_relpath):
        with open(yaml_collection_relpath, mode='r') as file:
            yaml_collection_dict = (yaml.safe_load(file))
        collection_dict = {}
        if 'collection' in yaml_collection_dict.keys():
            collection_dict = yaml_collection_dict['collection']
        return collection_dict

    def last_added_catalog_id(self):
        return self.catalogs[-1].id

    def last_added_collection_id(self):
        return self.collections[-1].id

    def get_collections_ids(self, id='', path='') -> list[str]:
        collections_ids = []
        for collection in self.collections:
            if (id in collection.id) and (path in collection.path):
                collections_ids.append(collection.id)
        return collections_ids

    def get_collections(self, id='', path='') -> list[CollectionDefinition]:
        matching_collections = []
        for collection in self.collections:
            if (id in collection.id) and (path in collection.path):
                matching_collections.append(collection)
        return matching_collections

    def get_collection(self, id) -> Optional[CollectionDefinition]:
        for collection in self.collections:
            if collection.id == id:
                return collection
        return None

    def get_catalogs_ids(self, id='', path='') -> list[str]:
        catalogs_ids = []
        for catalog in self.catalogs:
            if (id in catalog.id) and (path in catalog.path):
                catalogs_ids.append(catalog.id)
        return catalogs_ids

    def get_catalogs(self, id='', path='') -> list[CatalogDefinition]:
        matching_catalogs = []
        for catalog in self.catalogs:
            if (id in catalog.id) and (path in catalog.path):
                matching_catalogs.append(catalog)
        return matching_catalogs

    def get_catalog(self, id) -> Optional[CatalogDefinition]:
        for catalog in self.catalogs:
            if catalog.id == id:
                return catalog
        return None

class RESTOAPIDefinitions(AbstractDefinitions):
    """RESTOAPIDefinitions class.
    """
    def __init__(self, definition):
        print('Not implemented yet.')


REGISTRY_TYPES = {
    'YAML': YAMLDefinitions,
    'RESTO_REGISTRY_API': RESTOAPIDefinitions  # doesn't exists yet
}