from setuptools import setup, find_packages
from os import path

name = 'pdssp-crawler'
version_file = open(path.join('.', 'VERSION'))
version = version_file.read().strip()
# package_name
setup(
    name=name,
    version=version,
    py_modules=find_packages(),
    include_package_data=True,
    install_requires=[
        'apache-airflow==2.4.1',
        'pystac',
        'pydantic',
        'pyyaml',
        'geojson',
        'shapely'
    ],
    entry_points='''
        [console_scripts]
        crawler=crawler.cli:cli
    ''',
    command_options={
    'build_sphinx': {
        'project': ('setup.py', name),
        'version': ('setup.py', version),
        'source_dir': ('setup.py', 'docs')}},
)
