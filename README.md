# PDSSP Crawler

The PDSSP Crawler is the software component responsible for the extraction, transformation and ingestion of planetary surface data products metadata into the _PDSSP STAC Catalog service_ (RESTO). Through an Airflow web interface, it also provides a way to orchestrate and manage the PDSSP Crawler's tasks and behaviour.

Collection and products metadata are extracted from _OGC data catalog services_ (WFS and Features API), defined in the _PDSSP Services Registry_. Metadata can also be extracted from non-OGC data catalog services (PDS ODE API, ENP-TAP, HTTP GET), locally defined by the PDSSP operator (see [data/services](data/services)).

In both cases, metadata ingested into the PDSSP STAC Catalog are compliant to the STAC data model and STAC extensions, including the Solar System STAC extension.

See the [online documentation](https://pdssp.github.io/pdssp-crawler) for more information.

## Development

> :warning: The PDSSP Crawler is under development, and the current version is not fully fonctional nor stable.


## Installation

1. Set up conda environment

```
conda create --name pdssp-env python=3.9
```

2. Create and/or go to your working directory

```
mkdir -p </path/to/pdssp/crawler>
cd </path/to/pdssp/crawler>
```

3. Download and install package

```
git clone https://github.com/pdssp/pdssp-crawler.git
pip install -e pdssp-crawler
pip install -r pdssp-crawler/tests/requirements.txt
pip install -r pdssp-crawler/docs/requirements.txt
```

## Configuration

Edit the [crawler/config.py](pdssp-crawler/crawler/config.py) file to change the following variables:

```python
SOURCE_DATA_DIR = '/Users/nmanaud/workspace/pdssp/crawler-data'
STAC_DATA_DIR = '/Users/nmanaud/workspace/pdssp/pdssp-stac-repo'
PDSSP_REGISTRY_ENDPOINT = 'https://pdssp.ias.universite-paris-saclay.fr/registry/services'
LOCAL_REGISTRY_DIRECTORY = '/Users/nmanaud/workspace/pdssp/pdssp-crawler/data/services'
STAC_CATALOG_ENDPOINT = 'https://pdssp.ias.universite-paris-saclay.fr/catalog'
```

## Usage

### Crawler CLI

For example:

```shell
crawler extract --source_collection_id='pdsode-mex-omega-edr'
```


See [Crawler CLI Reference](https://pdssp.github.io/pdssp-crawler/crawler_cli.html)

### Crawler Python API

For example:

```python
from crawler.crawler import Crawler

crawler = Crawler()
services = crawler.get_registered_services()
```

See [Crawler Python API Reference](https://pdssp.github.io/pdssp-crawler/crawler_api.html)

### Crawler Web Interface (Airflow) 

https://pdssp.ias.universite-paris-saclay.fr/crawler (in development)


## Contributing

Keeping in mind that this project is starting and in active development...

If you are interested in the general topic of _planetary geospatial data catalog interoperability_ or the PDSSP Crawler in particular, feel to reach out to us, raise your questions, suggestions, or issues via the [PDSSP Crawler GitHub Issues](https://github.com/pdssp/pdssp-crawler/issues).


## Authors

* [Nicolas Manaud](https://github.com/nmanaud) (initial design/implementation work)
* [Jérôme Gasperi](https://github.com/jjrom) ("stac2resto", Dockerizing)
* [J-Christophe Malapert](https://github.com/J-Christophe) (project initiator/management)

See also the list of [contributors](https://github.com/pdssp/pdssp-crawler/graphs/contributors) who is participating in the development of the PDSSP Crawler.

## License
