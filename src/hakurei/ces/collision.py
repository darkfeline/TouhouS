#!/usr/bin/env python3

from gensokyo import primitives

from hakurei import ces


class Hitbox(ces.Position):

    def __init__(self, hb):
        self.hb = hb

    @property
    def x(self):
        if isinstance(self.hb, primitives.Circle):
            return self.hb.x
        elif isinstance(self.hb, primitives.Rect):
            return self.hb.centerx

    @x.setter
    def x(self, value):
        if isinstance(self.hb, primitives.Circle):
            self.hb.x = value
        elif isinstance(self.hb, primitives.Rect):
            self.hb.centerx = value

    @property
    def y(self):
        if isinstance(self.hb, primitives.Circle):
            return self.hb.y
        elif isinstance(self.hb, primitives.Rect):
            return self.hb.centery

    @y.setter
    def y(self, value):
        if isinstance(self.hb, primitives.Circle):
            self.hb.y = value
        elif isinstance(self.hb, primitives.Rect):
            self.hb.centery = value


class CollisionSystem(ces.System):

    req_components = (Hitbox,)

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
                for hb1 in e1.get(Hitbox):
                    for hb2 in e2.get(Hitbox):
                        if self.collide(hb1, hb2):
                            collided.append((e1, e2))
        for a in collided:
            self.sm.dispatch_event('on_collide', a)
