class NetworkError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UnsupportedFormatError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ConfigurationError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
