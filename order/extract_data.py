from collections import Callable
from typing import Dict, List

from common.extract_data import extract_data_from_body


def extract_post_order_data(req_body: dict) -> dict:
    return extract_data_from_body(req_body, ["name", "customer_name", "quantity"])


def extract_post_order_data_decoupled(
    req_body: dict, extract_func: Callable[[Dict, List], Dict]
) -> dict:
    return extract_func(req_body, ["name", "customer_name", "quantity"])


def extract_curry(extract_func: Callable[[Dict, List], Dict]) -> Callable:
    def extract_post_order_data_curried(req_body: dict) -> dict:
        return extract_func(req_body, ["name", "customer_name", "quantity"])

    return extract_post_order_data_curried
