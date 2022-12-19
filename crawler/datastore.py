"""PDSSP Crawler data store module."""

from pydantic import BaseModel
from typing import List, Union, Optional

from .registry import Service, ExternalService

from pathlib import Path
from datetime import datetime
import json

import copy

COLLECTIONS_JSON_TYPE = 'SourceCollections'
"""JSON Source Collections file type"""

class SourceCollectionModel(BaseModel):
    collection_id: str
    service: Optional[Union[Service, ExternalService]]
    source_schema: Optional[str]
    target: Optional[str]
    stac_extensions: Optional[list[str]]
    n_products: Optional[int]
    extracted: Optional[bool] = False
    extracted_files: Optional[list] = []  # should be changed/renamed to `source_dir`
    transformed: Optional[bool] = False
    stac_dir: Optional[str] = ''
    ingested: Optional[bool] = False
    stac_url: Optional[str] = ''


class DataStore:
    """DataStore class.
    """
    def __init__(self, source_data_dir='', stac_data_dir='', collections=None):
        # TODO: check that source and STAC data directories exist.
        self.source_data_dir = source_data_dir
        self.stac_data_dir = stac_data_dir

        self.collections_index_file = Path(source_data_dir, 'collections_index.json')

        # load data store collections if collections index file exists
        if self.collections_index_file.is_file():
            print('Loading data store source collections...')
            collections = self.load_collections(self.collections_index_file)
            print(f'{len(collections)} source collections loaded in the data store.')
            self.source_collections = collections
        else:
            print('Source collections index file not found.')
            if collections:
                print('Creating collections index file from input collections...')
            else:
                print('Creating empty collections index file...')

            self.reset_source_collections(collections=collections)

    def reset_source_collections(self, collections=None):
        """Reset source collections index to an empty collections or an input collections list.
        """
        self.source_collections = []
        if collections:
            self.source_collections = collections

        self.save_source_collections(overwrite=True)

    def list_source_collections(self, collection_id='', service_type=None, target=None, extracted=None, transformed=None, ingested=None):
        """Display all, or a filtered list of source collections indexed in the data store.
        """
        collections = self.get_source_collections(collection_id=collection_id, service_type=service_type,
                                                     target=target, extracted=extracted, transformed=transformed, ingested=ingested)

        if len(collections) == 0:
            print('No collections matching input filters.')
            return

        print(f'{len(collections)} collections matching input filters:')
        print()
        print(f'{"ID":<30}  {"service type":<12}  {"source schema":<13}  {"nb of products":<15}  {"extracted":<10}  {"transformed":<12}  {"ingested":<9}  {"target":<12}')
        # {"metadata schema":<18}  {"stac extensions":<20}')
        print(f'{"-" * 30}  {"-" * 12}  {"-" * 13}  {"-" * 15}  {"-" * 10}  {"-" * 12}  {"-" * 9}  {"-" * 9}')
        for collection in collections:
            extracted_str = 'Y' if collection.extracted else 'N'
            transformed_str = 'Y' if collection.transformed else 'N'
            ingested_str = 'Y' if collection.ingested else 'N'
            source_schema_str = collection.source_schema if collection.source_schema else 'UNDEFINED'
            print(f'{collection.collection_id:<30}  {collection.service.type.name:<12}  {source_schema_str:<13}  '
                  f'{collection.n_products:<15}  {extracted_str:<10}  {transformed_str:<12}  {ingested_str:<9}  {collection.target:<12}')
        print()

    def get_source_collection(self, collection_id: str) -> SourceCollectionModel:
        """Returns the source collection corresponding to input identifier.
        """
        collection = None
        for source_collection in self.source_collections:
            if source_collection.collection_id == collection_id:
                return source_collection
        return collection

    def get_source_collections(self, collection_id='', service_type=None, target=None, extracted=None, transformed=None, ingested=None) -> [SourceCollectionModel]:
        """Returns source collections matching input filters.
        """

        # set initial list of filtered source collections
        filtered_collections = copy.copy(self.source_collections)

        if collection_id:
            source_collections = []
            for collection in filtered_collections:
                if collection_id.lower() in collection.collection_id.lower():
                    source_collections.append(collection)
            filtered_collections = source_collections

        if service_type:
            source_collections = []
            for collection in filtered_collections:
                if service_type == collection.service.type.name:
                    source_collections.append(collection)
            filtered_collections = source_collections

        if target:
            source_collections = []
            for collection in filtered_collections:
                if target.lower() in collection.target.lower():
                    source_collections.append(collection)
            filtered_collections = source_collections

        if extracted:
            source_collections = []
            for collection in filtered_collections:
                if collection.extracted:
                    source_collections.append(collection)
            filtered_collections = source_collections

        if transformed:
            source_collections = []
            for collection in filtered_collections:
                if collection.transformed:
                    source_collections.append(collection)
            filtered_collections = source_collections

        if ingested:
            source_collections = []
            for collection in filtered_collections:
                if collection.ingested:
                    source_collections.append(collection)
            filtered_collections = source_collections

        return filtered_collections

    # TODO: add_source_collections
    def add_source_collections(self, collections: [SourceCollectionModel]):
        """Add collections to the source collections index table"""
        pass

    # TODO: update_source_collections
    def update_source_collections(self, collections: [SourceCollectionModel]):
        """Update collections in the source collections index table"""
        pass

    # TODO: delete_source_collections
    def delete_source_collections(self, collections: [SourceCollectionModel]):
        """Delete collections to the source collections index table"""
        pass

    def save_source_collections(self, overwrite=False):
        """Save loaded source collections into the JSON collections index file.
        """
        if not Path.is_file(self.collections_index_file) or overwrite:
            self.save_collections(self.source_collections, filepath=self.collections_index_file)

    def save_collections(self, collections, basename='', filepath=None):
        if filepath:
            collections_filepath = filepath
        else:
            if not basename:
                basename = 'collections'

            # set output JSON Source Collections file path
            collections_filename = f'{basename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json' # datetime tag
            collections_filepath = Path(self.source_data_dir, collections_filename)

        json_dict = {
            'type': COLLECTIONS_JSON_TYPE,
            'collections': []
        }
        for collection in collections:
            json_dict['collections'].append(json.loads(collection.json(by_alias=True)))

        with open(collections_filepath, 'w') as f:
            f.write(json.dumps(json_dict))

        print(f'{len(collections)} collections saved in {collections_filepath} file.')

    def load_collections(self, filepath):

        with open(filepath, 'r') as f:
            data = json.load(f)

        if 'type' in data.keys():
            if data['type'] != COLLECTIONS_JSON_TYPE:
                raise Exception(f'Error loading input {filepath} file: not a JSON `{COLLECTIONS_JSON_TYPE}` file ("type"="{data["type"]}".')
        else:
            raise Exception(f'Error loading input {filepath} file: missing JSON "type" attribute.')

        if 'collections' not in data.keys():
            raise Exception(f'Error loading input {filepath} file: missing JSON "collections" attribute.')

        # get collections
        collections_dicts = data['collections']

        collections = []
        for collection_dict in collections_dicts:
            try:
                # attempt to load collection dict to a SourceCollectionModel object
                collection = SourceCollectionModel(**collection_dict)
            except Exception as e:
                print(e)
                collection = None

            # add to list if valid
            if collection:
                collections.append(collection)
            else:
                print(f'[WARNING] The following collection dictionary could not be loaded in a SourceCollectionModel object: {collection_dict}')
                print()

        return collections