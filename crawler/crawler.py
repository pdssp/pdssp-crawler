"""Crawler module."""

from typing import List, Optional

from .extractor import Extractor
from .transformer import Transformer
from .ingestor import Ingestor
from .registry import HealthcheckrRegistry, LocalRegistry, Service, ServiceType, ExternalServiceType
from .datastore import DataStore, SourceCollectionModel
from .config import (
    SOURCE_DATA_DIR,
    STAC_DATA_DIR,
    PDSSP_REGISTRY_ENDPOINT,
    LOCAL_REGISTRY_DIRECTORY,
    STAC_CATALOG_PARENT_ENDPOINT,
)

from pathlib import Path

class Crawler:
    """Crawler class acting as controller and high-level interface.

    Used by the Crawler CLI and Airflow DAGs.
    """
    def __init__(self):
        self.registry = HealthcheckrRegistry(url=PDSSP_REGISTRY_ENDPOINT)
        self.local_registry = LocalRegistry(path=LOCAL_REGISTRY_DIRECTORY)
        self.datastore = DataStore(source_data_dir=SOURCE_DATA_DIR, stac_data_dir=STAC_DATA_DIR)
        self.registered_services = []
        self.registered_collections = []

    def reset_datastore(self):
        """Reset data store using retrieved collections from internal and external data catalog services.
        """
        self.retrieve_registered_services()
        self.retrieve_registered_collections()
        self.datastore.reset_source_collections(collections=self.registered_collections)

    def retrieve_registered_services(self) -> None:
        # allowed_types = ['WFS', 'PDSODE', 'EPNTAP'] # only "data service" types allowed
        allowed_types = ExternalServiceType.__members__.keys()

        self.registered_services = []
        for registry in [self.registry, self.local_registry]:
            for service in registry.get_services():
                if service.type.name in allowed_types:
                    self.registered_services.append(service)
                else:
                    print(f'`{service.title}` service not a data catalog service: not included in Crawler registered services.')

    def get_registered_services(self, retrieve=False) -> List[Service]:
        if not self.registered_services or retrieve:
            self.retrieve_registered_services()
        return self.registered_services

    def retrieve_registered_collections(self) -> None: # TODO: Add filters (eg: `target`)
        if not self.registered_services:
            print('No data catalog services are registered. Use Crawler.retrieve_registered_services() method. ')

        for service in self.registered_services:
            # retrieve list of collections provided by each registered service
            collections = Extractor(service=service).get_service_collections()   # filters to be added, passed to the get_service_collections() method
            print(f'{len(collections)} collections found in {service.title} service.')
            for collection in collections:
                if collection:
                    # print(f'{collection.collection_id} added to the registered collections list.')
                    self.registered_collections.append(collection)
                else:
                    print('[WARNING] Not a collection.')
            print()

        print(f'{len(self.registered_collections)} collections retrieved from {len(self.registered_services)} registered services.')

    def get_registered_collections(self, retrieve=False) -> List[SourceCollectionModel]:
        if not self.registered_collections or retrieve:
            self.retrieve_registered_services()
        return self.registered_collections

    def save_registered_collections(self, retrieve=False):
        registered_collections = self.get_registered_collections(retrieve=retrieve)
        self.datastore.save_collections(registered_collections, basename='registered_collections')

    def list_source_collections(self, collection_id='', service_type=None, target=None, extracted=None, transformed=None, ingested=None):
        """Display all, or a filtered list of source collections indexed in the data store.
        """
        self.datastore.list_source_collections(collection_id=collection_id, service_type=service_type,
                                              target=target, extracted=extracted, transformed=transformed, ingested=ingested)

    def get_source_collection(self, collection_id) -> SourceCollectionModel:
        """Returns the source collection of a given identifier."""
        return self.datastore.get_source_collection(collection_id)

    def get_source_collections(self, collection_id='', service_type=None, target=None, extracted=None, transformed=None, ingested=None) -> [SourceCollectionModel]:
        """Returns the definition of the source collection matching a set of input filters.
        """
        return self.datastore.get_source_collections(collection_id=collection_id, service_type=service_type,
                                                     target=target, extracted=extracted, transformed=transformed, ingested=ingested)


    def process_collections(self, collection_id='', service_type=None, target=None, extracted=None, transformed=None, ingested=None, overwrite=False) -> None:
        """Process all or a filtered selection of collections.
        """
        source_collections = self.get_source_collections(collection_id=collection_id, service_type=service_type,
                                                         target=target, extracted=extracted, transformed=transformed,
                                                         ingested=ingested)
        for source_collection in source_collections:
            print(f'Processing {source_collection.collection_id} collection...')
            self.extract_collection(source_collection.collection_id, overwrite=overwrite)
            self.transform_collection(source_collection.collection_id, overwrite=overwrite)
            self.ingest_collection(source_collection.collection_id, update=overwrite)

    def extract_collection(self, collection_id: str, overwrite=False) -> None:
        """Extract source collection file(s) from the "data catalog" service associated to a given collection identifier.
        """
        # get source collection from data store
        collection = self.get_source_collection(collection_id)
        if not collection:
            print(f'Could not retrieve input `{collection_id}` source collection from data store.')
            return

        if collection.extracted:
            if not overwrite: # quit unless input overwrite
                print(f'{collection_id} collection already extracted:')
                print(f'- Source collection file(s): {collection.extracted_files}')  # extracted_data_dir ???
                print()
                return

        print(f'Extracting {collection_id} source collection files...')
        try:
            extractor = Extractor(service=collection.service)
            extractor.extract(collection_id, output_dir_path=self.datastore.source_data_dir, overwrite=overwrite)  # .get_collection_metadata_files()
        except Exception as e:
            print(f'Could not extract {collection_id} source collection.')
            print(e)
            return

        # Update source collection and data store
        collection.extracted = extractor.extracted
        collection.extracted_files = extractor.extracted_files
        self.datastore.save_source_collections(overwrite=True)

        # report on source collection extraction
        print(f'{collection_id} source collection successfully extracted:')
        print(f'- Source collection file(s) = {collection.extracted_files}')
        print()


    def transform_collection(self, collection_id, subdir='', overwrite=False):
        """Transform a source collection into a STAC collection file.
        """
        # get source collection from data store
        collection = self.get_source_collection(collection_id)
        if not collection:
            print(f'Could not retrieve input `{collection_id}` source collection from data store.')
            return

        if collection.transformed:
            if not overwrite: # quit unless input overwrite
                print(f'{collection_id} already transformed:')
                print(f'- STAC collection file: {collection.stac_dir}')
                return

        if not collection.extracted:
            print(f'{collection_id} source collection not extracted as source collection file(s).')
            self.extract_collection(collection_id, overwrite=overwrite)

        if collection.extracted:
            print(f'Transforming {collection_id} source collection into a STAC catalog file...')
            print(f'- Source collection file(s): {collection.extracted_files}')
            try:
                transformer = Transformer(collection)
                output_dir_path = Path(self.datastore.stac_data_dir, subdir)
                transformer.transform(output_dir_path=output_dir_path, overwrite=overwrite)
            except Exception as e:
                print(f'Could not transform {collection_id} source collection.')
                print(e)
                return

            # Update source collection and data store
            collection.transformed = transformer.transformed
            collection.stac_dir = transformer.stac_dir
            self.datastore.save_source_collections(overwrite=True)
        else:
            print(f'Could not extract {collection_id} source collection.')

        # report on source collection transformation
        if collection.transformed:
            print(f'{collection_id} source collection successfully transformed:')
            print(f'- STAC catalog file = {collection.stac_dir}/catalog.json')
        else:
            print(f'Could not transform {collection_id} source collection.')

    def ingest_collection(self, collection_id, update=False):
        """Ingest a STAC collection into the destination STAC catalog service.
        """
        # get source collection from data store
        collection = self.get_source_collection(collection_id)
        if not collection:
            print(f'Could not retrieve input `{collection_id}` source collection from data store.')
            return

        if collection.ingested:
            if not update:  # quit unless input update is True
                print(f'{collection_id} already ingested:')
                print(f'- STAC collection file: {collection.stac_dir}')
                print(f'- STAC collection URL: {collection.stac_url}')
                return

        if not collection.transformed:
            print(f'{collection_id} source collection not transformed to STAC catalog or collection file.')
            self.transform_collection(collection_id, overwrite=update)

        if collection.transformed:
            print(f'Ingesting {collection_id} STAC catalog...')
            print(f'- STAC catalog dir: {collection.stac_dir}')
            # ingestor = Ingestor(stac_api_parent_url=STAC_CATALOG_PARENT_ENDPOINT)  # requires RESTO_ADMIN_AUTH_TOKEN env variable
            # stac_collection_file = f'{collection.stac_dir}/collection.json'
            # ingestor.ingest(stac_file=stac_collection_file, update_if_exists=update, ingest_strategy='catalog')
            try:
                ingestor = Ingestor(stac_api_parent_url=STAC_CATALOG_PARENT_ENDPOINT) # requires RESTO_ADMIN_AUTH_TOKEN env variable
                stac_collection_file = f'{collection.stac_dir}/collection.json'
                ingestor.ingest(stac_file=stac_collection_file, update_if_exists=update, ingest_strategy='both')
            except Exception as e:
                print(f'Could not ingest {collection_id} source collection.')
                print(e)
                return

            # Update source collection and data store
            collection.ingested = ingestor.ingested
            collection.stac_url = ingestor.stac_url
            self.datastore.save_source_collections(overwrite=True)
        else:
            print(f'Could not transform {collection_id} source collection.')

        # report on source collection ingestion
        if collection.ingested:
            print(f'{collection_id} successfully ingested:')
            print(f'- Source STAC catalog/collection directory (`stac_dir`): {collection.stac_dir}')
            print(f'- Destination STAC catalog/collection URL: {collection.stac_url}')
        else:
            print(f'Could not ingest {collection_id} STAC collection.')
