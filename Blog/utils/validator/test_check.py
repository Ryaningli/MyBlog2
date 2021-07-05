from hard.validator import validate_scheme


class Checker:
    def __init__(self, scheme, data):
        self.scheme = scheme
        self.data = data
        self.is_valid = True
        self.error_message = None
        checker = getattr(validate_scheme, self.scheme)()
        result = checker.__get_result__(self.data)
        self.is_valid = result['is_valid']
        self.error_message = result['error_message']
