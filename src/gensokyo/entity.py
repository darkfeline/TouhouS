#!/usr/bin/env python3


class Entity:

    """
    Entity
    Contains Components

    """

    def __init__(self):
        self.components = set()

    def __iter__(self):
        return iter(self.components)

    def add(self, component):
        self.components.add(component)

    def get(self, type):
        x = []
        for a in self.components:
            if isinstance(a, type):
                x.append(a)
        return x
