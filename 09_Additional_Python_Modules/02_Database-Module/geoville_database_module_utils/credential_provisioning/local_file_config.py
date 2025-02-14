import os
from configparser import ConfigParser, NoSectionError


########################################################################################################################
# Method definition
########################################################################################################################

def config_postgresql(filename, section) -> object:
    """ PostgreSQL config from .ini file

    A typical database config example file may look like that:
    ---------------------------------------
    [sectionName]
    host=xxxxx
    database=xxxxx
    user=xxxxx
    password=xxxxx
    port=xxxxx
    ---------------------------------------

    Arguments:
        filename (str): Name of the config file providing the credentials for the db_config connection
        section (str): the section in the db_config credential file providing us

    Returns:
        section_data (list): all necessary information to establish a db_config connection

    """

    parser = ConfigParser()

    if os.path.exists(filename):
        parser.read(filename)

        section_data = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                section_data[param[0]] = param[1]
        else:
            raise NoSectionError(f'No section {section} found in the given file {filename}')

        return section_data

    else:
        raise FileNotFoundError(f'File does not exist under the given path: {filename}')
