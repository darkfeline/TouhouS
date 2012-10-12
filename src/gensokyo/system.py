#!/usr/bin/env python3

import abc

from gensokyo import component
from gensokyo import locator


class System:

    """
    Superclass for Systems

    """

    __metaclass__ = abc.ABCMeta


class PhysicsSystem(System):

    req_components = (component.Velocity, component.Position)

    def update(self, dt):
        for entity in locator.em.get_with(self.req_components):
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
        :param t1, t2: hitboxes to compare
        :type t1, t2: tuple of hitbox components
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
        entities, comps = locator.em.get_with(self.req_components)
        for i, e1 in enumerate(entities):
            for j, e2 in enumerate(entities[i + 1:]):
                if self.collide(comps[i], comps[i + j + 1]):
                    collided.append((e1, e2))
        for a in collided:
            locator.model.sm.dispatch_event('on_collide', a)
