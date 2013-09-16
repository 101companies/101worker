__author__ = 'martin'


class Person:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()