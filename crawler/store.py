"""PDSSP Crawler data store module."""

from pydantic import BaseModel

from .config import (
    SOURCE_DATA_DIR,
    STAC_DATA_DIR,
    REGISTRY_GITHUB_REPOSITORY,
    STAC_GITHUB_REPOSITORY
)

class SourceCollectionStatus(BaseModel):
    collection_id: str
    extracted: bool
    transformed: bool
    ingested: bool

class DataStore:
    """DataStore class.
    """
    def __init__(self, source_data_dir=SOURCE_DATA_DIR, stac_data_dir=STAC_DATA_DIR):
        # TODO: check that source and STAC data directories exist.
        self.source_data_dir = source_data_dir
        self.stac_data_dir = stac_data_dir

    def get_source_collection(self, src_collection_id):
        pass