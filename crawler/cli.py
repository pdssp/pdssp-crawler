"""Crawler CLI module."""

import click
import os
import yaml

from .config import (
    SOURCE_DATA_DIR,
    STAC_DATA_DIR,
    PDSSP_REGISTRY_ENDPOINT,
    LOCAL_REGISTRY_DIRECTORY,
    STAC_CATALOG_PARENT_ENDPOINT,
)
from crawler.crawler import Crawler
from crawler.extractor import Extractor
import crawler.schemas

package_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = open(os.path.join(package_path, 'VERSION')).read().strip()


@click.version_option(package_name='pdssp-crawler')
@click.group()
def cli():
    """Crawler CLI."""
    pass

@cli.command()
def config():
    """Show Crawler configuration."""
    click.echo()
    click.echo(f'(Internal) PDSSP Services Registry URL   : {PDSSP_REGISTRY_ENDPOINT}')
    click.echo(f'(External) services registry directory   : {LOCAL_REGISTRY_DIRECTORY}')
    click.echo(f'Source collections data directory        : {SOURCE_DATA_DIR}')
    click.echo(f'STAC collections data directory          : {STAC_DATA_DIR}')
    click.echo(f'Destination (PDSSP) STAC API Catalog URL : {STAC_CATALOG_ENDPOINT}')
    click.echo()

@cli.command()
def initds():
    """Initialise data store."""
    Crawler().reset_datastore()

@cli.command()
@click.option('--id', type=click.STRING, help='Collection ID filter.', default='')
@click.option('--service-type', type=click.STRING, help='Service type filter.', default='')
@click.option('--target', type=click.STRING, help='Target filter.', default='')
@click.option('--extracted/--no-extracted', help='Filter to return only transformed collections', default=None)
@click.option('--transformed/--no-transformed', help='Filter to return only transformed collections', default=None)
@click.option('--ingested/--no-ingested', help='Filter to return only ingested collections', default=None)
def collections(id, service_type, target, extracted, transformed, ingested):
    """Show source collections available in the data store.

    Returned source collections can optionally be filtered by identifier, service type, target, and whether or it has been
    extracted, transformed or ingested.
    """
    Crawler().list_source_collections(
        collection_id=id,
        service_type=service_type,
        target=target,
        extracted=extracted,
        transformed=transformed,
        ingested=ingested
    )

@cli.command()
@click.option('--id', type=click.STRING, help='Collection ID filter.', default='')
@click.option('--service-type', type=click.STRING, help='Service type filter.', default='')
@click.option('--target', type=click.STRING, help='Target filter.', default='')
@click.option('--extracted/--no-extracted', help='Filter to return only transformed collections', default=None)
@click.option('--transformed/--no-transformed', help='Filter to return only transformed collections', default=None)
@click.option('--ingested/--no-ingested', help='Filter to return only ingested collections', default=None)
@click.option('--overwrite/--no-overwrite', help='Overwrite existing source collection files.', default=False)
def process(id, service_type, target, extracted, transformed, ingested, overwrite):
    """Process all or a filtered selection of source collections.

    Use options to filter source collections from the data store. If you're unsure about the filtering result, first use
    the `collections` command to preview the list of source collections given your input filters.

    Source collections will currently be processed sequentially, going through extraction, transformation and ingestion.
    Note that all STAC collections are grouped into a single STAC catalog, with one catalog per target body. Ingestion
    of all collections could be done at once when they all have been transformed.
    """
    Crawler().process_collections(collection_id=id, service_type=service_type, target=target, extracted=extracted,
                                  transformed=transformed, ingested=ingested, overwrite=overwrite)

@cli.command()
@click.option('--id', type=click.STRING, help='Collection ID.', default='')
@click.option('--overwrite/--no-overwrite', help='Overwrite existing source collection files.', default=False)
def extract(id, overwrite):
    """Extract source collection metadata files from source data catalog service.
    """
    Crawler().extract_collection(id, overwrite=overwrite)


@cli.command()
@click.option('--id', type=click.STRING, help='Collection ID.', default='')
@click.option('-o', '--overwrite/--no-overwrite', help='Overwrite existing STAC catalog files.', default=False)
def transform(id, overwrite):
    """Transform extracted source collection files to STAC catalog files.
    """
    Crawler().transform_collection(id, overwrite=overwrite)


@cli.command()
@click.option('--id', type=click.STRING, help='Collection ID.', default='')
@click.option('--update/--no-update', help='Update destination STAC collection if exists', default=False)
def ingest(id, update):
    """Ingest transformed STAC catalog files to destination STAC API Catalog.
    """
    Crawler().ingest_collection(id, update=update)


@cli.command()
@click.option('-s', '--service-title', type=click.STRING, help='Show service information/collections for a given service title.', default='')
def registry(service_title):
    """Show internal and external registered services.

    Optionally display service information and collections using the `service` option.
    For example::

        crawler registry --service-title='PDS ODE API'
        crawler registry -s 'PDS ODE API'

    """
    crawler = Crawler()
    registered_services = crawler.get_registered_services()
    if service_title:
        for registered_service in registered_services:
            if registered_service.title == service_title:
                collections = Extractor(service=registered_service).get_service_collections()
                print()
                print(f'{len(collections)} collections found in {service_title}:')
                for collection in collections:
                    print(f'- {collection.collection_id}')
                print()
    else:
        print()
        print(f'{len(registered_services)} registered services found:')
        for registered_service in registered_services:
            print(f'- {registered_service.title}')
        print()

@cli.command()
@click.option('--get/--no-get', help='Get schema JSON representation.', default=False)
@click.option('--name', type=click.STRING, help='Name of the schema.', default='')
@click.option('--type', type=click.STRING, help='Type of the schema object: `collection` or `item`.', default='')
def schemas(get, name, type):
    """Get schemas information."""
    if get:
        print(crawler.schemas.get_schema_json(name,type))
    else:
        print(crawler.schemas.get_schema_names())

if __name__ == '__main__':
    cli()
