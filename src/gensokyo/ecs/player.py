# Imports {{{1
import abc
import logging
from collections import namedtuple
from functools import partial

from pyglet.window import key

from gensokyo import ecs
from gensokyo import primitives
from gensokyo.primitives import Vector
from gensokyo.ecs.pos import Position, SlavePosition
from gensokyo.ecs.script import Script
from gensokyo.ecs import bullet
from gensokyo.ecs import collision
from gensokyo.ecs import sprite
from gensokyo import resources

__all__ = ['InputMovement', 'InputMovementSystem']
logger = logging.getLogger(__name__)


# Base {{{1

# Input{{{2
class InputMovement(SlavePosition):

    def __init__(self, master, speed_mult, focus_mult, rect):
        self.speed_mult = speed_mult
        self.focus_mult = focus_mult
        self.rect = rect
        super().__init__(master)

    def setpos(self, pos):
        self.rect.center = pos


class InputMovementSystem(ecs.System):

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


# Shield {{{2
# TODO think this through
class Shield(ecs.Component):

    def __init__(self, dur):
        self.dur = dur
        self.state = 0

    def __bool__(self):
        if self.state > 0:
            return True
        else:
            return False


class ShieldDecay(ecs.System):

    req_components = (Shield,)

    def on_update(self, dt):
        for entity in self.env.em.get_with(self.req_components):
            for shield in entity.get(self.req_components[0]):
                if shield:
                    shield.state -= dt
                else:
                    entity.delete(shield)


# Player {{{2
Player = namedtuple("Player", [
    'img', 'group', 'hb_img', 'hb_group', 'hitbox', 'shield_dur', 'speed_mult',
    'focus_mult', 'move_rect', 'script'
])
Player = partial(Player, group='player', hb_group='player_hb', shield_dur=3)
PlayerBullet = partial(bullet.Bullet, group='player_bullet')


def make_player(world, drawer, player, x, y):

    e = world.make_entity()
    add = partial(world.add_component, e)

    pos_ = Position((x, y))
    add(pos_)

    hb = collision.Hitbox(pos_, player.hitbox.copy())
    add(hb)

    sprite_ = sprite.Sprite(pos_, drawer, player.group, player.img)
    add(sprite_)

    input = InputMovement(pos_, player.speed_mult, player.focus_mult,
                          player.move_rect.copy())
    add(input)

    add(player.script())

    return e


def make_straight_bullet(world, drawer, bullet, x, y, speed):
    v = primitives.Vector(0, speed)
    return bullet.make_bullet(world, drawer, bullet, x, y, v)


# Reimu {{{1
class LoopFireScript(Script):

    def __init__(self, rate):
        super().__init__()
        self.state = 0
        self.limit = 1 / rate

    def run(self, entity, world, root, dt):
        firing = root.key_state[key.Z]
        if firing:
            self.state += dt
        if self.state >= self.limit:
            self.state -= self.limit
            self.fire(entity, world, root)

    @abc.abstractmethod
    def fire(self, entity, world, root):
        raise NotImplementedError


class ReimuScript(LoopFireScript):

    def __init__(self):
        rate = 20
        super().__init__(rate)

    def fire(self, entity, world, root):
        speed = 50
        x, y = world.cm[Position][entity].pos
        b = make_straight_bullet(world, root.drawers, ReimuShot, x + 10, y,
                                 speed)
        world.gm['player_bullet'].append(b)
        b = make_straight_bullet(world, root.drawers, ReimuShot, x - 10, y,
                                 speed)
        world.gm['player_bullet'].append(b)


Reimu = partial(
    Player, img=resources.player['reimu']['player'],
    hb_img=resources.player['reimu']['hitbox'],
    hitbox=primitives.Circle(0, 0, 3),
    speed_mult=10,
    focus_mult=0.5,
    move_rect=primitives.Rect(0, 0, 25, 35),
    script=ReimuScript
)
ReimuShot = partial(PlayerBullet, img=resources.player['reimu']['shot'],
                    dmg=20)


# TODO add hitbox sprite
#class Player(ecs.Entity):
#
#    def on_key_press(self, symbol, modifiers):
#        if symbol == key.LSHIFT:
#            hb = self.get(PlayerHitbox)[0]
#            hb_sprite = graphics.Sprite(self.hb_sprite_img, hb.x, hb.y)
#            self.add(hb_sprite)
#            self.hb_sprite = hb_sprite
#
#    def on_key_release(self, symbol, modifiers):
#        if symbol == key.LSHIFT:
#            self.delete(self.hb_sprite)
#            del self.hb_sprite

# vim: set fdm=marker:
