from setuptools import find_packages, setup


########################################################################################################################
# Python package definition
########################################################################################################################

setup(
    name='geoville-keycloak-module',
	version="1.1.1",
    packages=find_packages(exclude=["tests", "*tests.py"]),
    url='',
    license='GeoVille Software',
    author='Michel Schwandner',
    author_email='schwandner@geoville.com',
    description='Useful functionalities to communicate to GeoVilles Keycloak server',
    install_requires=['python-keycloak==3.9.3', 'fastapi>=0.85']
)