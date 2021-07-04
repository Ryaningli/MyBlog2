class ValidateBase:
    def __get_result__(self, data):
        result = None
        for key in self.__dir__():
            if not key.startswith('_'):
                # value = data.__getattr__(key)
                value = data[key]
                result = getattr(self, key)(value)
                if not result['is_valid']:
                    return result
        return result
