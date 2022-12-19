"""Crawler CLI module."""

import click
import os
import yaml

from crawler.config import LOCAL_REGISTRY_DIRECTORY
from crawler.registry import RegistryInterface
import crawler.schemas

package_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = open(os.path.join(package_path, 'VERSION')).read().strip()


@click.version_option(package_name='pdssp-crawler')
@click.group()
def cli():
    """Crawler CLI."""
    pass


@cli.command()
@click.option('--get-collections/--no-get-collections', help='Get list of registry collections.', default=False)
@click.option('--get-collection/--no-get-collection', help='Get registry collection.', default=False)
@click.option('--get-catalogs/--no-get-catalogs', help='Get list of registry catalogs.', default=False)
@click.option('--get-catalog/--no-get-catalog', help='Get registry catalog.', default=False)
@click.option('--id', type=click.STRING, help='ID or ID filter.', default='')
@click.option('--path', type=click.STRING, help='Path filter.', default='')
def registry(get_collections, get_collection, get_catalogs, get_catalog, id, path):
    """Get registry catalogs and collections."""

    registry = RegistryInterface('YAML', path=LOCAL_REGISTRY_YAML_FILE)

    if get_collections:
        # print(id, path)
        collections = registry.get_collections(id=id, path=path)
        if collections:
            click.echo(f'{len(collections)} collections matching input filters:')
            click.echo()
            click.echo(f'{"ID":<40}  {"path":<20}  {"service type":<15}  {"metadata schema":<18}  {"stac extensions":<20}')
            click.echo(f'{"-"*40}  {"-"*20}  {"-"*15}  {"-"*18}  {"-"*20}')
            for collection in collections:
                click.echo(f'{collection.id:<40}  {collection.path:<20}  '
                           f'{collection.source.service.type:<15}  {collection.source.metadata_schema:<18}  '
                           f'{collection.extensions}')
            click.echo()
        else:
            click.echo(f'No collections matching input filter: id={id}, path={path}')
    elif get_collection:
        collection = registry.get_collection(id)
        if collection:
            click.echo(yaml.safe_dump(collection.dict(), sort_keys=False))
        else:
            click.echo(f'No collection matching input ID: {id}')
    elif get_catalogs:
        catalogs = registry.get_catalogs(id=id, path=path)
        if catalogs:
            click.echo(f'{len(catalogs)} catalogs matching input filters:')
            click.echo()
            click.echo(
                f'{"ID":<30}  {"path":<20}')
            click.echo(f'{"-" * 30}  {"-" * 20}')
            for catalog in catalogs:
                click.echo(f'{catalog.id:<30}  {catalog.path:<20}')
            click.echo()
        else:
            click.echo(f'No catalogs matching input filter: id={id}, path={path}')
    elif get_catalog:
        catalog = registry.get_catalog(id)
        if catalog:
            click.echo(yaml.safe_dump(catalog.dict(), sort_keys=False))
        else:
            click.echo(f'No catalog matching input ID: {id}')
    else:
        click.echo(f'type: {registry.type}')
        click.echo(f'path: {registry.path}')
        click.echo(f'number of catalogs: {len(registry.catalogs)}')
        click.echo(f'number of collections: {len(registry.collections)}')
        click.echo()

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
