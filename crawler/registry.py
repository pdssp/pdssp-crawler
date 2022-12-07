"""PDSSP Crawler RegistryInterface module."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

import requests
from contextlib import closing

from pathlib import Path
import glob
import json

class ProviderRole(Enum):
    producer = 'producer'
    licensor = 'licensor'
    processor = 'processor'
    host = 'host'


class ServiceProvider(BaseModel):
    name: str = Field(..., title='Organization name')
    description: Optional[str] = Field(None, title='Organization description')
    roles: Optional[List[ProviderRole]] = Field(None, title='Organization roles')
    url: Optional[str] = Field(None, title='Organization homepage')


class ServiceType(Enum):
    STAC = 'STAC'
    WFS = 'WFS'
    WMS = 'WMS'
    WMTS = 'WMTS'
    XYZ = 'XYZ'


class ExternalServiceType(Enum):
    WFS = 'WFS'
    PDSODE = 'PDSODE'
    EPNTAP = 'EPNTAP'


class Service(BaseModel):
    title: str
    description: str
    providers: List[ServiceProvider]
    type: ServiceType
    url: str
    ping_url: Optional[str] = None
    ssys_targets: Optional[List[str]] = Field(None, alias='ssys:targets')


class ExternalService(Service):
    type: ExternalServiceType
    extra_params: Optional[dict]


class RegistryInterface():
    """Abstract registry class that defines a common interface for the children HealthcheckrRegistry and Local RegistryInterface classes."""
    def __init__(self, url='', path=''):
        self.url = url
        self.path = path
        self.services = []

    def get_services(self) -> List[Service]:
        return self.services

class HealthcheckrRegistry(RegistryInterface):
    """Class that represents a PDSSP Services RegistryInterface.

    End-point: https://pdssp.ias.universite-paris-saclay.fr/registry/services
    """
    def __init__(self, url=''):
        super().__init__(url=url)

    def get_services(self):
        with closing(requests.get(self.url)) as r:
            if r.ok:
                response = r.json()
            else:
                raise Exception(f'Unable to retrieve data services registered at {self.url}: {r.status_code}')

        if 'services' not in response.keys():
            raise Exception('Response not conform to expected model.')

        services_dicts = response['services']
        if not isinstance(services_dicts, list):
            raise Exception('Response not conform to expected model.')

        for service_dict in services_dicts:
            self.services.append(Service(**service_dict))

        return self.services


class LocalRegistry(RegistryInterface):
    """Class that represents a local registry defining external services, not compliant to the PDSSP data model.
    """
    def __init__(self, path=''):  # path='pdssp-crawler/data/services'
        super().__init__(path=path)

    def get_services(self):
        # check that local registry directory exists
        if not (Path(self.path).exists() and Path(self.path).is_dir()):
            raise Exception('Input `{path}` path does not exist or not a directory')

        # list all JSON files in local registry directory
        service_json_files = glob.glob(self.path+'/*.json')

        # add service corresponding to each service JSON file
        for service_json_file in service_json_files:
            with open(service_json_file, 'r') as f:
                service_dict = json.load(f)
                self.services.append(ExternalService(**service_dict))

        return self.services
