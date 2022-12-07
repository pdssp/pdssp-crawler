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
from .schemas import create_schema_object, PDSODE_Product

def Extractor(service_type='', service=None): # source_collection_model as input !!!!!!
    """Extractor function serving as Extractor objects factory.
    """
    if service:
        service_type_enum = service.type
    elif service_type:
        service_type_enum = ExternalServiceType[service_type]
    else:
        raise ValueError('Either a `service_type` (str) or `service` (Service) keyword argument is required as input.')

    if service_type_enum in EXTRACTORS.keys():
        ExtractorClass = EXTRACTORS[service_type_enum]
        extractor = ExtractorClass(service=service)
        return extractor
    else:
        raise Exception(f'Invalid catalog service type: {service_type_enum}. Allowed types are: {EXTRACTORS.keys()}')


class AbstractExtractor:
    """Abstract Extractor class.
    """
    def __init__(self, service=None):
        # automatically set extractor service type from inheriting Extractor class.
        self.service_type = ''
        class_name = self.__class__.__name__
        for service_type in EXTRACTORS.keys():
            if class_name == EXTRACTORS[service_type].__name__:
                self.service_type = service_type
        # print(f'service type = {self.service_type}')

        # check that optional input service object matches with the extractor service type.
        self.service = None
        self.service_collections = []
        if service:
            self.set_service(service)

        self.products = []
        # self.n_products = 0
        self.file_idx = 1
        self.product_idx = 0

        self.extracted = False
        self.n_extracted_files = 0
        self.extracted_files = []
        # self.extracted_data_dir = ''

    def set_service(self, service):
        if service.type == self.service_type:
            self.service = service
            self.service_collections = []  # reset list of service collections
        else:
            raise ValueError(f'`{service.type}` type from input `service` object does not match '
                             f'Extractor `{self.service_type}` service type ')

    def get_service_collections(self):
        return []

    def extract(self):
        pass

class PDSODE_Extractor(AbstractExtractor):
    """PDSODE_Extractor class.
    """
    def __init__(self, service=None, extracted_files=None):
        super().__init__(service=service)

        self.retrieve_service_collections(service=service)

        if extracted_files:
            self.extracted_files = extracted_files

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

            try:
                source_collection = SourceCollectionModel(collection_id=collection_id, service=self.service,
                                                          n_products=n_products, targets=targets)
            except:
                source_collection = None

            if source_collection:
                self.service_collections.append(source_collection)

    def get_service_collections(self, service=None, targets=None, valid_footprint=True):
    # TODO: Implement fitering, possibly based on generic keywords: targets, valid_footprint, instrument_host_ids, instrument_ids, product_types.
        if not self.service_collections:
            self.retrieve_service_collections(service=None)
        return self.service_collections

    #
    # def extract_collection_metadata(self, collection_id, service=None):
    #     """Extract collection metadata into source collection file."""
    #     pass

    def get_collection_metadata(self, collection_id, service=None) -> SourceCollectionModel:
        # if service:  # set extractor service to input optional service keyword argument
        #     self.set_service(service)
        for service_collection in self.service_collections:
            if service_collection.collection_id == collection_id:
                return service_collection

    def read_collection_metadata(self, collection_metadata_file_path): # -> SourceCollectionMetadata:
        with open(collection_metadata_file_path, 'r') as f:
            data = json.load(f)
        return data

    def reset_reader_iterator(self):
        self.file_idx = 1
        self.products = []
        self.product_idx = 0

    def read_next_product_metadata(self):
        """Iterator reader returning the next product metadata from extracted collection files.
        """
        if not self.products:
            if self.file_idx < self.n_extracted_files:
                file_path = self.extracted_files[self.file_idx]
                with open(file_path, 'r') as f:
                    data = json.load(f)

                # store source products metadata in the list of SourceProduct.
                for metadata_dict in data['ODEResults']['Products']['Product']:
                    product_metadata = PDSODE_Product(**metadata_dict)
                    self.products.append(product_metadata)
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
        collection_metadata = self.get_collection_metadata(collection_id)

        collection_file_path = Path(output_dir_path, collection_id, collection_id+'.json')
        if Path.is_file(collection_file_path):
            if not overwrite:
                print(f'Extracted {collection_file_path} file already exists. Use `overwrite=True` to overwrite existing files.')
                return

        Path.mkdir(collection_file_path.parent, parents=True, exist_ok=overwrite)
        with open(collection_file_path, 'w') as file:
            json.dump(collection_metadata.json(), file)

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
        target = collection_metadata.targets[0].lower()

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
        n_products = min(collection_metadata.n_products, extract_limit)  # temporary for testing purpose
        print(f'Extracting {n_products} products metadata...')
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
    def __init__(self, service=None):
        super().__init__(service=service)
        pass

class EPNTAP_Extractor(AbstractExtractor):
    """EPNTAP_Extractor class.
    """
    def __init__(self, service=None):
        super().__init__(service=service)
        pass


# define list of available extractors
EXTRACTORS = {
    ExternalServiceType.EPNTAP: EPNTAP_Extractor,
    ExternalServiceType.PDSODE: PDSODE_Extractor,
    ExternalServiceType.WFS: WFS_Extractor
}
"""List of available extractors and their corresponding `ServiceType`."""