# PDSSP Crawler

**Extract, transform and ingest planetary surface metadata into a STAC API Catalog.**

The PDSSP Crawler is the software component responsible for the extraction, transformation and ingestion of planetary surface data products metadata into the _PDSSP STAC Catalog service_ (RESTO). Through an Airflow web interface, it also provides a way to orchestrate and manage the PDSSP Crawler's tasks and behaviour.

Collection and products metadata are extracted from _OGC data catalog services_ (WFS, Features API, STAC API), defined in the _PDSSP Services Registry_. Metadata can also be extracted from _non-OGC data catalog services_ (PDS ODE API, ENP-TAP, HTTP GET, PDS API, ...), locally defined by the PDSSP operator (see [data/services](data/services)).

In both cases, metadata ingested into the PDSSP STAC Catalog are compliant to the _PDSSP Data Model_, which consists of the STAC data model extended through existing and new STAC extensions, including the Solar System STAC extension.

> :warning: The PDSSP Crawler is under development, and the current version is not fully functional nor stable. See the [online documentation](https://pdssp.github.io/pdssp-crawler) for more information.

## Installation

In a next version installation via Docker will be possible, enabling deployment to the PDSSP server. For now, follow these steps:

1. **Set up conda environment**

Create environment:

```
conda create --name pdssp-env python=3.9
```

Activate environment:

```
conda activate pdssp-env
```

2. **Create and go to your working directory**

```
mkdir -p </path/to/pdssp/crawler>
cd </path/to/pdssp/crawler>
```

3. **Download and install package**

```
git clone https://github.com/pdssp/pdssp-crawler.git
pip install -e pdssp-crawler
pip install -r pdssp-crawler/tests/requirements.txt
pip install -r pdssp-crawler/docs/requirements.txt
```

## Configuration


The configuration mechanism will be improved in the next versions. For now:

1. Create the _incoming source_ and the _outgoing STAC_ directories in your working directories. For example:

```shell
mkdir crawler-data
mkdir pdssp-stac-repo
```

3. Edit the [crawler/config.py](crawler/config.py) file to change the following variables accordingly. In the following example, `/Users/nmanaud/workspace/pdssp` is the working directory and the source and STAC data directories are respectively named `crawler-data` and `pdssp-stac-repo`. 

```python
SOURCE_DATA_DIR = '/Users/nmanaud/workspace/pdssp/crawler-data'
STAC_DATA_DIR = '/Users/nmanaud/workspace/pdssp/pdssp-stac-repo'
PDSSP_REGISTRY_ENDPOINT = 'https://pdssp.ias.universite-paris-saclay.fr/registry/services'
LOCAL_REGISTRY_DIRECTORY = '/Users/nmanaud/workspace/pdssp/pdssp-crawler/data/services'
STAC_CATALOG_PARENT_ENDPOINT = 'https://pdssp.ias.universite-paris-saclay.fr'
```

Set the `RESTO_ADMIN_AUTH_TOKEN` environment variable, required for ingestion POST request to PDSSP Catalog STAC API (RESTO).

Airflow configutation [TBD]

## Usage

### Crawler CLI

List CLI commands and get help:

```shell
crawler --help
```

Initialise data store with available source collections (run once):

```shell
crawler initds
```

Display/filter source collections status:

```shell
crawler collections --target=mars
```

Extract, transform and ingest:

```shell
crawler extract --id='MRO_HIRISE_RDRV11'
crawler transform --id='MRO_HIRISE_RDRV11'
crawler ingest --id='MRO_HIRISE_RDRV11'
```
or just:

```shell
crawler ingest --id='MRO_HIRISE_RDRV11'
```

Process all source collections associated to Mars:

```shell
crawler process --target=mars
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

Keeping in mind that this project is in active development... if you are interested in the general topic of _planetary geospatial data catalog interoperability_ or the PDSSP Crawler in particular, feel to reach out to us, raise your questions, suggestions, or issues using [PDSSP Crawler GitHub Issues](https://github.com/pdssp/pdssp-crawler/issues).


## Authors

* [Nicolas Manaud](https://github.com/nmanaud) (initial design/implementation work)
* [Jérôme Gasperi](https://github.com/jjrom) ("stac2resto", Dockerizing)
* [Jean-Christophe Malapert](https://github.com/J-Christophe) (project initiator/management)

See also the list of [contributors](https://github.com/pdssp/pdssp-crawler/graphs/contributors) who is participating in the development of the PDSSP Crawler.

## License

This project is licenced under [Apache License 2.0](https://github.com/pdssp/pdssp-crawler/blob/main/LICENSE) [TBC].