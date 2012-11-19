from gensokyo import scene
from gensokyo import ces
from gensokyo.ces import stage
from gensokyo.ces import graphics
from gensokyo.ces import player
from gensokyo.ces import ui
from gensokyo.ces import gamedata
from gensokyo import resources


class GameScene(scene.Scene):

    player_class = player.Reimu
    stage_class = stage.StageOne
    ui_image = resources.ui_image

    def init(self):

        # Groups
        self.gm.make_group('bullets')
        self.gm.make_group('enemies')

        # Entities
        # UI image
        bg = ces.Wrapper(graphics.Sprite('ui', self.ui_image))
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

        # Data
        data = ces.Wrapper(gamedata.GameData())
        self.tm.tag('data', data)

        # Systems
        g = GameGraphics()
        self.sm.add(g)
        fps = ui.FPSSystem()
        self.sm.add(fps)
        data = gamedata.DataSystem()
        self.sm.add(data)

        # TODO finish this


class GameGraphics(graphics.Graphics):

    _map = ('player', 'player_bullet', 'player_hb', 'enemy', 'item',
            'enemy_bullet', 'ui', 'ui_element')
