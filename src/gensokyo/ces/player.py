from pyglet.window import key

from gensokyo.primitives import Circle, Vector
from gensokyo import locator
from gensokyo import ces
from gensokyo.ces import Position
from gensokyo.ces.bullet import Bullet
from gensokyo.ces.graphics import Sprite
from gensokyo.globals import GAME_AREA
from gensokyo import resources


class PlayerState(ces.Component):

    die_invuln = 3
    speed_mult = 500
    focus_mult = 0.5
    edge_bound = 25

    def __init__(self):

        self.focus_state = 0
        self.shooting_state = 0
        self.invuln_state = 0
        self.move_state = Vector(0, 0)


class BulletGen(ces.Position):

    shot_rate = 20

    def __init__(self, bullet):
        """
        :param bullet: bullet constructor
        :type bullet: callable returning bullet

        """
        self.bullet = bullet
        self.shot_state = 0


class PlayerBulletGenSystem(ces.System):

    sprite_group = 'player_bullet'

    def update(self, dt):
        player = locator.sm['player']
        state = player.get(PlayerState)[0]
        if state.shooting_state:
            p = player.get(Position)[0]
            for gen in player.get(BulletGen):
                gen.shot_state += dt
                if gen.shot_state >= gen.shot_rate:
                    b = gen.bullet(p.x, p.y)
                    locator.sm.dispatch_event(
                        'on_add_sprite', b, self.sprite_group)


class PlayerUpdateSystem(ces.System):

    def update(self, dt):

        player = locator.sm['player']
        state = player.get(PlayerState)[0]

        # movement
        ps = player.get(Position)
        p = ps[0]
        cur = Vector(p.x, p.y)
        v = state.move_state * (state.speed_mult * dt)
        if state.focus_state:
            v *= state.focus_state
        x, y = cur + v
        # bound movement
        left = GAME_AREA.left + state.edge_bound
        right = GAME_AREA.right - state.edge_bound
        if x < left:
            x = left
        elif x > right:
            x = right
        top = GAME_AREA.top + state.edge_bound
        bottom = GAME_AREA.bottom - state.edge_bound
        if y < bottom:
            y = bottom
        elif y > top:
            y = top
        # move stuff
        for p in ps:
            p.x, p.y = x, y

        # invuln
        if state.invuln_state > 0:
            state.invuln_state -= dt


class PlayerInputSystem(ces.System):

    def __init__(self):
        locator.window.push_handlers(self)

    def delete(self):
        locator.window.remove_handlers(self)

    def on_key_press(self, symbol, modifiers):
        player = locator.tm['player']
        state = player.get(PlayerState)[0]
        if symbol == key.LSHIFT:
            p = player.get(Position)[0]
            state.focus_state = 1
            hb = Sprite(player.hb_sprite_img, p.x, p.y)
            locator.sm.dispatch_event(
                'on_add_sprite', hb, player.hb_sprite_group)
            player.add(hb)
            player.hb_sprite = hb
        elif symbol == key.Z:
            state.shooting_state = 1

    def on_key_release(self, symbol, modifiers):
        player = locator.tm['player']
        state = player.get(PlayerState)[0]
        if symbol == key.LSHIFT:
            state.focus_state = 0
            player.delete(player.hb_sprite)
            del player.hb_sprite
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


class Player(ces.Entity):

    sprite_img = None
    sprite_group = 'player'
    hb_sprite_img = None
    hb_sprite_group = 'player_hb'
    hb = None

    def __init__(self, x, y):
        super().__init__()

        # TODO components

    # TODO move this to... somewhere
    def die(self):
        if self.invuln > 0:
            return 1
        else:
            self.invuln += Player.die_invuln
            return 0


# TODO fix
class ReimuShot(Bullet):

    sprite_img = resources.player['reimu']['shot']

    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 1500
        self.dmg = 20
        self.hb = self.rect


# TODO fix
class Reimu(Player):

    sprite_img = resources.player['reimu']['player']
    hb_sprite_img = resources.player['reimu']['hitbox']

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
