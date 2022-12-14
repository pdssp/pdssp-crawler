import pytest

from crawler.registry import RegistryInterface, YAMLRegistry
from crawler.config import LOCAL_REGISTRY_YAML_FILE

@pytest.fixture
def registry():
    """Return a YAMLRegistry object."""
    return RegistryInterface('YAML', path=LOCAL_REGISTRY_YAML_FILE)

def test_create_yaml_registry():
    registry = RegistryInterface('YAML', path=LOCAL_REGISTRY_YAML_FILE)
    print(registry)
    assert isinstance(registry, YAMLRegistry)

def test_parse_stac_catalog_model(registry):
    registry.parse_stac_catalog_model()
    assert True