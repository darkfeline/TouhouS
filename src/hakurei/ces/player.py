from pyglet.window import key
from gensokyo.primitives import Circle
from gensokyo import ces
from gensokyo import locator

from hakurei.object.bullet import Bullet
from hakurei.globals import GAME_AREA
from hakurei import resources


class PlayerMoveComponent(ces.Component):
    pass


class PlayerMoveSystem(ces.Component):
    pass


class PlayerInvulnComponent(ces.Component):
    pass


class PlayerInputSystem(ces.System):

    def __init__(self):
        locator.window.push_handlers(self)

    def delete(self):
        locator.window.remove_handlers(self)

    def on_key_press(self, symbol, modifiers):
        state = locator.tm['player'].get(PlayerState)[0]
        if symbol == key.LSHIFT:
            state.focus_state = 1
        elif symbol == key.Z:
            state.shooting_state = 1

    def on_key_release(self, symbol, modifiers):
        state = locator.tm['player'].get(PlayerState)[0]
        if symbol == key.LSHIFT:
            state.focus_state = 0
        elif symbol == key.Z:
            state.shooting_state = 0

    def update(self, dt):
        state = locator.tm['player'].get(PlayerState)[0]
        x, y = 0, 0
        if locator.key_state[key.LEFT]:
            x = -1
        if locator.key_state[key.RIGHT]:
            x += 1
        if locator.key_state[key.DOWN]:
            y = -1
        if locator.key_state[key.UP]:
            y += 1
        v = Vector(x, y).get_unit_vector()
        state.move_state = v


# TODO fix everything
class Player(ces.Entity):

    sprite_img = None
    sprite_group = 'player'
    hb_sprite_img = None
    hb_sprite_group = 'player_hb'
    hb = None
    die_invuln = 3
    speed_multiplier = 500
    focus_multiplier = 0.5
    shot_rate = 20

    shooting = 0
    shot_state = 0
    invuln = 0

    def __init__(self, x, y):
        super().__init__()

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
