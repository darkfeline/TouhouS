from gensokyo import ces
from gensokyo import primitives
from gensokyo import locator


class Physics(ces.Component):

    """
    Physics component.

    .. attribute: vel
        velocity
    .. attribute: acc
        acceleration

    """

    def __init__(self, vel=None):
        if vel is None:
            self.vel = primitives.Vector(0, 0)
        elif isinstance(vel, primitives.Vector):
            self.vel = vel
        else:
            raise TypeError
        self.acc = primitives.Vector(0, 0)

    @property
    def speed(self):
        return self.vel.length


class PhysicsSystem(ces.System):

    req_components = (Physics, ces.Position)

    def update(self, dt):
        for entity in locator.em.get_with(self.req_components):
            phys, pos = entity.get(self.req_components)
            for phy in phys:
                for p in pos:
                    p.x += phy.vel.x
                    p.y += phy.vel.y
                phy.vel += phy.acc
