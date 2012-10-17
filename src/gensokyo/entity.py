#!/usr/bin/env python3


class Entity:

    """
    An entity represents a game object and contains components which
    encapsulate certain data.  It can have any combination of components.
    Generally an entity will only have one component per superclass, e.g., with
    A > C, it will usually have either one A or one C or neither, although in
    certain cases having more of the same component may make sense.  However,
    it may be useful to make Interface superclasses.

    """

    def __init__(self):
        self.components = set()

    def __iter__(self):
        return iter(self.components)

    def add(self, component):
        self.components.add(component)

    def delete(self, component):
        self.components.remove(component)
        if hasattr(component, 'delete'):
            component.delete()

    def get(self, types):
        """
        If types is a single type, return a tuple of components who are an
        instance of type or a subclass of type.  If types is a list of types,
        return a tuple of all components of the given types with the following
        format::

            (
                (components where isinstance(component, types[0])),
                (components where isinstance(component, types[1])),
                .
                .
            )

        Some tuples may be empty if the entity does not have those components.

        """
        try:
            return tuple([tuple([
                component for component in self if isinstance(component, type)
                ]) for type in types])
        except TypeError:
            return tuple([
                component for component in self if isinstance(component, types)
                ])
