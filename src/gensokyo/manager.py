#!/usr/bin/env python3

from weakref import WeakValueDictionary

from gensokyo import component


class SetManager:

    def __init__(self):
        self.items = set()

    def add(self, item):
        self.items.add(item)

    def __iter__(self):
        return iter(self.items)


class EntityManager(SetManager):

    @property
    def entities(self):
        return self.items

    def delete(self, entity):
        self.entities.remove(entity)
        for a in entity.get(component.Sprite):
            a.delete()


class MapManager:

    def __init__(self):
        self.items = WeakValueDictionary()

    def __getitem__(self, key):
        return self.items[key]


class SystemManager(SetManager):

    @property
    def systems(self):
        return self.items

    def update(self, dt):
        for system in self.systems:
            system.update(dt)
