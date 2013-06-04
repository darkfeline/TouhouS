import logging
import weakref

from gensokyo import master
from gensokyo.clock import Clock
from gensokyo import ecs
from gensokyo import sprite
from gensokyo import stage
from gensokyo.ecs import player
from gensokyo import ui
from gensokyo.ecs import script
from gensokyo.ecs import enemy
from gensokyo.ecs import rails
from gensokyo.ecs import collision
from gensokyo.ecs import gc
from gensokyo.ecs import physics
from gensokyo import resources
from gensokyo import globals

logger = logging.getLogger(__name__)


class GameScene(master.Scene):

    player_class = player.Reimu
    stage_class = stage.StageOne
    ui_image = resources.ui_image

    def __init__(self, rootenv):

        super().__init__(rootenv, GameDrawer())
        self.clock = Clock()
        self.world = ecs.World()
        self.stage = self.stage_class(rootenv, self.world)
        self.clock.push_handlers(self.stage)

        #######################################################################
        # UI
        # UI image
        self.ui_img = sprite.Sprite(self.drawer, 'ui', self.ui_image)
        # Counters
        self.counters = {}
        counters = {
            'high_score': (ui.TextCounter, 430, 415, 'High score', 0),
            'score': (ui.TextCounter, 430, 391, 'Score', 0),
            'lives': (ui.IconCounter, 430, 361, 'Lives', 3),
            'bombs': (ui.IconCounter, 430, 339, 'Bombs', 3)}
        for tag, a in counters.items():
            c, x, y, tit, val = a
            counter = c(self.drawer, x, y, tit, val)
            self.counters[tag] = counter
        # FPS
        self.fps = ui.FPSDisplay(self.drawer, 570, 2, rootenv.clock)
        self.clock.push_handlers(self.fps)
        logger.info('UI setup done')

        #######################################################################
        # Systems
        self.input = player.InputMovementSystem(
            self.world, rootenv.key_state, globals.GAME_AREA)
        self.clock.push_handlers(self.input)
        self.script = script.ScriptSystem(self.world, self)
        self.clock.push_handlers(self.script)
        a = GameCollisionSystem(self.world, self)
        self.clock.push_handlers(a)
        a = rails.RailSystem(self.world)
        self.clock.push_handlers(a)
        a = physics.PhysicsSystem(self.world)
        self.clock.push_handlers(a)
        a = enemy.GrimReaper(self.world)
        self.clock.push_handlers(a)
        a = gc.GarbageCollectSystem(self.world, globals.GAME_AREA)
        self.clock.push_handlers(a)
        logger.info('Systems setup done')

        #######################################################################
        # Entities
        # Player
        player_ = player.make_player(
            self.world, self.drawer, self.player_class,
            *globals.DEF_PLAYER_XY
        )
        self.world.tm['player'] = player_
        logger.info('Entities setup done')
        logger.info('Game scene setup done')

    def enter(self):
        logger.debug("Entering game")
        self.rootenv.clock.schedule(self.clock.tick)
        self.rootenv.drawers.add(self.drawer)

    def exit(self):
        logger.debug("Exiting game")
        self.rootenv.clock.unschedule(self.clock.tick)
        self.rootenv.drawers.remove(self.drawer)

    # TODO
    def kill_player(self):
        l = self.counters['lives']
        if l.value > 0:
            l.value -= 1
        else:
            self.rootenv.state.event('quit')


class GameCollisionSystem(collision.CollisionSystem):

    def __init__(self, world, scene):
        super().__init__(world)
        self.get_scene = weakref.ref(scene)

    @property
    def scene(self):
        return self.get_scene()

    def on_update(self, dt):
        pl = self.world.tm['player']
        hbs = self.world.cm[collision.Hitbox]
        pl_hb = hbs[pl]
        for b in iter(self.world.gm['enemy_bullet']):
            if pl_hb.collide(hbs[b]):
                self.scene.kill_player()
        life = self.world.cm[enemy.Life]
        for b in iter(self.world.gm['player_bullet']):
            b_hb = hbs[b]
            for e in ecs.intersect(self.world, enemy.Life):
                if b_hb.collide(hbs[e]):
                    life[e].life -= b.dmg
                    self.world.remove_entity(b)
                    break


class GameDrawer(sprite.SpriteDrawer):

    layers = (
        'player', 'player_bullet', 'player_hb', 'enemy', 'item',
        'enemy_bullet', 'ui', 'ui_element')
