import abc
import logging

from pyglet.window import key

from gensokyo import locator
from gensokyo import ces
from gensokyo import primitives
from gensokyo.ces import script
from gensokyo.ces import bullet
from gensokyo.ces import graphics
from gensokyo.ces import collision
from gensokyo.ces import observer
from gensokyo import resources

logger = logging.getLogger(__name__)


class BaseShifter(ces.Position):
    pass


class Shifter(BaseShifter):
    pass


class MasterShifter(BaseShifter, observer.Input):

    speed_mult = 500
    focus_mult = 0.5
    rect = primitives.Rect(0, 0, 25, 35)

    def __init__(self, pos):

        self.focus = False
        self.rect = self.rect.copy()
        self.pos = pos

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, value):
        self.rect.center = value

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.focus = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.focus = False


class ShiftingSystem(ces.System, observer.Updating):

    req_components = (MasterShifter,)
    opt_components = (Shifter,)

    def __init__(self, bounds):
        self.bounds = bounds

    def set_pos(self, entity):
        pass

    def on_update(self, dt):

        # Get current key state
        v = [0, 0]
        if key[key.RIGHT]:
            v[0] += 1
        if key[key.LEFT]:
            v[0] -= 1
        if key[key.UP]:
            v[1] += 1
        if key[key.DOWN]:
            v[1] -= 1
        v = primitives.Vector(*v).get_unit_vector()

        for entity in locator.em.get_with(self.req_components):
            # Calculate movement
            master = entity.get(self.req_components[0])[0]
            start = master.pos
            dpos = v * master.speed_mult
            if master.focus:
                dpos *= master.focus_mult
            dpos = tuple(dpos)
            # Move master
            master.pos = tuple(start[i] + dpos[i] for i in [0, 1])
            # Calculate bounds
            if master.rect.left < self.bounds.left:
                master.rect.left = self.bounds.left
            elif master.rect.right > self.bounds.right:
                master.rect.right = self.bounds.right
            if master.rect.bottom < self.bounds.bottom:
                master.rect.bottom = self.bounds.bottom
            elif master.rect.top > self.bounds.top:
                master.rect.top = self.bounds.top
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


class ShieldDecay(ces.System, observer.Updating):

    req_components = (Shield,)

    def on_update(self, dt):
        for entity in locator.em.get_with(self.req_components):
            for shield in entity.get(self.req_components[0]):
                if shield:
                    shield.state -= dt
                else:
                    entity.delete(shield)


class Player(ces.Entity, observer.Input):

    sprite_img = None
    sprite_group = 'player'
    hb_sprite_img = None
    hb_sprite_group = 'player_hb'
    hb = None
    shield_dur = 3

    def __init__(self, x, y):
        """
        Add FiringUnit to complete

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


# TODO do we need this?
class FiringUnit(script.Script):
    pass


class LimitedLoopFiring(script.ConditionUnit, observer.Input, Shifter,
                        observer.Updating):

    def __init__(self, pos, rate, bullet):
        super().__init__()
        self.pos = pos
        self.state = 0
        self.limit = 1 / rate
        self.bullet = bullet
        self.is_firing = False

    @property
    def satisfied(self):
        if self.state > self.limit:
            return True
        else:
            return False

    def run(self, entity):
        self.state -= self.limit
        b = self.bullet(*self.pos)
        locator.em.add(b)
        locator.gm.add_to('player_bullet', b)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.Z:
            logger.debug("Z pressed")
            self.is_firing = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.Z:
            logger.debug("Z released")
            self.is_firing = False

    def on_update(self, dt):
        if self.is_firing:
            self.state += dt


class PlayerHitbox(collision.Hitbox, MasterShifter):
    pass


class PlayerSprite(graphics.Sprite, Shifter):
    pass


class PlayerBullet(bullet.Bullet, metaclass=abc.ABCMeta):

    sprite_group = 'player_bullet'


class ReimuShot(PlayerBullet):

    sprite_img = resources.player['reimu']['shot']
    speed = 1500
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
        f = FiringUnit([(LimitedLoopFiring((x - 10, y), 20, ReimuShot),
                        LimitedLoopFiring((x + 10, y), 20, ReimuShot))])
        self.add(f)
