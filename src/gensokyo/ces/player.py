import abc
import logging

from pyglet.window import key

from gensokyo import ces
from gensokyo import primitives
from gensokyo.primitives import Vector
from gensokyo.ces.pos import Position, SlavePosition
from gensokyo.ces import script
from gensokyo.ces import bullet
from gensokyo.ces import graphics
from gensokyo.ces import collision
from gensokyo import resources

__all__ = ['InputMovement']
logger = logging.getLogger(__name__)


class InputMovement(SlavePosition):

    def __init__(self, speed_mult, focus_mult, rect):
        self.speed_mult = speed_mult
        self.focus_mult = focus_mult
        self.rect = rect

    def setpos(self, pos):
        self.rect.center = pos


class InputMovementSystem(ces.System):

    def __init__(self, world, key_state, bounds):
        super().__init__(world)
        self.key_state = key_state
        self.bounds = bounds

    def on_update(self, dt):
        # get keys
        vel = [0, 0]
        if self.key_state[key.RIGHT]:
            vel[0] += 1
        if self.key_state[key.LEFT]:
            vel[0] -= 1
        if self.key_state[key.UP]:
            vel[1] += 1
        if self.key_state[key.DOWN]:
            vel[1] -= 1
        vel = Vector(*vel).get_unit_vector()
        focus = True if self.key_state[key.LSHIFT] else False
        # Calculate movement
        player = self.word.tm['player']
        pos = self.world.cm[Position][player]
        im = self.world.cm[InputMovement][player]
        dpos = vel * im.speed_mult
        if focus:
            dpos *= im.focus_mult
        # Move
        pos.pos = tuple(Vector(*pos.pos) + Vector(*dpos))
        im.setpos(pos.pos)
        # Calculate bounds/fix
        if im.rect.left < self.bounds.left:
            im.rect.left = self.bounds.left
        elif im.rect.right > self.bounds.right:
            im.rect.right = self.bounds.right
        if im.rect.bottom < self.bounds.bottom:
            im.rect.bottom = self.bounds.bottom
        elif im.rect.top > self.bounds.top:
            im.rect.top = self.bounds.top
        pos.pos = im.rect.center
        logger.debug('Master moved to %s', pos.pos)


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


class LimitedLoopFiring(script.Script, Shifter):

    def __init__(self, pos, rate, bullet):
        super().__init__()
        self.pos = pos
        self.state = 0
        self.limit = 1 / rate
        self.bullet = bullet

    def run(self, entity, env, dt):
        if self.is_firing():
            self.state += dt
        if self.state >= self.limit:
            self.state -= self.limit
            b = self.bullet(*self.pos)
            env.em.add(b)
            env.gm.add_to('player_bullet', b)

    @staticmethod
    def is_firing():
        return locator.key_state[key.Z]


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
        self.add(LimitedLoopFiring((x - 10, y), 20, ReimuShot))
        self.add(LimitedLoopFiring((x + 10, y), 20, ReimuShot))
