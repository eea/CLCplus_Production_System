from geoville_database_module.postgres.dict import execute_database, read_from_database_one_row
from geoville_vault_module.vault.database_engine import get_static_db_credentials

from src.config import cnf
from src.error_handlers.class_http_error_401 import UnauthorizedError
from src.init.init_variables import VAULT_CLIENT
from src.postgres_connector.postgres_sql_queries import (insert_failed_abort_orders, insert_failed_orders,
                                                         insert_order_status, order_result_status,
                                                         select_order_status, update_order_status)


########################################################################################################################
# Class definition
########################################################################################################################

class PostgresConnector:
    """ Class definition for PostgreSQL API connector

    This class handles all the database communication required in the API

    """

    def __init__(self, test_db: bool) -> None:
        self.db_creds = self.fetch_vault_db_credentials(test_db)

    @staticmethod
    def fetch_vault_db_credentials(test_db: bool) -> dict:
        """ Fetches the database credentials from the Vault server

        This method fetches from the Vault server the database credentials depending on the incoming request and chooses
        between a Production or Test database.

        Arguments:
            test_db (bool): specifying if it is a test request or not

        Returns:
            (dict): all required database credentials

        """

        if test_db:
            return get_static_db_credentials(VAULT_CLIENT, cnf.APP_CONFIG.TEST_DB_MOUNT, cnf.APP_CONFIG.TEST_DB_PATH)

        return get_static_db_credentials(VAULT_CLIENT, cnf.APP_CONFIG.SECRET_MOUNT, cnf.APP_CONFIG.DB_PATH_STATIC)

    def get_order_status(self, query_values, user_id) -> dict:
        """ Executes the SQL query for retrieving an order status

        This method sends a SELECT query to the PostgreSQL server specified in the database credentials.

        Arguments:
            query_values (tuple): values used in the SQL query
            user_id (str): unique identifier of a user

        Returns:
            (dict): SQL query result

        """
        result_data = read_from_database_one_row(select_order_status, query_values, self.db_creds, True)

        if result_data is None or result_data is False:
            return {}

        if user_id != result_data[0]:
            raise UnauthorizedError('The user is not authorized to request this resource')

        return {
            "order_id": result_data[4],
            "service_name": result_data[1],
            "status": result_data[2],
            "result": result_data[3],
            "expiration_in_days": 30
        }

    def insert_order_states(self, query_values) -> None:
        """ Executes the SQL query for inserting an order status

        This method sends an INSERT query to the PostgreSQL server specified in the database credentials.

        Arguments:
            query_values (tuple): values used in the SQL query

        """
        execute_database(insert_order_status, query_values, self.db_creds, True)

    def insert_failed_order_states(self, query_values) -> None:
        """ Executes the SQL query for inserting a failed order state

        This method sends an INSERT query to the PostgreSQL server specified in the database credentials.

        Arguments:
            query_values (tuple): values used in the SQL query

        """
        execute_database(insert_failed_orders, query_values, self.db_creds, True)

    def insert_failed_abortion_orders(self, query_values) -> None:
        """ Executes the SQL query for inserting a failed order state

        This method sends an INSERT query to the PostgreSQL server specified in the database credentials.

        Arguments:
            query_values (tuple): values used in the SQL query

        """
        execute_database(insert_failed_abort_orders, query_values, self.db_creds, True)

    def update_order_state(self, query_values) -> None:
        """ Executes the SQL query for updating the order state

        This method sends an UPDATE query to the PostgreSQL server specified in the database credentials.

        Arguments:
            query_values (tuple): values used in the SQL query

        """
        execute_database(update_order_status, query_values, self.db_creds, True)

    def update_result_order_state(self, query_values) -> dict:
        """ Executes the SQL query for updating the result order state

        This method sends an UPDATE query to the PostgreSQL server specified in the database credentials.

        Arguments:
            query_values (tuple): values used in the SQL query

        Returns:
            (dict)
        """
        res = read_from_database_one_row(order_result_status, query_values, self.db_creds, True)

        return {
            "order_id": res[2],
            "user_id": res[0],
            "service_dag_name": res[1],
            "status": res[3],
            "result": res[4],
            "order_json": res[5],
            "email": res[6],
            "order_started": res[7].strftime('%Y-%m-%dT%H:%M:%S'),
            "order_finished": res[8].strftime('%Y-%m-%dT%H:%M:%S')
        }
