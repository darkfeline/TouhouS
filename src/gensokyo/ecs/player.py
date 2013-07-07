# Imports {{{1
import abc
import logging
import weakref
from collections import namedtuple
from functools import partial

from pyglet.window import key

from gensokyo import ecs
from gensokyo.primitives import Vector
from gensokyo.ecs.pos import Position, SlavePosition
from gensokyo.ecs.script import Script, Scriptlet
from gensokyo.ecs.bullet import Bullet, make_bullet
from gensokyo.ecs import collision
from gensokyo.ecs import sprite

__all__ = [
    'PlayerState', 'PlayerStateSystem',
    'InputMovement', 'InputMovementSystem',
    'Shield', 'ShieldDecay',
    'Hitbox', 'HitboxMarker', 'HitboxSystem', 'make_hitbox',
    'PlayerBullet', 'make_straight_bullet',
    'LoopFireScriptlet',
    'Player', 'make_player'
]
logger = logging.getLogger(__name__)


# Base {{{1

# State {{{2
class PlayerState(ecs.Component):

    def __init__(self):
        self.focus = False


class PlayerStateSystem(ecs.System):

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            player = self.world.tm['player']
            ps = self.world.cm[PlayerState]
            state = ps[player]
            state.focus = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            player = self.world.tm['player']
            ps = self.world.cm[PlayerState]
            state = ps[player]
            state.focus = False


# Input {{{2
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
        # Calculate movement
        player = self.world.tm['player']
        pos = self.world.cm[Position][player]
        im = self.world.cm[InputMovement][player]
        ps = self.world.cm[PlayerState]
        dpos = vel * im.speed_mult
        if ps[player].focus:
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


# Hitbox {{{2
Hitbox = namedtuple("Hitbox", ['img', 'group'])


def make_hitbox(world, drawer, hitbox, pos):
    e = world.make_entity()
    add = partial(world.add_component, e)
    pos = Position(pos)
    add(pos)
    sprite_ = sprite.Sprite(pos, drawer, hitbox.group, hitbox.img)
    add(sprite_)
    return e


class HitboxMarker(SlavePosition):

    def __init__(self, master, world, hitbox):
        self.hitbox = hitbox
        self._hb_entity = None
        self._world = weakref.ref(world)
        super().__init__(master)

    def setpos(self, pos):
        self.pos = pos
        if self.hb_entity is not None:
            self.world.cm[Position][self.hb_entity].pos = pos

    @property
    def world(self):
        return self._world()

    # Note the implementation of hb_entity.  It starts as None, hence
    # the try/except in property getter, but after using once,
    # _hb_entity will be a weakref, and return None naturally if entitiy
    # is deleted.
    @property
    def hb_entity(self):
        try:
            return self._hb_entity()
        except TypeError:
            return None

    @hb_entity.setter
    def hb_entity(self, value):
        self._hb_entity = weakref.ref(value)


class HitboxSystem(ecs.System):

    def __init__(self, world, drawer):
        super().__init__(world)
        self._drawer = weakref.ref(drawer)

    @property
    def drawer(self):
        return self._drawer()

    def on_update(self, dt):
        player = self.world.tm['player']
        hbm = self.world.cm[HitboxMarker]
        ps = self.world.cm[PlayerState]
        player_marker = hbm[player]
        if player_marker.hb_entity is not None:
            if not ps[player].focus:
                self.world.remove_entity(player_marker.hb_entity)
        else:
            if ps[player].focus:
                player_marker.hb_entity = make_hitbox(
                    self.world, self.drawer, player_marker.hitbox,
                    player_marker.pos
                )


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

# Bullet {{{2
PlayerBullet = partial(Bullet, group='player_bullet')


def make_straight_bullet(world, drawer, bullet, x, y, speed):
    v = Vector(0, speed)
    return make_bullet(world, drawer, bullet, x, y, v)


# Scriptlets {{{2
class LoopFireScriptlet(Scriptlet):

    def __init__(self, rate):
        super().__init__()
        self.state = 0
        self.limit = 1 / rate

    def run(self, entity, world, master, dt):
        firing = master.rootenv.key_state[key.Z]
        if firing:
            self.state += dt
        if self.state >= self.limit:
            self.state -= self.limit
            self.fire(entity, world, master)

    @abc.abstractmethod
    def fire(self, entity, world, master):
        raise NotImplementedError

# Player {{{2
Player = namedtuple("Player", [
    'img', 'group', 'hb_img', 'hb_group', 'hitbox', 'shield_dur', 'speed_mult',
    'focus_mult', 'move_rect', 'scriptlets'
])
Player = partial(Player, group='player', hb_group='player_hb', shield_dur=3)


def make_player(world, drawer, player, x, y):

    e = world.make_entity()
    add = partial(world.add_component, e)

    pos = Position((x, y))
    add(pos)

    hb = collision.Hitbox(pos, player.hitbox.copy())
    add(hb)

    sprite_ = sprite.Sprite(pos, drawer, player.group, player.img)
    add(sprite_)

    input = InputMovement(pos, player.speed_mult, player.focus_mult,
                          player.move_rect.copy())
    add(input)

    add(PlayerState())

    add(HitboxMarker(pos, world, Hitbox(player.hb_img, player.hb_group)))

    s = Script()
    for x in player.scriptlets:
        s.add(x())
    add(s)

    return e

# }}}1

# vim: set fdm=marker:
