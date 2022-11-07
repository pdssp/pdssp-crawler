"PDSSP Crawler extractor module (extract and read)."

# from .collection import SourceProduct
import requests
from contextlib import closing
import json
from pathlib import Path

from .store import DataStore
from .product import SourceProduct

def Extractor(collection_definition):
    """Extractor function serving as Extractor objects factory.
    """
    SERVICES_TYPES = {
        'EPNTAP_API': EPNTAP_Extractor,
        'PDSODE_API': PDSODE_Extractor,
        'WFS_API': WFS_Extractor
    }
    service_type = collection_definition.source.service.type
    if service_type in SERVICES_TYPES.keys():
        ExtractorClass = SERVICES_TYPES[service_type]
        extractor = ExtractorClass(collection_definition)
        return extractor
    else:
        print(f'Unknown catalog service type: {service_type}.')
        return None

class AbstractExtractor:
    """Abstract Extractor class.
    """
    def __init__(self, collection_definition):
        # self.source_collection = collection_definition
        self.collection_id = collection_definition.id
        self.service_type = collection_definition.source.service.type
        self.service_url = collection_definition.source.service.url
        self.service_params = collection_definition.source.service.params
        self.source_schema = collection_definition.source.metadata_schema  # Eg: PDSODE, EPNTAP, MarsSI
        self.source_format = collection_definition.source.file_format  # Eg: ODE JSON, GML, VOTable, GeoJSON, Shapefiles
        self.extracted_data_dir = ''
        self.n_extracted_files = 0
        self.extracted_files = []
        self.products = []
        self.extracted = False

    def __iter__(self):
        self.file_iter = 0
        self.product_iter = 0
        return

    def __next__(self):
        # returns next product from wihtin the extracted file set.
        self.product_iter += 1

        # if the end of the current extracted file has been reached, move to the next one.


        self.r
        return self.products[self.product_iter-1]  # a SourceProduct object

    def extract(self):
        pass

class PDSODE_Extractor(AbstractExtractor):
    """PDSODE_Extractor class.
    """
    def __init__(self, collection_definition):
        super().__init__(collection_definition)

        self.response = None

    def extract(self):
        # set ODE API query
        query = dict(
            target=self.service_params['target'],
            query='product',
            results='copmf',  # warning: this impacts the results metadata
            output='JSON',
            ihid=self.service_params['ihid'],
            iid=self.service_params['iid'],
            pt=self.service_params['pt']
        )

        # execute query
        with closing(requests.get(self.service_url, params=query)) as r:
            if r.ok:
                response = r.json()
            else:
                raise Exception(f'PDSODE_Extractor error with query at url: {self.service_url} with code: {r.status_code}')


        extracted_file_path = Path(DataStore().source_data_dir, self.collection_id, self.collection_id+'_001.json')
        Path.mkdir(extracted_file_path.parent, parents=True)

        # write extracted file
        with open(extracted_file_path, 'w') as file:
            json.dump(response, file)

        #self.products = response['ODEResults']['Products']['Product']   Optional, when only one extracted file is required

        self.n_extracted_files += 1
        self.extracted_files.append(extracted_file_path)

    def read_next(self):
        file_path = self.extracted_files[self.file_iter]
        with open(file_path, 'r') as f:
            data = json.load(f)

        # store source products metadata in the list of SourceProduct.
        for metadata_dict in data['ODEResults']['Products']['Product']:
            source_product = SourceProduct(self.source_schema, metadata_dict)
            self.products.append(source_product)


class WFS_Extractor(AbstractExtractor):
    """WFS_Extractor class.
    """

    def __init__(self):
        pass

class EPNTAP_Extractor(AbstractExtractor):
    """EPNTAP_Extractor class.
    """

    def __init__(self):
        pass