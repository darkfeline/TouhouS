import abc
import logging
from collections import namedtuple
from functools import partial

from pyglet.window import key

from gensokyo import ces
from gensokyo import primitives
from gensokyo.primitives import Vector
from gensokyo.ces.pos import Position, SlavePosition
from gensokyo.ces.script import Script
from gensokyo.ces import bullet
from gensokyo.ces import graphics
from gensokyo.ces import collision
from gensokyo.ces import sprite
from gensokyo import resources

__all__ = ['InputMovement', 'InputMovementSystem']
logger = logging.getLogger(__name__)


class InputMovement(SlavePosition):

    def __init__(self, master, speed_mult, focus_mult, rect):
        self.speed_mult = speed_mult
        self.focus_mult = focus_mult
        self.rect = rect
        super().__init__(master)

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


Player = namedtuple("Player", [
    'img', 'group', 'hb_img', 'hb_group', 'hitbox', 'shield_dur'])
Player = partial(Player, group='player')
Reimu = partial(
    Player, img=resources.player['reimu']['player'],
    hb_img=resources.player['reimu']['hitbox'],
    hitbox=primitives.Circle(0, 0, 3)
)


def make_player(world, drawer, player, x, y, *, script):

    e = world.make_entity()
    add = partial(world.add_component, e)

    pos_ = Position(x, y)
    add(pos_)

    hb = collision.Hitbox(pos_, player.hitbox.copy())
    add(hb)

    sprite_ = sprite.Sprite(pos_, drawer, player.group, player.img)
    add(sprite_)

    assert isinstance(script, Script)
    add(script)

    return e


class Player(ces.Entity):

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

    @staticmethod
    def is_focus():
        return locator.key_state[key.LSHIFT]


PlayerBullet = partial(bullet.Bullet, group='player_bullet')
ReimuShot = partial(PlayerBullet, img=resources.player['reimu']['shot'],
                    dmg=20)


def make_straight_bullet(world, drawer, bullet, x, y, speed):
    v = primitives.Vector(0, speed)
    return bullet.make_bullet(world, drawer, bullet, x, y, v)


class ReimuShot(PlayerBullet):

    speed = 50


class Reimu(Player):

    sprite_img = resources.player['reimu']['player']
    hb_sprite_img = resources.player['reimu']['hitbox']
    hb = primitives.Circle(0, 0, 3)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.add(LimitedLoopFiring((x - 10, y), 20, ReimuShot))
        self.add(LimitedLoopFiring((x + 10, y), 20, ReimuShot))
