#!/usr/bin/env python3

from weakref import WeakValueDictionary

from pyglet import event

from gensokyo import component


class EntityManager:

    def __init__(self):
        self.entities = set()

    def add(self, entity):
        self.entities.add(entity)

    def __iter__(self):
        return iter(self.entities)

    def delete(self, entity):
        self.entities.remove(entity)
        for a in entity.get(component.Component):
            entity.delete(a)

    def get_with(self, types):
        """
        Find all entities who have at least one component of each type and
        return a set of entities

        """
        good = set()
        for entity in self.entities:
            components = entity.get(types)
            # Check if all slots in components are filled
            if len([a for a in components if len(a) == 0]) == 0:
                good.add(entity)
        return good


class GroupManager:

    def __init__(self):
        self.groups = WeakValueDictionary()

    def __getitem__(self, key):
        return self.groups[key]

    def make_group(self, key):
        if not key in self.groups.keys():
            self.groups[key] = set()

    def add_to(self, key, entity):
        self.items[key].add(entity)


class TagManager:

    def __init__(self):
        self.items = WeakValueDictionary()

    def __getitem__(self, key):
        return self.items[key]

    def tag(self, key, entity):
        self.items[key] = entity


class SystemManager(event.EventManager):

    def __init__(self):
        self.systems = set()

    def add(self, system):
        self.systems.add(system)
        self.push_handlers(system)

    def __iter__(self):
        return iter(self.systems)

    def update(self, dt):
        for system in self.systems:
            if hasattr(system, 'update'):
                system.update(dt)
