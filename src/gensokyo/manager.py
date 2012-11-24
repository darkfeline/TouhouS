from weakref import WeakValueDictionary
from weakref import WeakSet
import logging

from gensokyo import ces

logger = logging.getLogger(__name__)


class EntityManager:

    def __init__(self):
        self.entities = set()

    def add(self, entity):
        logger.debug("Add entity {}".format(entity))
        self.entities.add(entity)

    def __iter__(self):
        return iter(self.entities)

    def delete(self, entity=None):
        if entity:
            self.entities.remove(entity)
            for a in entity.get(ces.Component):
                entity.delete(a)
        else:
            for entity in list(self.entities):
                self.delete(entity)

    def get_with(self, types):
        """
        Find all entities who have at least one component of each type and
        return a set of entities

        :param types: component types to look for
        :type types: tuple
        :rtype: set

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
        self.groups = {}

    def __getitem__(self, key):
        return self.groups[key]

    def make_group(self, key):
        if not key in self.groups.keys():
            self.groups[key] = WeakSet()

    def add_to(self, key, entity):
        self.groups[key].add(entity)


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
        logger.debug("Add system {}".format(system))
        self.systems.add(system)

    def __iter__(self):
        return iter(self.systems)

    def delete(self):
        for a in self.systems:
            if hasattr(a, 'delete'):
                a.delete()
