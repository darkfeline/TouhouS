import abc
import logging

from pyglet.window import key

from gensokyo import ces
from gensokyo import primitives
from gensokyo.ces import script
from gensokyo.ces import bullet
from gensokyo.ces import graphics
from gensokyo.ces import collision
from gensokyo import resources
from gensokyo import locator

logger = logging.getLogger(__name__)


class BaseShifter(ces.Position):
    pass


class Shifter(BaseShifter):
    pass


class MasterShifter(BaseShifter, metaclass=abc.ABCMeta):

    """
    .. attribute:: speed_mult
    .. attribute:: focus_mult
    .. attribute:: rect

    """

    pass


class ShiftingSystem(ces.System):

    req_components = (MasterShifter,)
    opt_components = (Shifter,)

    def __init__(self, env, bounds):
        super().__init__(env)
        env.clock.push_handlers(self)
        self.bounds = bounds

    def on_update(self, dt):

        logger.debug('Shift system update')
        # Get current key state
        v = [0, 0]
        if locator.key_state[key.RIGHT]:
            v[0] += 1
        if locator.key_state[key.LEFT]:
            v[0] -= 1
        if locator.key_state[key.UP]:
            v[1] += 1
        if locator.key_state[key.DOWN]:
            v[1] -= 1
        v = primitives.Vector(*v).get_unit_vector()

        for entity in self.env.em.get_with(self.req_components):
            # Calculate movement
            master = entity.get(self.req_components[0])[0]
            start = master.pos
            dpos = v * master.speed_mult
            if master.is_focus():
                dpos *= master.focus_mult
            dpos = tuple(dpos)
            # Move master
            master.pos = tuple(start[i] + dpos[i] for i in [0, 1])
            # Calculate bounds
            if master.left < self.bounds.left:
                master.left = self.bounds.left
            elif master.right > self.bounds.right:
                master.right = self.bounds.right
            if master.bottom < self.bounds.bottom:
                master.bottom = self.bounds.bottom
            elif master.top > self.bounds.top:
                master.top = self.bounds.top
            logger.debug('Master moved to %s', master.pos)
            end = master.pos
            dpos = tuple(end[i] - start[i] for i in [0, 1])
            # Do for slaves
            for sh in entity.get(self.opt_components[0]):
                sh.pos = tuple(sh.pos[i] + dpos[i] for i in [0, 1])


class Shield(ces.Component):

    """Can have multiple"""

    def __init__(self, dur):
        self.dur = dur
        self.state = 0

    def __bool__(self):
        if self.state > 0:
            return True
        else:
            return False


class ShieldDecay(ces.System):

    req_components = (Shield,)

    def on_update(self, dt):
        for entity in self.env.em.get_with(self.req_components):
            for shield in entity.get(self.req_components[0]):
                if shield:
                    shield.state -= dt
                else:
                    entity.delete(shield)


class Player(ces.Entity):

    sprite_img = None
    sprite_group = 'player'
    hb_sprite_img = None
    hb_sprite_group = 'player_hb'
    hb = None
    shield_dur = 3

    def __init__(self, x, y):
        """
        Add firing script to complete

        """
        super().__init__()

        hb = self.hb.copy()
        hb = PlayerHitbox(hb)
        hb.pos = x, y
        self.add(hb)

        s = PlayerSprite(self.sprite_group, self.sprite_img, x=x, y=y)
        self.add(s)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            hb = self.get(PlayerHitbox)[0]
            hb_sprite = graphics.Sprite(self.hb_sprite_img, hb.x, hb.y)
            self.add(hb_sprite)
            self.hb_sprite = hb_sprite

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.delete(self.hb_sprite)
            del self.hb_sprite


class LimitedLoopFiring(script.ConditionUnit, Shifter):

    def __init__(self, pos, rate, bullet):
        super().__init__()
        self.pos = pos
        self.state = 0
        self.limit = 1 / rate
        self.bullet = bullet

    @property
    def satisfied(self):
        if self.state > self.limit:
            return True
        else:
            return False

    def run(self, entity, env):
        self.state -= self.limit
        b = self.bullet(*self.pos)
        env.em.add(b)
        env.gm.add_to('player_bullet', b)

    @staticmethod
    def is_firing():
        return locator.key_state[key.Z]

    def on_update(self, dt):
        if self.is_firing():
            self.state += dt


class PlayerHitbox(MasterShifter, collision.Hitbox):

    speed_mult = 10
    focus_mult = 0.5
    rect = primitives.Rect(0, 0, 25, 35)

    def __init__(self, hb):
        if isinstance(hb, primitives.Circle):
            pos = (hb.x, hb.y)
        elif isinstance(hb, primitives.Rect):
            pos = hb.center
        super().__init__(pos)
        self.rect = self.rect.copy()
        self.pos = pos

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, value):
        self.rect.center = value
        super(self.__class__, self.__class__).pos.fset(self, value)

    @property
    def top(self):
        return self.rect.top

    @top.setter
    def top(self, value):
        self.rect.top = value
        self.pos = self.rect.center

    @property
    def bottom(self):
        return self.rect.bottom

    @bottom.setter
    def bottom(self, value):
        self.rect.bottom = value
        self.pos = self.rect.center

    @property
    def left(self):
        return self.rect.left

    @left.setter
    def left(self, value):
        self.rect.left = value
        self.pos = self.rect.center

    @property
    def right(self):
        return self.rect.right

    @right.setter
    def right(self, value):
        self.rect.right = value
        self.pos = self.rect.center

    @staticmethod
    def is_focus():
        return locator.key_state[key.LSHIFT]


class PlayerSprite(Shifter, graphics.Sprite):
    pass


class PlayerBullet(bullet.Bullet, metaclass=abc.ABCMeta):

    sprite_group = 'player_bullet'


class ReimuShot(PlayerBullet):

    sprite_img = resources.player['reimu']['shot']
    speed = 50
    dmg = 20
    hitbox = primitives.Rect(0, 0, sprite_img.width, sprite_img.height)

    def __init__(self, x, y):
        super().__init__(x, y, primitives.Vector(0, self.speed))


class Reimu(Player):

    sprite_img = resources.player['reimu']['player']
    hb_sprite_img = resources.player['reimu']['hitbox']
    hb = primitives.Circle(0, 0, 3)

    def __init__(self, x, y):
        super().__init__(x, y)
        f = script.Script([(LimitedLoopFiring((x - 10, y), 20, ReimuShot),
                            LimitedLoopFiring((x + 10, y), 20, ReimuShot))])
        self.add(f)
