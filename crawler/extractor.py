"""PDSSP Crawler extractor module (extract and read).

To add an Extractor handling a new service type::

    class NEW_Extractor(AbstractExtractor):
        def __init__(self, service=None):
            super().__init__(service=service)
            pass


    EXTRACTORS = {
        ExternalServiceType.EPNTAP: EPNTAP_Extractor,
        ExternalServiceType.PDSODE: PDSODE_Extractor,
        ExternalServiceType.WFS: WFS_Extractor,
        ExternalServiceType.NEW: NEW_Extractor
    }

"""

# from .collection import SourceProduct
import requests
from contextlib import closing
import json
from pathlib import Path

from .datastore import DataStore, SourceCollectionModel
from .registry import ExternalServiceType, Service
from .schemas import create_schema_object, PDSODE_Product, PDSODE_IIPTSet


def Extractor(collection=None, service_type='', service=None):  # -> AbstractExtractor
    """Extractor function serving as Extractor objects factory.
    """

    # set service_type_enum
    if collection:
        service_type_enum = collection.service.type
    elif service:
        service_type_enum = service.type
    elif service_type:
        service_type_enum = ExternalServiceType[service_type]
    else:
        raise ValueError('At least one of the `service_type` (str) or `service` (Service) keyword argument is required as input.')

    # check that service_type_enum is valid and create corresponding Extractor object.
    if service_type_enum in EXTRACTORS.keys():
        ExtractorClass = EXTRACTORS[service_type_enum]
        extractor = ExtractorClass(collection=collection, service=service)
        return extractor
    else:
        raise Exception(f'Invalid catalog service type: {service_type_enum}. Allowed types are: {EXTRACTORS.keys()}')


class AbstractExtractor:
    """Abstract Extractor class.
    """
    def __init__(self, collection=None, service=None):
        # automatically set extractor service type from inheriting Extractor class.
        self.service_type = ''
        class_name = self.__class__.__name__
        for service_type in EXTRACTORS.keys():
            if class_name == EXTRACTORS[service_type].__name__:
                self.service_type = service_type
        # print(f'service type = {self.service_type}')

        # init extractor properties
        self.service = None
        self.service_collections = []
        self.collection = None
        self.extracted = False
        self.n_extracted_files = 0
        self.extracted_files = []
        # self.extracted_data_dir = ''

        # set service and collection properties
        if service and not collection:
            self.set_service(service)
        elif collection and not service:
            self.set_collection(collection)
        else:
            raise ValueError('Only one of the `service` or `collection` input keyword arguments can be used.')

        self.products = []
        # self.n_products = 0
        self.file_idx = 1
        self.product_idx = 0

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}> "
            f"extracted: {self.extracted} | "
            f"extracted_files: {self.extracted_files}"
        )

    def set_service(self, service):
        # check that input service object matches with the extractor service type.
        if service.type == self.service_type:
            self.service = service
            self.service_collections = []  # reset list of service collections
        else:
            raise ValueError(f'`{service.type}` type from input `service` object does not match '
                             f'Extractor `{self.service_type}` service type ')

    def set_collection(self, collection: SourceCollectionModel):
        """Set extracted source collection from input SourceCollectionModel object and derive Extractor properties from it.
        """
        # set extract collection
        self.collection = collection

        # set service
        self.set_service(collection.service)

        # set extracted files
        self.extracted = collection.extracted
        self.n_extracted_files = len(collection.extracted_files)
        self.extracted_files = collection.extracted_files

    def get_service_collections(self):
        return []

    def extract(self):
        pass

