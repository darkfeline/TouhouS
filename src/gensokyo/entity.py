#!/usr/bin/env python3

class Entity:

    """
    Entity
    Contains Components

    Keeps a reference to components to keep alive.
    Propagates updates to components with update method.

    """

    def __init__(self):
        self.components = set()

    def add(self, component):
        self.components.add(component)

    def has(self, type):
        for a in self.components:
            if isinstance(a, type):
                return True
        return False

    def get(self, type):
        x = []
        for a in self.components:
            if isinstance(a, type):
                x.append(a)
        return x
