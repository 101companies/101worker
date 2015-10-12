__author__ = 'martin'


class BadIdentifierException(Exception):
    def __init__(self, identifier, message='Identifier {} does not exist'):
        self.value = message.format(identifier)

    def __str__(self):
        return repr(self.value)


class BadFragmentDescription(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Fragment description doesn\'t match a fragment'


class NonExistingPathException(Exception):
    def __init__(self, path):
        self.value = 'Path {} does not exist'.format(path)

    def __str__(self):
        return repr(self.value)


class NotReadableException(Exception):
    def __init__(self, path):
        self.value = "Can't read content from {}, because there is no geshi code assigned".format(path)