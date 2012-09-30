#!/usr/bin/env python3

from gensokyo import component
from gensokyo import locator


class System:

    req_components = ()

    @classmethod
    def check(cls, entity):
        """Check if entity has necessary components."""
        to_check = list(cls.req_components)
        for component in entity:
            for type in to_check:
                if isinstance(entity, type):
                    to_check.remove(type)
                    break
        if len(to_check) > 0:
            return False
        else:
            return True


class PhysicsSystem(System):

    req_componenets = (component.Position, component.Velocity)

    def update(self, dt):
        for entity in [e for e in locator.em if self.check(e)]:
            vs = e.get(component.Velocity)
            for i, v in enumerate(vs):
                if i == 0:
                    for p in e.get_all(component.Position):
                        p.x += v.x * dt
                        p.y += v.y * dt
                else:
                    vs[i - 1].x += v.x * dt
                    vs[i - 1].y += v.y * dt


class CollisionSystem:

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
