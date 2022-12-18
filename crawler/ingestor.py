import pystac
import requests
import os
from pathlib import Path

# DESTINATION_STAC_CATALOGS = ['mars', 'moon', 'titan']

COLLECTION_DEFAULT_MODEL = 'DefaultModel'

INGEST_STRATEGIES = {
    'catalog': { 'ingest_catalog': True, 'ingest_feature': False},
    'feature': { 'ingest_catalog': True, 'ingest_feature': False},
    'both': { 'ingest_catalog': True, 'ingest_feature': True},
    'none': { 'ingest_catalog': False, 'ingest_feature': False}
}
"""Ingest strategies define what is ingested i.e. "collection", "feature", "both" or "none".
"""

class Ingestor:
    """Ingestion of STAC catalog or collection into destination STAC API service (eg: PDSSP RESTO).
    """
    def __init__(self, stac_api_url='', auth_token='', source_collection=None):
        self.stac_api_url = stac_api_url
        self.ingested = False
        self.stac_url = ''
        self.do_not_split_geom = True
        self.source_collection = None
        self.processed_features = []  # stac2resto `lookup_table`

        # set source_schema and collection properties
        if stac_api_url and not source_collection:
            self.stac_api_url = stac_api_url
        elif source_collection and not stac_api_url:
            self.set_source_collection(source_collection)
        else:
            raise ValueError('Only one of the `stac_api_url` or `source_collection` input keyword arguments can be used.')

        # set header: resto admin auth token is required for POST
        if not auth_token:
            auth_token = os.environ.get('RESTO_ADMIN_AUTH_TOKEN')
            if not auth_token:
                raise Exception(f'RESTO_ADMIN_AUTH_TOKEN enviroment variable, or `auth_token` input argument, is required for ingestion.')
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'stac2resto',
            'Authorization': 'Bearer ' + auth_token
        }

    def set_source_collection(self, source_collection):
        self.source_collection = source_collection
        self.ingested = source_collection.ingested
        self.stac_url = source_collection.stac_url

    def update_source_collection(self):
        if self.source_collection:
            self.source_collection.ingested = self.ingested
            self.source_collection.stac_url = self.stac_url

    def post_catalog(self, catalog_dict):
        catalog_id = catalog_dict['id']

        # post request
        url = f'{self.stac_api_url}/catalogs'
        parent_id = None
        parent_path = '' if not parent_id else f'/{parent_id}'
        print(f'Creating {catalog_id} catalog to {url}{parent_path}...')
        ssl_verify = True
        response = requests.post(url, json=catalog_dict, params={"pid": parent_id}, headers=self.headers, verify=ssl_verify)

        # handling response
        if response.status_code == 200:
            print(f'{catalog_id} catalog ingested successfully.')

            # set ingestor status/attributes
            self.ingested = True
            self.stac_url = f'{url}{parent_path}/{catalog_id}'  # ?
            # self.update_source_collection()
            # TODO: all collections belonging to the ingested catalog should be updated !

            return response.json()

        # HTTP !== 200 => error
        if response.status_code != 200:
            raise Exception('Catalog ingestion failed: ' + str(response.json()))

    def update_catalog(self):
        return None

    def delete_catalog(self, catalog_id):
        return None

    def post_collection(self, collection_dict, update_if_exists=False):
        # copy input STAC collection dict
        tmp_collection_dict = collection_dict.copy()

        # get collection Id
        collection_id = tmp_collection_dict['id']

        # add collection default model to apply to new collection if not present in collection.json file
        if 'model' not in tmp_collection_dict.keys():
            tmp_collection_dict['model'] = COLLECTION_DEFAULT_MODEL

        # discard summaries and links
        if 'summaries' in tmp_collection_dict.keys():
            tmp_collection_dict.pop('summaries')
        if 'links' in tmp_collection_dict.keys():
            tmp_collection_dict.pop('links')

        # POST request
        url = f'{self.stac_api_url}/collections'
        ssl_verify = True
        print(f'Creating {collection_id} collection using `{COLLECTION_DEFAULT_MODEL}` model to {self.stac_api_url} ...')
        response = requests.post(url, json=tmp_collection_dict, headers=self.headers, verify=ssl_verify)

        # handling response
        if response.status_code == 200:
            print(f'{collection_id} collection created successfully.')
            return response
        elif response.status_code == 409:
            # HTTP 409 => collection exists. Retry with PUT to update, if `update_if_exists` input argument set to True.
            if update_if_exists:
                response = self.update_collection(collection_dict, update_if_exists=update_if_exists)
            else:
                print(f'{collection_id} already exists. Use `update_if_exists=True` to update collection.')
                return None

        # HTTP !== 200 => error
        if response.status_code != 200:
            print(f'{collection_id} collection POST failed: ' + str(response.json()))

        return response

    def update_collection(self, collection_dict, update_if_exists=False):
        # copy input STAC collection dict
        tmp_collection_dict = collection_dict.copy()

        # set collection Id
        collection_id = tmp_collection_dict['id']

        # add collection default model to apply to new collection if not present in collection.json file
        if 'model' not in tmp_collection_dict.keys():
            tmp_collection_dict['model'] = COLLECTION_DEFAULT_MODEL

        # discard summaries and links
        if 'summaries' in tmp_collection_dict.keys():
            tmp_collection_dict.pop('summaries')
        if 'links' in tmp_collection_dict.keys():
            tmp_collection_dict.pop('links')

        # PUT request
        url = f'{self.stac_api_url}/collections/{collection_id}'
        ssl_verify = True
        print(f'Updating existing {collection_id} collection using {COLLECTION_DEFAULT_MODEL} model to {url} ...')
        response = requests.put(url, json=tmp_collection_dict, headers=self.headers, verify=ssl_verify)

        # handle response
        if response.status_code == 200:
            print(f'{collection_id} collection created successfully.')
            return response
        elif response.status_code == 409:
            # HTTP 409 => collection exists. Retry with PUT to update, if `update_if_exists` input argument set to True.
            if update_if_exists:
                response = self.update_collection(collection_dict, update_if_exists=update_if_exists)
            else:
                print(f'{collection_id} already exists. Use `update_if_exists=True` to update collection.')
                return response

        # HTTP !== 200 => error
        if response.status_code != 200:
            print(f'{collection_id} collection PUT failed: ' + str(response.json()))

        return response

    def delete_collection(self, collection_id):
        # set request
        url = f'{self.stac_api_url}/collections/{collection_id}'
        ssl_verify = True

        # DELETE request
        print(f'Deleting {collection_id} collection ...')
        response = requests.post(url, headers=self.headers, verify=ssl_verify)

        # handle response
        if response.status_code == 200:
            print(f'{collection_id} collection deleted successfully.')
        else:
            print(f'{collection_id} collection DELETE failed: {str(response.json())}')
            return None

        return response

    def post_feature(self, feature_dict, update_if_exists=False):
        # set feature ID
        feature_id = feature_dict['id']
        collection_id = feature_dict['collection']

        if feature_id in self.processed_features:
            return None

        # Set request
        #
        url = f'{self.stac_api_url}/collections/{collection_id}/items'
        ssl_verify = True

        # use or not ST_SplitDateLine
        params = {}
        if self.do_not_split_geom:
            params = {'_splitGeom': 0}

        # Post request
        #
        print(f'Creating {feature_id} feature in {collection_id} collection ...')
        response = requests.post(url, json=feature_dict, params=params, headers=self.headers, verify=ssl_verify)

        # Handle response
        #
        # HTTP 409 => feature exists. Retry with PUT to update (self.update_feature)
        if response.status_code == 409:
            if update_if_exists:
                response = self.update_feature(feature_dict)
            else:
                print(f'{feature_id} already exists. Use `update_if_exists=True` to update feature.')
                return None

        if response.status_code == 200:
            print(f'{feature_id} feature created successfully.')
        else:
            print(f'{feature_id} feature POST failed: {str(response.json())}')
            return None

        # # HTTP !== 200 => error
        # if response.status_code != 200:
        #     print('Collection POST failed: ' + str(response.json()))

        return response

    def update_feature(self, feature_dict):
        # set feature and parent collection ID
        feature_id = feature_dict['id']
        collection_id = feature_dict['collection']

        # set request
        url = f'{self.stac_api_url}/collections/{collection_id}/items/{feature_id}'
        ssl_verify = True

        # post request
        print(f'Updating {feature_id} feature in {collection_id} collection ...')
        response = requests.put(url, json=feature_dict, headers=self.headers, verify=ssl_verify)

        # handle response
        if response.status_code == 200:
            print(f'{feature_id} feature updated successfully.')
        else:
            print(f'{feature_id} feature PUT failed: {str(response.json())}')
            return None

        return response

    def delete_feature(self, feature_id):
        return None

    def delete(self, stac_file='', collection_id='', feature_id='', catalog_id=''):
        if stac_file:
            # read input STAC file
            stac_object_dict = pystac.read_file(stac_file).to_dict()

            if not stac_object_dict or 'type' not in stac_object_dict.keys():
                raise Exception(f'Invalid STAC file: {stac_file}.')

            stac_object_type = stac_object_dict['type']
            stac_object_id = stac_object_dict['id']
            print(f'Found `{stac_object_id}` {stac_object_type.lower()}.')
        else:
            # get input STAC object type and ID
            if collection_id:
                stac_object_type = 'Collection'
                stac_object_id = collection_id
            elif feature_id:
                stac_object_type = 'Feature'
                stac_object_id = feature_id
            elif catalog_id:
                stac_object_type = 'Catalog'
                stac_object_id = catalog_id
            else:
                raise ValueError('At least one of the input optional argument is required.')

        # delete STAC object
        if stac_object_type == 'Collection':
            print(stac_object_id)
            self.delete_collection(stac_object_id)
        elif stac_object_type == 'Feature':
            self.delete_feature(stac_object_id)
        elif stac_object_type == 'Catalog':
            self.delete_catalog(stac_object_id)
        else:
            raise ValueError('Invalid STAC object type.')


    def ingest(self, stac_file='', stac_api_url='', update_if_exists=False, ingest_strategy='catalog'):  # dest_catalog_name='',
        """Ingest input STAC file into destination STAC API catalog service.

        Input STAC file can be a catalog, a collection or an item JSON file. Different ingestion strategies define
        what is ingested i.e. 'catalog', 'feature', 'both' or 'none'.

        ~ stac2resto ("process_stuff(url, lookup_table"))
        """
        # read input STAC file
        stac_object_dict = pystac.read_file(stac_file).to_dict()  # "stuff"

        if not stac_object_dict or 'type' not in stac_object_dict.keys():
            raise Exception(f'Invalid STAC file: {stac_file}.')

        if ingest_strategy not in INGEST_STRATEGIES.keys():
            raise Exception(f'Invalid `{ingest_strategy}` ingestion strategy. Allowed values are: {list(INGEST_STRATEGIES.keys())}')
        else:
            ingest_feature = INGEST_STRATEGIES[ingest_strategy]['ingest_feature']
            ingest_catalog = INGEST_STRATEGIES[ingest_strategy]['ingest_catalog']

        if stac_object_dict['type'] == 'Feature':
            if ingest_feature:
                response = self.post_feature(stac_object_dict, update_if_exists=update_if_exists)
                if response:
                    self.processed_features.append(stac_object_dict['id']) # append feature ID
            return

        if stac_object_dict['type'] == 'Collection':
            print(f'Found `{stac_object_dict["id"]}` collection.')
            if ingest_catalog:
                self.post_collection(stac_object_dict, update_if_exists=update_if_exists)

        if stac_object_dict['type'] == 'Catalog':
            print(f'Found `{stac_object_dict["id"]}` catalog.')
            if ingest_catalog:
                self.post_catalog(stac_object_dict)

        # no links skip
        if isinstance(stac_object_dict['links'], list) is False:
            print('  No links to process - skipping')
            return

        # recursively process/ingest links
        size = len(stac_object_dict['links'])
        print("   Found %s links" % str(size))

        for link in stac_object_dict['links']:
            # derive the absolute child url
            # child_path = get_absolute_url(stac_file, link['href'])
            child_path = str(Path(Path(stac_file).parent, link['href'])) #

            if link['rel'] in ['item', 'items'] and ingest_feature:
                # print(child_path)
                self.ingest(stac_file=child_path, ingest_strategy=ingest_strategy, update_if_exists=update_if_exists)
            elif link['rel'] == 'child':
                print("------------------------------------------------------------------------------------")
                print("Process %s" % child_path)
                print("------------------------------------------------------------------------------------")
                self.ingest(stac_file=child_path, ingest_strategy=ingest_strategy, update_if_exists=update_if_exists)

        if stac_object_dict['type'] == 'Collection':
            # self.ingested = True
            self.stac_url = f'{self.stac_api_url}/collections/{stac_object_dict["id"]}'