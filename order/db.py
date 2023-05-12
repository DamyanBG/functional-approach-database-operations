from common.database import execute_query, database_connect, insert_query_builder
from collections import Callable


def insert_order(order_data: dict) -> str:
    result = execute_query(
        database_connect,
        insert_query_builder(
            "orders",
            ["name", "customer_name", "quantity"],
            [order_data["name"], order_data["customer_name"], order_data["quantity"]],
        ),
        lambda cursor: cursor.fetchone(),
    )

    return result[0]


def insert_order_curry(
    execute_func: Callable,
    database_connect_func: Callable,
    insert_query_builder_func: Callable,
) -> Callable:
    def insert_order(order_data: dict) -> str:
        result = execute_func(
            database_connect_func,
            insert_query_builder_func(
                "orders",
                ["name", "customer_name", "quantity"],
                [
                    order_data["name"],
                    order_data["customer_name"],
                    order_data["quantity"],
                ],
            ),
            lambda cursor: cursor.fetchone(),
        )
        new_order_id = result[0]
        return new_order_id

    return insert_order


def insert_order_decoupled(
    order_data: dict,
    execute_func: Callable,
    database_connect_func: Callable,
    insert_query_builder_func: Callable,
) -> str:
    result = execute_func(
        database_connect_func,
        insert_query_builder_func(
            "orders",
            ["name", "customer_name", "quantity"],
            [order_data["name"], order_data["customer_name"], order_data["quantity"]],
        ),
        lambda cursor: cursor.fetchone(),
    )
    new_order_id = result[0]
    return new_order_id
