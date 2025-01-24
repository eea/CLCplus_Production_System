from geoville_database_module_utils.db_config import postgresql


########################################################################################################################
# Method definition
########################################################################################################################

def read_from_database_one_row(sql, values, db_params, autocommit):
    """ Reads one row from the database

    This function reads one row from a database query and returns its result

    Arguments:
        sql (str): SQL query string
        values (tuple): values for the SQL query
        db_params (dict): contains the database connection parameters
        autocommit (bool): True...ON, False...Off

    Returns:
        result (tuple): A tuple with ONE item with the result

    """

    connection = __connect_to_database(db_params, autocommit)
    result = postgresql.__query_select_fetch_one_row(connection, sql, values)
    __close_database_connection(connection)

    return result


########################################################################################################################
# Method definition
########################################################################################################################

def read_from_database_all_rows(sql, values, db_params, autocommit):
    """ Reads all rows from the database

    This function reads all rows from a database query and returns its result.

    Arguments:
        sql (str): SQL query string
        values (tuple): values for the SQL query
        db_params (dict): contains the database connection parameters
        autocommit (bool): True...ON, False...Off

    Returns:
        result (tuple): A tuple holding all the data

    """

    connection = __connect_to_database(db_params, autocommit)
    result = postgresql.__query_select_fetchall(connection, sql, values)
    __close_database_connection(connection)

    return result


########################################################################################################################
# Method definition
########################################################################################################################

def read_from_database_many_rows(sql, values, size, db_params, autocommit):
    """ Reads many (size) rows from the database

    This function reads many rows from a database query and returns its result. By specifying the size parameter the
    number of rows to be returned, can be configured.

    Arguments:
        sql (str): SQL query string
        values (tuple): values for the SQL query
        size (int): number of returned rows
        db_params (dict): contains the database connection parameters
        autocommit (bool): True...ON, False...Off

    Returns:
       result (tuple): A tuple holding some data

    """

    connection = __connect_to_database(db_params, autocommit)
    result = postgresql.__query_select_fetchmany(connection, sql, values, size)
    __close_database_connection(connection)

    return result


########################################################################################################################
# Method definition
########################################################################################################################

def execute_database(sql, values, db_params, autocommit):
    """ Executes commands against the database

    This function executes a command against the DB without returning a query result.

    Arguments:
        sql (str): SQL query string
        values (tuple): values for the SQL query
        db_params (dict): contains the database connection parameters
        autocommit (bool): True...ON, False...Off

    Returns:
        success (bool): success of the operation

    """

    connection = __connect_to_database(db_params, autocommit)
    success = postgresql.__execute_database(connection, sql, values)
    __close_database_connection(connection)

    return success


########################################################################################################################
# Method definition
########################################################################################################################

def execute_values_database(sql, param_list, db_params, autocommit):
    """ Batch method for insert, updates and delete

    This function execute many onto the db_config (for updates, inserts, del operations)

    Arguments:
        sql (str): SQL query string
        param_list: The list to execute values
        db_params (dict): contains the database connection parameters
        autocommit (bool): True...ON, False...Off

    Returns:
        success (bool): success of the operation

    """

    connection = __connect_to_database(db_params, autocommit)
    success = postgresql.__execute_values(connection, sql, param_list)
    __close_database_connection(connection)

    return success


########################################################################################################################
# Method definition
########################################################################################################################

def __connect_to_database(db_params, autocommit):
    """
    Connect to the db_config

    Arguments:
        db_params (dict): full path to the database configuration file
        autocommit (bool): True...ON, False...Off

    Returns:
        connection (obj): the db_config connection

    """

    connection = postgresql.__connect_to_database(db_params, autocommit)
    connection.commit()

    return connection


########################################################################################################################
# Method definition
########################################################################################################################

def __close_database_connection(connection):
    """ Closes the database connection

    Destructor for the database connection object

    Arguments:
        connection (obj): current database connection object

    Returns:
        success (bool): success of the operation

    """

    success = postgresql.__close_connection(connection)
    return success
