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

    req_componenets = (component.Hitbox,)

    def update(self, dt):
        collided = []
        entities = [e for e in locator.em if self.check(e)]
        for i, e1 in enumerate(entities):
            for e2 in entities[i + 1:]:
                hb1 = e1.get(component.Hitbox)
                hb2 = e2.get(component.Hitbox)
                if hb1.collide(hb2):
                    collided.append((e1, e2))
        for a in collided:
            self.dispatch_event('on_collide', a)

CollisionSystem.register_event_type('on_collide')
