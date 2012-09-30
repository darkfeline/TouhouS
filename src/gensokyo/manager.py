#!/usr/bin/env python3

from gensokyo import component


class Manager:

    def __init__(self):
        self.items = set()

    def add(self, item):
        self.items.add(item)


class EntityManager(Manager):

    @property
    def entities(self):
        return self.items

    def delete(self, entity):
        self.entities.remove(entity)
        for a in entity.get(component.Sprite):
            a.delete()
