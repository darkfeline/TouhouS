#!/usr/bin/env python3


class Entity:

    """
    An entity represents a game object and contains components which
    encapsulate certain data.  An entity should only have one component per
    superclass, e.g., it should have either an A component or an
    ASubclass component, not both.

    """

    def __init__(self):
        self.components = set()

    def __iter__(self):
        return iter(self.components)

    def add(self, component):
        self.components.add(component)
