import psycopg2
import psycopg2.extras
import time

from geoville_database_module_utils.connection_config.connection_config import LIMIT_RETRIES
from geoville_database_module_utils.credential_provisioning.local_file_config import config_postgresql


########################################################################################################################
# Method definition
########################################################################################################################

def __read_credentials(filename, section):
    """ Reads database credentials from a file

    This method reads the database credentials from a given configuration file (.ini)

    Arguments:
        filename (str): full path to the database configuration file
        section (str): section name in the database configuration file

    Returns:
        params (dict): database connection parameters

    """

    params = config_postgresql(filename, section)
    return params


########################################################################################################################
# Method definition
########################################################################################################################

def __connect_to_database(db_connection_params, autocommit):
    """ Connects to the database

    This method is used to connect to the database specified in the connection parameters

    Arguments:
        db_connection_params (dict): database connection parameters from the configuration file
        autocommit (bool): True...ON, False...Off

    Returns:
        connection (obj): an active connection

    """

    retry_counter = 0

    while retry_counter < LIMIT_RETRIES:
        try:
            connection = psycopg2.connect(**db_connection_params)
            connection.set_session(autocommit=autocommit)
            connection.commit()

        except psycopg2.OperationalError as error:
            print(f'Unable to connect! Retry: {retry_counter} Error: {error}')
            time.sleep(1)
            retry_counter += 1
            continue

        return connection

    print('Unable to connect after LIMIT_RETRIES')


########################################################################################################################
# Method definition
########################################################################################################################

def __query_select_fetch_one_row(connection, query, values):
    """
    The fetchone row method

    Arguments:
        connection (obj): current database connection object
        query (str): SQL query string
        values (tuple): values for the SQL query

    Returns:
        result (tuple): the result tuple

    """

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()
        connection.commit()

    except psycopg2.OperationalError as error:
        print(f'Database error fetchone querySelect "{query}", error: {error}')
        return False

    else:
        return result


########################################################################################################################
# Method definition
########################################################################################################################

def __query_select_fetchall(connection, query, values):
    """
    The fetchall row method

    Arguments:
        connection (obj): current database connection object
        query (str): SQL query string
        values (tuple): values for the SQL query

    Returns:
        result (tuple): the result tuple

    """

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        connection.commit()

    except psycopg2.OperationalError as error:
        print(f'Database error in fetchall querySelect "{query}", error: {error}')
        return False

    else:
        return result


########################################################################################################################
# Method definition
########################################################################################################################

def __query_select_fetchmany(connection, query, values, rows):
    """
    The fetchmany row method

    Arguments:
        connection (obj): current database connection object
        query (str): SQL query string
        values (tuple): values for the SQL query
        rows (int): number of returned rows

    Returns:
        result (tuple): the result tuple

    """

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchmany(rows)
        connection.commit()

    except psycopg2.OperationalError as error:
        print(f'Database error in fetchmany querySelect "{query}", error: {error}')
        return False

    else:
        return result


########################################################################################################################
# Method definition
########################################################################################################################

def __execute_database(connection, query, values):
    """
    Execute a command in the DB method

    Arguments:
        connection (obj): current database connection object
        query (str): SQL query string
        values (tuple): values for the SQL query

    Returns:
        (bool): success of the operation

    """

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

    except psycopg2.OperationalError as error:
        print(f'Database error execute sql "{query}", error: {error}')
        return False

    else:
        return True


########################################################################################################################
# Method definition
########################################################################################################################

def __execute_values(connection, query, param_list) -> bool:
    """
    Execute many values command, for large updates, large inserts, etc.

    Arguments:
        connection (obj): current database connection object
        query (str): SQL query string
        param_list (list): list of parameters to be executed in the query

    Returns:
        (bool): success of the operation

    """

    try:
        cursor = connection.cursor()
        psycopg2.extras.execute_values(cursor, query, param_list)
        connection.commit()

    except psycopg2.OperationalError as error:
        print(f'Database error in execute_batch "{query}", error: {error}')
        return False

    else:
        return True


########################################################################################################################
# Method definition
########################################################################################################################

def __close_connection(connection):
    """ Closes the connection

    This method closes the database connection

    Arguments:
        connection (obj): current database connection object

    Returns:
        (bool): success of the operation

    """

    try:
        connection.close()

    except psycopg2.OperationalError as error:
        print(f'Database error closing connection {error}')
        return False

    else:
        return True


########################################################################################################################
# Method definition
########################################################################################################################

def __del__(connection):
    """ Destructor method

    This method serves as a destructor method for closing the database connection objet

    Arguments:
        connection (obj): current database connection object

    """

    connection.close()
