#!/usr/bin/env python3

# TODO move component code to EntityManager


class Entity:

    """
    An entity represents a game object and contains components which
    encapsulate certain data.  An entity may have one component per class,
    however it should only have one component per superclass, e.g., while an
    entity could both have an A component and a ASubclass component, it should
    only have either one or the other.

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
        """
        Return the component of that type.  If it doesn't exist, return the
        first component whose type is a subclass of type.  If there are still
        no components, raise TypeError.

        """
        try:
            return self.components[type]
        except KeyError:
            try:
                return self.get_all(type)[0]
            except IndexError:
                raise TypeError(
                    "{} doesn't contain a component of {}".format(self, type))

    def get_all(self, type):
        """
        Return a list of all components whose type is a subclass of type.  This
        is useful for e.g. Interfaces

        """
        a = []
        for ct, c in self.components.items():
            if issubclass(ct, type):
                a.append(c)
        return a
