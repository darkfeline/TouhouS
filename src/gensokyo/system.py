#!/usr/bin/env python3

from pyglet import event

from gensokyo import component
from gensokyo import locator


class System:

    """
    Superclass for Systems

    """

    req_components = ()


class PhysicsSystem(System):

    req_components = (component.Velocity, component.Position)

    def update(self, dt):
        for entity, comps in locator.em.get_with(self.req_components):
            vs = comps[0][0]
            for i, v in enumerate(vs):
                if i == 0:
                    for p in comps[1]:
                        p.x += v.x * dt
                        p.y += v.y * dt
                else:
                    vs[i - 1].x += v.x * dt
                    vs[i - 1].y += v.y * dt


class CollisionSystem(System, event.EventDispatcher):

    req_components = (component.Hitbox,)

    def update(self, dt):
        collided = []
        entities, comps = locator.em.get_with(self.req_components)
        for i, e1 in enumerate(entities):
            hb1 = comps[i][0]
            for j, e2 in enumerate(entities[i + 1:]):
                hb2 = comps[i + j + 1][0]
                if hb1.collide(hb2):
                    collided.append((e1, e2))
        for a in collided:
            self.dispatch_event('on_collide', a)

CollisionSystem.register_event_type('on_collide')