class PDSODE_Extractor(AbstractExtractor):
    """PDSODE_Extractor class.
    """
    def __init__(self, collection=None, service=None):
        super().__init__(collection=collection, service=service)

        # self.retrieve_service_collections(service=service)

    def retrieve_service_collections(self, service=None):
        if service:  # set extractor service to input optional service keyword argument
            self.set_service(service)

        # form query to retrieve all
        query = dict(
            query='iipy',
            output='JSON',
            # odemetadb='mars'
        )

        # execute query
        print('Querying PDS ODE REST API service...')
        with closing(requests.get(self.service.url, params=query)) as r:
            if r.ok:
                response = r.json()
            else:
                raise Exception(f'PDS ODE REST API query {r.status_code} error: url={self.service.url}, query={query}')

        # parse response into the list of SourceCollectionModel objects, `self.service_collections`.
        iiptset_dicts = response['ODEResults']['IIPTSets']['IIPTSet']
        for iiptset_dict in iiptset_dicts:
            # do not add collection if products have no valid footprints
            if 'ValidFootprints' in iiptset_dict.keys():
                if iiptset_dict['ValidFootprints'] != 'T':
                    continue

            # set source collection ID
            collection_id = f'{iiptset_dict["IHID"]}_{iiptset_dict["IID"]}_{iiptset_dict["PT"]}'

            # set number of products
            if 'NumberProducts' in iiptset_dict.keys():
                n_products = int(iiptset_dict['NumberProducts'])
            else:
                print(f'Missing `NumberProducts` for {collection_id} IIPTSet: not added to service collections.')
                n_products = 0
                continue

            # TODO: valid target before adding to targets list (schema for targets, instrument hosts, instruments, product types?).
            targets = [iiptset_dict['ODEMetaDB']]  # at least the target related to the ODEMetaDB
            if 'ValidTargets' in iiptset_dict.keys():
                if 'ValidTarget' in iiptset_dict['ValidTargets'].keys():
                    iiptset_valid_target = iiptset_dict['ValidTargets']['ValidTarget']
                    # print(iiptset_valid_target)
                    if isinstance(iiptset_valid_target, str):
                        targets.append(iiptset_valid_target)  # only one target is defined, as a string
                    elif isinstance(iiptset_valid_target, list):  # more than one target defined, as a list of string
                        for target in iiptset_valid_target:
                            targets.append(target)

            # set source schema
            source_schema = self.service.extra_params['source_schema']

            # set reference target
            target = targets[0].upper()

            try:
                source_collection = SourceCollectionModel(
                    collection_id=collection_id,
                    service=self.service,
                    source_schema=source_schema,
                    n_products=n_products,
                    target=target
                )
            except:
                source_collection = None

            if source_collection:
                self.service_collections.append(source_collection)

    def get_service_collections(self, service=None, targets=None, valid_footprint=True):
    # TODO: Implement fitering, possibly based on generic keywords: targets, valid_footprint, instrument_host_ids, instrument_ids, product_types.
        if not self.service_collections:
            self.retrieve_service_collections(service=None)
        return self.service_collections

    def retrieve_collection_metadata(self, collection_id):
        # if service:  # set extractor service to input optional service keyword argument
        #     self.set_service(service)

        # form query to retrieve all
        query = dict(
            query='iipy',
            output='JSON',
            # odemetadb='mars'
        )

        # execute query
        print(f'Retrieving `{collection_id}` collection metadata from PDS ODE REST API service...')
        with closing(requests.get(self.service.url, params=query)) as r:
            if r.ok:
                response = r.json()
            else:
                raise Exception(f'PDS ODE REST API query {r.status_code} error: url={self.service.url}, query={query}')

        # parse response into the list of SourceCollectionModel objects, `self.service_collections`.
        iiptset_dicts = response['ODEResults']['IIPTSets']['IIPTSet']

        for iiptset_dict in iiptset_dicts:
            this_collection_id = f'{iiptset_dict["IHID"]}_{iiptset_dict["IID"]}_{iiptset_dict["PT"]}'
            if this_collection_id == collection_id:
                try:
                    print(iiptset_dict)
                    collection_metadata = PDSODE_IIPTSet(**iiptset_dict)
                    return collection_metadata
                except Exception as e:
                    print(e)
                    print(iiptset_dict)
                    return None

    def get_collection_metadata(self, collection_id, service=None) -> SourceCollectionModel:
        # if service:  # set extractor service to input optional service keyword argument
        #     self.set_service(service)
        for service_collection in self.service_collections:
            if service_collection.collection_id == collection_id:
                return service_collection

    def read_collection_metadata(self, collection_metadata_file_path=''): # -> SourceCollectionMetadata:
        if not collection_metadata_file_path:
            if self.extracted_files[0]:
                collection_metadata_file_path = self.extracted_files[0]
            else:
                raise Exception('Could not derive `collection_metadata_file_path`.')

        with open(collection_metadata_file_path, 'r') as f:
            metadata_dict = json.load(f)

        try:
            collection_metadata = PDSODE_IIPTSet(**metadata_dict)
        except Exception as e:
            print(e)
            print(metadata_dict)
            return None

        return collection_metadata

    def reset_reader_iterator(self):
        self.file_idx = 1
        self.products = []
        self.product_idx = 0

    def read_product_metadata(self):  # TODO: add `collection_metadata_file_path` keyword argument.
        """Iterator reader returning the next product metadata from extracted collection files.

        Use ``self.reset_reader_iterator()`` to reset reader iterator.
        """

        if not self.products:
            if self.file_idx < self.n_extracted_files:
                file_path = self.extracted_files[self.file_idx]
                with open(file_path, 'r') as f:
                    data = json.load(f)

                # store source products metadata in the list of SourceProduct.
                for metadata_dict in data['ODEResults']['Products']['Product']:
                    try:
                        product_metadata = PDSODE_Product(**metadata_dict)
                        self.products.append(product_metadata)
                    except Exception as e:
                        print(e)
                        print(metadata_dict)
                        return None
            else:
                raise Exception('No more product metadata to read.')

        next_product = self.products[self.product_idx]
        self.product_idx += 1

        if self.product_idx >= len(self.products):
            self.product_idx = 0
            self.products = []
            self.file_idx += 1

        return next_product


    def extract(self, collection_id, output_dir_path='', service=None, overwrite=False):
        """Extract collection files required to retrieve collection and product metadata.
        """
        if service:  # set extractor service to input optional service keyword argument
            self.set_service(service)

        # set `query_limit` parameters
        query_limit = 100
        extract_limit = 300  # temporary for testing purpose

        # Extract and save collection meta.
        #
        collection_metadata = self.retrieve_collection_metadata(collection_id)
        # collection_metadata = extractor.retrieve_collection_metadata('MRO_HIRISE_RDRV11')

        collection_file_path = Path(output_dir_path, collection_id, collection_id+'.json')
        if Path.is_file(collection_file_path):
            if not overwrite:
                print(f'Source collection {collection_file_path} file already exists. Use `overwrite=True` to overwrite existing files.')
                return

        Path.mkdir(collection_file_path.parent, parents=True, exist_ok=overwrite)
        with open(collection_file_path, 'w') as file:
            file.write(collection_metadata.json(indent=3))

        print(collection_file_path)

        self.n_extracted_files = 1
        self.extracted_files = [str(collection_file_path)]

        # # more sophisticated, but useful?...
        # self.extracted_files = {'collection_metadata_file': collection_file_path,
        #                         'products_metadata_files': [str(collection_file_path)]}

        # Extract and save collection products metadata.
        #
        # derive (ihid, iid, pt) IIPTSet query parameters from collection ID
        iiptset = collection_id.split('_')

        # set `target` query parameter
        if isinstance(collection_metadata.ValidTargets.ValidTarget, str):
            target = collection_metadata.ValidTargets.ValidTarget
        elif isinstance(collection_metadata.ValidTargets.ValidTarget, list):
            target = collection_metadata.ValidTargets.ValidTarget[0]

        # set default ODE API query
        query = dict(
            target=target,
            query='product',
            results='copmf',  # warning: this impacts the results metadata
            output='JSON',
            offset=0,
            limit=query_limit,
            ihid=iiptset[0],
            iid=iiptset[1],
            pt=iiptset[2]
        )

        offset = 0
        n_products = min(collection_metadata.NumberProducts, extract_limit)  # temporary for testing purpose
        print(f'Extracting metadata of {n_products} products...')
        while offset < n_products:
            # update query `offset` parameter
            query['offset'] = offset

            # execute query
            with closing(requests.get(self.service.url, params=query)) as r:
                if r.ok:
                    response = r.json()
                else:
                    raise Exception(f'PDSODE_Extractor query error: {r.status_code}')

            # write output file
            extracted_file_path = Path(output_dir_path, collection_id, collection_id+f'_{self.n_extracted_files:03}.json')

            with open(extracted_file_path, 'w') as file:
                json.dump(response, file)

            print(extracted_file_path)

            offset += query_limit + 1
            self.extracted_files.append(str(extracted_file_path))
            self.n_extracted_files += 1

        self.extracted = True
        print(f'{self.extracted_files} extracted files in {Path(output_dir_path, collection_id)} directory.')

        #self.products = response['ODEResults']['Products']['Product']   Optional, when only one extracted file is required


    # def read_next(self):
    #     file_path = self.extracted_files[self.file_idx]
    #     with open(file_path, 'r') as f:
    #         data = json.load(f)
    #
    #     # store source products metadata in the list of SourceProduct.
    #     for metadata_dict in data['ODEResults']['Products']['Product']:
    #         source_product = SourceProduct(self.source_schema, metadata_dict)
    #         self.products.append(source_product)


class WFS_Extractor(AbstractExtractor):
    """WFS_Extractor class.
    """
    def __init__(self,  collection=None, service=None):
        super().__init__( collection=collection, service=service)
        pass

class EPNTAP_Extractor(AbstractExtractor):
    """EPNTAP_Extractor class.
    """
    def __init__(self, collection=None, service=None):
        super().__init__(collection=collection, service=service)
        pass


# define list of available extractors
EXTRACTORS = {
    ExternalServiceType.EPNTAP: EPNTAP_Extractor,
    ExternalServiceType.PDSODE: PDSODE_Extractor,
    ExternalServiceType.WFS: WFS_Extractor
}
"""List of available extractors and their corresponding `ServiceType`."""