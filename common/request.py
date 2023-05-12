import azure.functions as func
from typing import Any
import logging


def response_builder(status_code: int, body: Any = None) -> func.HttpResponse:
    return func.HttpResponse(status_code=status_code, body=body)


def process_database_request(
    req: func.HttpRequest,
    get_request_data,
    extract_data_func,
    database_func,
    response_builder_func,
    status_code,
    body_builder=None,
) -> func.HttpResponse:
    req_data = get_request_data(req)
    logging.info("before extract")
    try:
        data = extract_data_func(req_data)
    except Exception as e:
        logging.warn(e)
        return response_builder_func(status_code=400)
    query_result = database_func(data)
    body = None
    if body_builder:
        body = body_builder(query_result)
    return response_builder_func(status_code, body)


def process_database_request_decoupled(
    req: func.HttpRequest,
    get_request_data,
    extract_data_func,
    extract_func,
    database_func,
    response_builder_func,
    status_code,
    execute_query_func,
    database_conn_func,
    query_build_func,
    body_builder=None,
) -> func.HttpResponse:
    req_data = get_request_data(req)
    try:
        data = extract_data_func(req_data, extract_func)
    except:
        return response_builder_func(status_code=400)
    query_result = database_func(
        data, execute_query_func, database_conn_func, query_build_func
    )
    body = None
    if body_builder:
        body = body_builder(query_result)
    return response_builder_func(status_code, body)
