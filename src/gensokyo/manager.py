#!/usr/bin/env python3

from weakref import WeakValueDictionary

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
        for a in entity.get(component.Sprite):
            a.delete()

    def get_with(self, types):
        """
        Find all entities who have components of all the types and return a
        list of tuples with the following format::

            (entity, (
                (components where isinstance(component, types[0])),
                (components where isinstance(component, types[1])),
                .
                .
            ))

        You can loop over the returned list like so::

            for entity, comps in em.get_with(types):
                # setup
                # get single component
                comp = comps[0][0]
                # enumerate over many
                for comp in comps[1]:
                    # process

        """
        good = []
        for entity in self.entities:
            components = entity.get(types)
            # Check if all slots in components are filled
            if len([a for a in components if len(a) == 0]) == 0:
                good.append((entity, components))
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


class SystemManager:

    def __init__(self):
        self.systems = set()

    def add(self, system):
        self.systems.add(system)

    def __iter__(self):
        return iter(self.systems)

    def update(self, dt):
        for system in self.systems:
            system.update(dt)
