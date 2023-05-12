def extract_data_from_body(req_body: dict, keys: list) -> dict:
    data = {}
    for key in keys:
        data[key] = req_body[key]
    return data
