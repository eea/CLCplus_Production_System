from setuptools import find_packages, setup

########################################################################################################################
# Python package definition
########################################################################################################################

setup(
    name='geoville-database-module',
	version="1.0.0",
    packages=find_packages(exclude=["tests", "*test.py"]),
    url='',
    license='GeoVille Software',
    author='Michel Schwandner',
    author_email='schwandner@geoville.com',
    description='GeoVille PostgreSQL database connector supporting .ini files and python dictionaries',
    install_requires=['psycopg2-binary==2.9.5']
)
