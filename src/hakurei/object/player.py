#!/usr/bin/env python3

from pyglet.window import key
from gensokyo.primitives import Vector, Circle

from hakurei.object.bullet import Bullet
from hakurei.globals import GAME_AREA
from hakurei import resources

class PlayerInputComponent(InputComponent):

    def update(self, dt):
        x = 0
        if locator.key_state[key.LEFT]:
            x = -1
        if locator.key_state[key.RIGHT]:
            x += 1
        y = 0
        if locator.key_state[key.DOWN]:
            y = -1
        if locator.key_state[key.UP]:
            y += 1
        v = Vector(x, y).get_unit_vector()
        self.dispatch_event('on_set_vdir', v)

    def key_press(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.dispatch_event('on_set_state', 1)
        elif symbol == key.Z:
            self.shooting = 1

    def key_release(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.dispatch_event('on_set_state', 0)
        elif symbol == key.Z:
            self.shooting = 0

PlayerInputComponent.register_event_type('on_set_state')
PlayerInputComponent.register_event_type('on_set_vdir')


class PlayerPhysicsComp(MultiSplitPhysicsComp):

    speeds = (0, 0)

    def on_set_vdir(self, vector):
        self.vdir = vector

    def on_set_state(self, state):
        self.state = state


class Player(Container):

    sprite_img = None
    sprite_group = 'player'
    hb_img = None
    hb_group = 'player_hb'
    die_invuln = 3

    def __init__(self, x, y, hb=None):

        super().__init__()

        p = PlayerPhysicsComp()
        c = EnemyCollisionComponent(x, y, self.sprite_img.width,
                self.sprite_img.height, self.hb)
        g = SpriteComponent(self.sprite_group, img=self.sprite_img)

        p.speed = 0
        p.accel = 100
        p.max_speed = 300

        p.push_handlers(g)
        p.push_handlers(c)
        c.push_handlers(g)
        c.push_handlers(self)

        self.add(p)
        self.add(c)
        self.add(g)


        super().__init__(x, y, hb=hb)
        PlayerInputComponent.__init__(self)
        self._focus = 0
        self.speed_multiplier = 500
        self.focus_multiplier = 0.5
        self.shooting = 0
        self.shot_rate = 20
        self.shot_state = 0
        self.bullets = BulletGroup()
        self.invuln = 0
        self.v = Vector(0, 0)
        self.hbsprite = None

    @property
    def x(self):
        return super().x

    @x.setter
    def x(self, value):
        super(type(self), type(self)).x.fset(self, value)
        if hasattr(self, 'hbsprite') and self.hbsprite is not None:
            self.hbsprite.x = value

    @property
    def y(self):
        return super().y

    @y.setter
    def y(self, value):
        super(type(self), type(self)).y.fset(self, value)
        if hasattr(self, 'hbsprite') and self.hbsprite is not None:
            self.hbsprite.y = value

    @property
    def speed(self):
        if self.focus:
            return self.speed_multiplier * self.focus_multiplier
        else:
            return self.speed_multiplier

    @speed.setter
    def speed(self, value):
        self.speed_multiplier = value

    @property
    def focus(self):
        return int(self._focus)

    @focus.setter
    def focus(self, value):
        f = self.focus
        v = bool(value)
        if f != v:
            self._focus = v
            if v:
                self.hbsprite = Sprite(self.hb_img, self.x, self.y)
                self.add_sprite(self.hbsprite, self.hb_group)
            else:
                self.hbsprite.delete()
                self.hbsprite = None

    def die(self):
        if self.invuln > 0:
            return 1
        else:
            self.invuln += Player.die_invuln
            return 0

    def update(self, dt):
        super().update(dt)
        PlayerInputComponent.update(self, dt)
        # bound movement
        if self.right > GAME_AREA.right:
            self.right = GAME_AREA.right
        elif self.left < GAME_AREA.left:
            self.left = GAME_AREA.left
        if self.bottom < GAME_AREA.bottom:
            self.bottom = GAME_AREA.bottom
        elif self.top > GAME_AREA.top:
            self.top = GAME_AREA.top
        # invuln
        if self.invuln > 0:
            self.invuln -= dt
        # bullet generation
        if self.shooting:
            self.shot_state += dt
            self.update_fire(dt)
        # bullet update
        self.bullets.update(dt)

    def update_fire(self, dt):
        pass


class ReimuShot(Bullet):

    sprite_img = resources.player['reimu']['shot']

    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 1500
        self.dmg = 20
        self.hb = self.rect


class Reimu(Player):

    sprite_img = resources.player['reimu']['player']
    hb_img = resources.player['reimu']['hitbox']

    def __init__(self, x, y, hb=None):
        super().__init__(x, y)
        self.hb = Circle(self.x, self.y, 3)
        self.speed_multiplier = 500
        self.focus_multiplier = .5
        self.shot_rate = 20

    def update_fire(self, dt):
        period = 1 / self.shot_rate  # period of shot
        i = 0
        while self.shot_state > period:
            shot = ReimuShot(x=self.x - 10, y=self.bottom)
            shot.update(i)
            self.bullets.add(shot)
            shot = ReimuShot(x=self.x + 10, y=self.bottom)
            shot.update(i)
            self.bullets.add(shot)
            self.shot_state -= period
            i += period
