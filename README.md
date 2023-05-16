# Functional approach of common API problem - handling HTTP request followed by database operation

Here I implemented 4 ways of functional programming. You can find them in `./order/__init__.py` . There is the main logic behind the idea. The database higher order functions are in ./common/database.py .

## The first approach includes coupled functions:

### Using coupled functions

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


## The second approach uses decoupled functions and using lamda functions.

### Using lambda to decouple the logic
def _post_order_lambda_decoupled(req: func.HttpRequest) -> func.HttpResponse:
    response = process_database_request(
        req,
        lambda req: req.get_json(),
        lambda req_body: extract_data_from_body(
            req_body, ["name", "customer_name", "quantity"]
        ),
        lambda order_data: execute_query(
            database_connect,
            save_insert_query_builder(
                "orders",
                (
                    "name",
                    "customer_name",
                    "quantity",
                ),
                (
                    order_data["name"],
                    order_data["customer_name"],
                    order_data["quantity"],
                ),
            ),
            lambda cursor: cursor.fetchone(),
        ),
        response_builder,
        201,
        lambda id: json.dumps({"id": id}),
    )

    return response

## The third approach is implemented with the currying technique.

### Using currying to decouple the logic
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

## The last approachs is using higher order decoupled functions.

### using decoupled process func
```def _post_order_decoupled(req: func.HttpRequest) -> func.HttpResponse:
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
```