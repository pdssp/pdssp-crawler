"""PDSSP Crawler collection module."""

from .extractor import Extractor
from .transformer import Transformer
from .ingestor import Ingestor

class SourceCollection:
    """SourceCollection class.
    """
    def __init__(self, src_collec_def):
        """Constructor class.
        """
        # self.definition = definition # definition object
        self.id = src_collec_def.id
        self.title = src_collec_def.title
        self.description = src_collec_def.description
        # self.source_metadata = {}  # collection metadata set by extracting source metadata using the Extractor.
        # self.source_products = []  # list of SourceProduct objects extracted using the Extractor
        self.extractor = Extractor(src_collec_def)
        self.transformer = Transformer()
        self.ingestor = Ingestor()

    def __iter__(self):
        self.extractor.__iter__()

    def __next__(self):
        self.extractor.__next__()
        # ...or next(self.extractor)

    def get_next_product(self):
        self.__next__()

    def get_metadata(self):
        return self.extractor.get_collection_metadata()

    def is_extracted(self):
        return self.extractor.is_extracted()

    def is_transformed(self):
        return self.transformer.is_transformed()

    def is_ingested(self):
        return self.extractor.is_ingested()

    def get_source_schema(self):
        return self.extractor.get_source_schema()

    def get_stac_catalog_path(self):
        return self.transformer.get_stac_catalog_path()

    def get_stac_collection_url(self):
        return self.ingestor.get_stac_collection_url()

    def extract(self):
        """Extract.
        """
        self.extractor.extract(id=self.id, output_dir=DataStore().source_data_dir)

    def transform(self):
        """Transform.
        """
        self.transformer.transform()

    def ingest(self, dst_stac_server_url):
        self.ingestor.ingest()

class SourceProduct:
    """SourceProduct class.
    """
    def __init__(self):
        self.metadata = {}

    def get_metadata(self):
        return self.metadata

class SourceCollections:
    """SourceCollections class.
    """
    def __init__(self):
        self.n_source_collections = 0
        self.source_collections = []

    def add_collection(self, src_collection):
        self.source_collections.append(src_collection)
        self.n_source_collections +=1