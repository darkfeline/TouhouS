from gensokyo import primitives
from gensokyo.ecs.pos import Position
from gensokyo.ecs.player import Player, PlayerBullet, LoopFireScriptlet
from gensokyo.ecs.player import make_straight_bullet
from gensokyo import resources


class ReimuScriptlet(LoopFireScriptlet):

    def __init__(self):
        rate = 20
        super().__init__(rate)

    def fire(self, entity, world, master):
        speed = 50
        x, y = world.cm[Position][entity].pos
        b = make_straight_bullet(world, master.drawer, ReimuShot, x + 10, y,
                                 speed)
        world.gm['player_bullet'].add(b)
        b = make_straight_bullet(world, master.drawer, ReimuShot, x - 10, y,
                                 speed)
        world.gm['player_bullet'].add(b)


Reimu = Player(
    img=resources.player['reimu']['player'],
    hb_img=resources.player['reimu']['hitbox'],
    hitbox=primitives.Circle(0, 0, 3),
    speed_mult=10,
    focus_mult=0.5,
    move_rect=primitives.Rect(0, 0, 25, 35),
    scriptlets=(ReimuScriptlet,)
)
ReimuShot = PlayerBullet(
    img=resources.player['reimu']['shot'], dmg=20,
    hitbox=primitives.Rect(0, 0, 10, 60))

# vim: set fdm=marker:
