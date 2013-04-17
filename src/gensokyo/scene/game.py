import logging

from gensokyo import state
from gensokyo.clock import Clock
from gensokyo import ces
from gensokyo import sprite
from gensokyo.ces import player
from gensokyo import ui
from gensokyo.ces import script
from gensokyo.ces import enemy
from gensokyo.ces import rails
from gensokyo.ces import collision
from gensokyo.ces import gc
from gensokyo.ces import physics
from gensokyo import resources
from gensokyo import globals

logger = logging.getLogger(__name__)


class GameScene(state.State):

    player_class = player.Reimu
    stage_class = None
    ui_image = resources.ui_image

    def __init__(self, rootenv):

        self.graphics = GameDrawer()
        self.clock = Clock()
        self.world = ces.World()

        # TODO
        # FPS
        fps = ui.FPSDisplay(570, 2)
        self.em.add(fps)
        self.tm.tag('fps_display', fps)
        # Counters
        counters = {
            'high_score': (ui.TextCounter, 430, 415, 'High score'),
            'score': (ui.TextCounter, 430, 391, 'Score'),
            'lives': (ui.IconCounter, 430, 361, 'Lives'),
            'bombs': (ui.IconCounter, 430, 339, 'Bombs')}
        for tag, a in counters.items():
            c, x, y, tit = a
            counter = c(x, y, tit)
            self.em.add(counter)
            self.tm.tag(tag, counter)
        # Stage
        self.em.add(self.stage_class())
        #######################################################################
        # UI
        # UI image
        self.ui_img = sprite.Sprite(self.graphics, 'ui', self.ui_image)

        #######################################################################
        # Systems
        a = player.InputMovementSystem(self.world, globals.GAME_AREA)
        self.input = a
        self.clock.push_handlers(a)
        a = script.ScriptSystem(self.world)
        self.script = a
        self.clock.push_handlers(a)
        a = GameCollisionSystem(self.world)
        self.clock.push_handlers(a)
        a = rails.RailSystem(self.world)
        self.clock.push_handlers(a)
        a = physics.PhysicsSystem(self.world)
        self.clock.push_handlers(a)
        a = enemy.GrimReaper(self.world)
        self.clock.push_handlers(a)
        a = gc.GarbageCollectSystem(self.world, globals.GAME_AREA)
        self.clock.push_handlers(a)

        #######################################################################
        # Entities
        # Player
        player_ = player.make_player(
            self.world, self.drawer, self.player_class(),
            *globals.DEF_PLAYER_XY
        )
        self.world.tm['player'] = player_

    def enter(self, rootenv):
        logger.debug("Entering game")
        rootenv.clock.push_handlers(on_update=self.clock.tick)
        rootenv.drawers.push(self.graphics)
        self.input.key_state = rootenv.key_state
        self.script.rootenv = rootenv

    def exit(self, rootenv):
        logger.debug("Exiting game")
        rootenv.clock.remove_handlers(on_update=self.clock.tick)
        rootenv.drawers.remove(self.graphics)
        self.input.key_state = None
        self.script.rootenv = None


class GameCollisionSystem(collision.CollisionSystem):

    def on_update(self, dt):
        pl = self.world.tm['player']
        hbs = self.world.cm[collision.Hitbox]
        pl_hb = hbs[pl]
        for b in iter(self.world.gm['enemy_bullet']):
            if pl_hb.collide(hbs[b]):
                kill_player()
        life = self.world.cm[enemy.Life]
        for b in iter(self.world.gm['player_bullet']):
            b_hb = hbs[b]
            for e in ces.intersect(self.world, enemy.Life):
                if b_hb.collide(hbs[e]):
                    life[e].life -= b.dmg
                    self.world.remove_entity(b)
                    break


class GameDrawer(sprite.SpriteDrawer):

    map = ('player', 'player_bullet', 'player_hb', 'enemy', 'item',
           'enemy_bullet', 'ui', 'ui_element')


# TODO
def kill_player():
    l = locator.tm['lives']
    if l.value > 0:
        l.value -= 1
    else:
        locator.scene_stack.pop()
