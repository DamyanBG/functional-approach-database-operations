import azure.functions as func
import json


from .db import insert_order, insert_order_decoupled, insert_order_curry
from common.request import (
    process_database_request,
    response_builder,
    process_database_request_decoupled,
)
from common.extract_data import extract_data_from_body
from common.database import database_connect, execute_query, insert_query_builder
from .extract_data import (
    extract_post_order_data,
    extract_post_order_data_decoupled,
    extract_curry,
)


# using coupled functions
def _post_order_coupled(req: func.HttpRequest) -> func.HttpResponse:
    """
    I would use this approach. It is more cleaner"""
    response = process_database_request(
        req,
        lambda req: req.get_json(),
        extract_post_order_data,
        insert_order,
        response_builder,
        201,
        lambda id: json.dumps({"id": id}),
    )
    return response


# using lambda to decouple the logic
def _post_order_lambda_decoupled(req: func.HttpRequest) -> func.HttpResponse:
    response = process_database_request(
        req,
        lambda req: req.get_json(),
        lambda req_body: extract_data_from_body(
            req_body, ["name", "customer_name", "quantity"]
        ),
        lambda order_data: execute_query(
            database_connect,
            insert_query_builder(
                "orders",
                ["name", "customer_name", "quantity"],
                [
                    order_data["name"],
                    order_data["customer_name"],
                    order_data["quantity"],
                ],
            ),
            lambda cursor: cursor.fetchone(),
        ),
        response_builder,
        201,
        lambda id: json.dumps({"id": id}),
    )

    return response


# using currying to decouple the logic
def _post_order_curry_decoupled(req: func.HttpRequest) -> func.HttpResponse:
    """
    Would use this one too!"""
    response = process_database_request(
        req,
        lambda req: req.get_json(),
        extract_curry(extract_data_from_body),
        insert_order_curry(execute_query, database_connect, insert_query_builder),
        response_builder,
        201,
        lambda id: json.dumps({"id": id}),
    )

    return response


# using decoupled process func
def _post_order_decoupled(req: func.HttpRequest) -> func.HttpResponse:
    response = process_database_request_decoupled(
        req,
        lambda req: req.get_json(),
        extract_post_order_data_decoupled,
        extract_data_from_body,
        insert_order_decoupled,
        response_builder,
        201,
        execute_query,
        database_connect,
        insert_query_builder,
        lambda id: json.dumps({"id": id}),
    )

    return response


def main(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    action = req.params.get("action")

    if method == "POST":
        if action == "post_order_coupled":
            return _post_order_coupled(req)
        elif action == "post_order_lambda_decoupled":
            return _post_order_lambda_decoupled(req)
        elif action == "post_order_decoupled":
            return _post_order_decoupled(req)
        elif action == "post_order_curry_decoupled":
            return _post_order_curry_decoupled(req)

    return response_builder(404)
