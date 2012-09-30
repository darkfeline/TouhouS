#!/usr/bin/env python3


class Entity:

    """
    Entity
    Contains Components

    """

    def __init__(self):
        self.components = {}

    def __iter__(self):
        return iter(self.components)

    def add(self, component):
        if type(component) in self.components.keys():
            return
        self.components[type(component)] = component

    def get(self, type):
        """Return the component of that type"""
        return self.components[type]

    def get_all(self, type):
        """Return a list of all components whose type is a subclass of type"""
        a = []
        for ct, c in self.components.items():
            if issubclass(ct, type):
                a.append(c)
        return a
