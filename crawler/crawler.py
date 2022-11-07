"""Crawler module."""

from typing import Optional
from .collection import SourceCollection
from .registry import Registry, CollectionDefinition
from .store import DataStore, SourceCollectionStatus
from .config import (
    SOURCE_DATA_DIR,
    STAC_DATA_DIR,
    LOCAL_REGISTRY_YAML_FILE,
    REGISTRY_GITHUB_REPOSITORY,
    STAC_GITHUB_REPOSITORY
)

from .extractor import Extractor

class Crawler:
    """Crawler class acting as main controller.
    """
    def __init__(self):
       self.registry = Registry('YAML', path=LOCAL_REGISTRY_YAML_FILE)
       self.data_store = DataStore()

    def get_collection_definition(self, src_collection_id: str) -> Optional[CollectionDefinition]:
        """Returns the definition of a source collection, given its identifier.
        """
        return self.registry.get_collection(src_collection_id)

    def get_collection_status(self, src_collection_id: str) -> Optional[SourceCollectionStatus]:
        """Returns the processing status of a source collection.
        """
        src_collection = self.data_store.get_source_collection(src_collection_id)
        if src_collection:
            return src_collection.get_status()
        else:
            return None

    def extract_collection(self, src_collection_id: str, overwrite=False) -> None:
        """Extract source collection file(s) from the "data catalog" service associated to a given collection identifier.
        """

        # Check if source collection has been already extracted.
        src_collection = self.data_store.get_source_collection(src_collection_id)
        if src_collection:
            if src_collection.extracted:
                print(f'{src_collection_id} source collection has already between exacted:')
                print(f'extracted_data_dir = {src_collection.extracted_data_dir}')
                print(f'n_extracted_files = {src_collection.n_extracted_files}')
                print(f'extracted_files = {src_collection.extracted_files}')
                return
        else:
            # Get collection definition from the registry
            src_collec_def = self.registry.get_collection_definition(id=src_collection_id)
            src_collection = SourceCollection(src_collec_def)

        print(f'Extracting {src_collection_id} source collection...')
        # Extractor(src_collec_def, output_dir=self.data_store.source_data_dir).extract()
        src_collection.extract()

        # Report on source collection extraction
        if src_collection.extracted:
            print(f'{src_collection_id} source collection has been successfully extracted.')
            print(f'extracted_data_dir = {src_collection.extracted_data_dir}')
            print(f'n_extracted_files = {src_collection.n_extracted_files}')
            print(f'extracted_files = {src_collection.extracted_files}')

    def transform_collection(self, src_collection_id, overwrite=False):
        """Transform a single source collection into a STAC collection file."""

        # Get SourceCollection Object from the Crawler DataStore
        src_collection = self.data_store.get_source_collection(src_collection_id)
        if src_collection.extracted:
            src_collection.transform()
        else:
            print(f'{src_collection_id} source collection has not been extracted yet.')

        # Report on source collection transformation
        if src_collection.transformed:
            print(f'{src_collection_id} source collection has been successfully transformed into a STAC collection.')
            print(f'stac_collection_path = {src_collection.stac_collection_path}')

    def ingest_collection(self, src_collection_id):
        """Ingestion a collection into the destination STAC catalog service.
        """
        print(f'Loading your {src_collection_id} STAC collection soon...')