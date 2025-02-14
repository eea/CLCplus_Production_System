########################################################################################################################
# SQL select query for the GET order status request
########################################################################################################################

select_order_status = """SELECT 
                             user_id, service_name, status, result, order_id
                         FROM
                             service_orders.orders
                         WHERE 
                             order_id = %s AND 
                             deleted_on IS NULL;
                      """

########################################################################################################################
# SQL insert query for inserting an initial order state
########################################################################################################################

insert_order_status = """INSERT INTO service_orders.orders 
                         (
                             user_id, service_name, email, order_id, status, order_json
                         ) 
                         VALUES
                         (
                             %s, %s, %s, %s, %s, %s
                         );
                      """

########################################################################################################################
# SQL update query for updating the order state
########################################################################################################################

update_order_status = """UPDATE service_orders.orders 
                         SET
                             status = 'FAILED'
                         WHERE
                             order_id = %s
                      """


########################################################################################################################
# SQL update query for updating the order result state
########################################################################################################################

order_result_status = """UPDATE service_orders.orders as so
                         SET
                             status = %s,
                             result = %s
                         WHERE
                             order_id = %s
                         RETURNING so.*
                      """

########################################################################################################################
# SQL insert query for inserting the failed order states
########################################################################################################################

insert_failed_orders = """INSERT INTO service_orders.failed_orders 
                          (
                              user_id, service_name, order_id, status, order_json
                          ) 
                          VALUES
                          (
                              %s, %s, %s, %s, %s
                          );
                       """

########################################################################################################################
# SQL insert query for the inserting failed abort message
########################################################################################################################

insert_failed_abort_orders = """INSERT INTO service_orders.failed_abortion_orders 
                                (
                                    user_id, service_name, order_id, status
                                ) 
                                VALUES
                                (
                                    %s, %s, %s, %s
                                );
                             """