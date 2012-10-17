#!/usr/bin/env python3

import abc

from gensokyo import component
from gensokyo import locator


class System:

    """
    Superclass for Systems

    """

    __metaclass__ = abc.ABCMeta

    @staticmethod
    def get_with(types):
        """
        :param types: component types to look for
        :type types: tuple
        :rtype: set

        """
        return locator.model.em.get_with(types)

    @staticmethod
    def dispatch_event(event, *args):
        """
        :param event: event
        :type event: str

        """
        locator.sm.dispatch_event(event, *args)


class PhysicsSystem(System):

    req_components = (component.Velocity, component.Position)

    def update(self, dt):
        """
        For all entities with Velocity and Position components, PhysicsSystem
        applies ALL velocities to ALL positions

        """
        for entity in self.get_with(self.req_components):
            vel, pos = entity.get(self.req_components)
            for v in vel:
                for i in range(len(v)):
                    if i == 0:
                        for p in pos:
                            p.x += v[0].x * dt
                            p.y += v[0].y * dt
                    else:
                        v[i - 1].x += v[i].x * dt
                        v[i - 1].y += v[i].y * dt


class CollisionSystem(System):

    req_components = (component.Hitbox,)

    @staticmethod
    def collide(hb1, hb2):
        """
        :param t1: hitboxes to compare
        :param t2: hitboxes to compare
        :type t1: tuple
        :type t2: tuple
        :rtype: boolean

        """
        for i in range(len(hb1)):
            for j in range(len(hb2)):
                if hb1[i].collide(hb2[j]):
                    return True
        return False

    def update(self, dt):
        """
        Compare ALL of the hitboxes of entities with a hitbox component.  If
        any of them collide, have the SystemManager dispatch on_collide event
        with a tuple containing the two entities as an argument.

        """
        collided = []
        entities = self.get_with(self.req_components)
        for i, e1 in enumerate(entities):
            for e2 in enumerate(entities[i + 1:]):
                for hb1 in e1.get(component.Hitbox):
                    for hb2 in e2.get(component.Hitbox):
                        if self.collide(hb1, hb2):
                            collided.append((e1, e2))
        for a in collided:
            self.sm.dispatch_event('on_collide', a)
