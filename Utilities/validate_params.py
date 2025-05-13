def is_filled(value):
    """
    Checks if a value is considered 'filled'.
    Returns False for None, empty strings, empty lists, empty dicts, etc.
    """
    return not (value in [None, '', [], {}, ()])

def validate_request_body(data, path='', optional_keys=None):
    """
    Recursively validates all required values in a nested dictionary.
    Optional keys: if present, must be valid. If missing or empty, they are skipped.
    """
    if optional_keys is None:
        optional_keys = set()

    missing_fields = []

    for key, value in data.items():
        current_path = f"{path}.{key}" if path else key

        if isinstance(value, dict):
            missing_fields.extend(validate_request_body(value, current_path, optional_keys))
        else:
            if isinstance(value, str):
                value = value.strip()

            if current_path in optional_keys:
                if is_filled(value):  # optional and has a value → must be valid
                    continue
                else:
                    continue  # optional and empty → skip
            else:
                if not is_filled(value):
                    missing_fields.append(current_path)

    return missing_fields



