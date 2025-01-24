from setuptools import find_packages, setup


########################################################################################################################
# Python package definition
########################################################################################################################

setup(
    name='geoville-vault-module',
	version="1.0.0",
    packages=find_packages(exclude=["tests", "*tests.py"]),
    url='',
    license='GeoVille Software',
    author='Michel Schwandner',
    author_email='schwandner@geoville.com',
    description="Useful functionalities to communicate to GeoVille's Hashicorp Vault server",
    install_requires=['hvac==2.0.0', 'requests~=2.31']
)
