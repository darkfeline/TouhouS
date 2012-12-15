from gensokyo import scene
from gensokyo import ces
from gensokyo.ces import stage
from gensokyo.ces import graphics
from gensokyo.ces import player
from gensokyo.ces import ui
from gensokyo.ces import update
from gensokyo.ces import script
from gensokyo.ces import enemy
from gensokyo.ces import rails
from gensokyo.ces import collision
from gensokyo.ces import gc
from gensokyo.ces import physics
from gensokyo import resources
from gensokyo import locator
from gensokyo import globals


class GameScene(scene.Scene):

    player_class = player.Reimu
    stage_class = stage.StageOne
    ui_image = resources.ui_image

    def __init__(self):

        super().__init__()

        self.graphics = GameGraphics()
        self.updater = update.Updater()

        # Systems
        self.sm.add(player.ShiftingSystem(self, globals.GAME_AREA))
        self.sm.add(player.ShieldDecay(self))
        self.sm.add(script.ScriptSystem(self))
        self.sm.add(enemy.GrimReaper(self))
        self.sm.add(rails.RailSystem(self))
        self.sm.add(physics.PhysicsSystem(self))
        self.sm.add(gc.GarbageCollectSystem(self, globals.GAME_AREA))

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
        self.updater.push_handlers(fps)
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
        locator.clock.push_handlers(self.updater)
        locator.graphics.push(self.graphics)

    def exit(self):
        locator.clock.remove_handlers(self.updater)
        locator.graphics.pop()

    def delete(self):
        super().delete()


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


class GameGraphics(graphics.Graphics):

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
