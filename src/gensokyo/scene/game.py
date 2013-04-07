import logging

from gensokyo import state
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

    def __init__(self):

        super().__init__()

        self.graphics = GameDrawer()

        # Systems
        ui.FPSSystem(self)
        player.ShiftingSystem(self, globals.GAME_AREA)
        player.ShieldDecay(self)
        script.ScriptSystem(self)
        enemy.GrimReaper(self)
        rails.RailSystem(self)
        physics.PhysicsSystem(self)
        gc.GarbageCollectSystem(self, globals.GAME_AREA)

        # Groups
        self.gm.make_group('enemy_bullet')
        self.gm.make_group('enemy')
        self.gm.make_group('player_bullet')

        #######################################################################
        # Entities
        #######################################################################
        # UI image
        bg = ces.Entity()
        bg.add(graphics.Sprite('ui', self.ui_image))
        self.em.add(bg)
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
        # Player
        player_ = self.player_class(*globals.DEF_PLAYER_XY)
        self.em.add(player_)
        self.tm.tag('player', player_)

    def enter(self):
        logger.debug("Entering game")
        locator.clock.push_handlers(on_update=self.clock.tick)
        locator.graphics.push(self.graphics)

    def exit(self):
        logger.debug("Exiting game")
        locator.clock.remove_handlers(on_update=self.clock.tick)
        locator.graphics.pop()


class GameCollisionSystem(collision.CollisionSystem):

    def on_update(self, dt):
        player_hb = locator.tm['player'].get(collision.Hitbox)
        for b in locator.gm['enemy_bullet']:
            if collision.collide(player_hb, b):
                kill_player()
        for b in locator.gm['player_bullet']:
            for e in locator.em.get_with(enemy.Life):
                if collision.collide(b, e):
                    hit_life(e, b.dmg)
                    locator.em.delete(b)
                    break


class GameDrawer(sprite.SpriteDrawer):

    map = ('player', 'player_bullet', 'player_hb', 'enemy', 'item',
           'enemy_bullet', 'ui', 'ui_element')


def kill_player():
    l = locator.tm['lives']
    if l.value > 0:
        l.value -= 1
    else:
        locator.scene_stack.pop()


def hit_life(entity, dmg):
    for l in entity.get(enemy.Life):
        l.life -= dmg
