import logging
import weakref

from gensokyo import state
from gensokyo.master import Master
from gensokyo.clock import Clock
from gensokyo import sprite
from gensokyo import ui
from gensokyo import ecs
from gensokyo.ecs import player
from gensokyo.ecs import script
from gensokyo.ecs import enemy
from gensokyo.ecs import bullet
from gensokyo.ecs import rails
from gensokyo.ecs import collision
from gensokyo.ecs import gc
from gensokyo.ecs import physics
from gensokyo.data.players.reimu import Reimu
from gensokyo import resources
from gensokyo import globals

logger = logging.getLogger(__name__)


class GameScene(state.State, Master):

    player_class = Reimu
    ui_image = resources.ui_image

    def __init__(self, master, stage_class):

        super().__init__(master)
        self._drawer = GameDrawer()
        self._clock = Clock()
        self.world = ecs.World()
        self.stage = stage_class(self.world, self)
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
        self.fps = ui.FPSDisplay(self.drawer, 570, 2, self.rootenv.clock)
        self.clock.push_handlers(self.fps)
        logger.info('UI setup done')

        #######################################################################
        # Systems
        a = player.InputMovementSystem(
            self.world, self.rootenv.key_state, globals.GAME_AREA)
        self.clock.push_handlers(a)

        self.ps_system = player.PlayerStateSystem(self.world)

        a = script.ScriptSystem(self.world, self)
        self.clock.push_handlers(a)

        a = player.HitboxSystem(self.world, self.drawer)
        self.clock.push_handlers(a)

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

        del a
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
        self.master.clock.add_clock(self.clock)
        self.master.drawer.add(self.drawer)
        self.rootenv.window.push_handlers(self.ps_system)

    def exit(self):
        logger.debug("Exiting game")
        self.master.clock.remove_clock(self.clock)
        self.master.drawer.remove(self.drawer)
        self.rootenv.window.remove_handlers(self.ps_system)

    def kill_player(self):
        l = self.counters['lives']
        if l.value > 0:
            l.value -= 1
        else:
            self.master.event('quit')


class GameCollisionSystem(collision.CollisionSystem):

    def __init__(self, world, scene):
        super().__init__(world)
        self._scene = weakref.ref(scene)

    @property
    def scene(self):
        return self._scene()

    def on_update(self, dt):
        player = self.world.tm['player']
        hb = self.world.cm[collision.Hitbox]
        player_hitbox = hb[player]
        for b in iter(self.world.gm['enemy_bullet']):
            if player_hitbox.collide(hb[b]):
                self.scene.kill_player()
                self.world.remove_entity(b)
        life = self.world.cm[enemy.Life]
        dmg = self.world.cm[bullet.Damage]
        for b in iter(self.world.gm['player_bullet']):
            bullet_hitbox = hb[b]
            for e in ecs.intersect(self.world, enemy.Life):
                if bullet_hitbox.collide(hb[e]):
                    life[e].life -= dmg[b].dmg
                    self.world.remove_entity(b)
                    break


class GameDrawer(sprite.SpriteDrawer):

    def __init__(self):
        super().__init__((
            'player', 'player_bullet', 'player_hb', 'enemy', 'item',
            'enemy_bullet', 'ui', 'ui_element'))
