from gensokyo import scene

from hakurei import ces
from hakurei import resources


class GameModel(scene.Model):

    player_class = ces.player.Reimu
    stage_class = ces.stage.StageOne
    ui_image = resources.ui_image

    def init(self):

        # Groups
        self.gm.make_group('bullets')
        self.gm.make_group('enemies')

        # Entities
        # UI image
        bg = ces.Wrapper(ces.graphics.Sprite('ui', self.ui_image))
        self.em.add(bg)
        # FPS
        fps = ces.ui.FPSDisplay(570, 2)
        self.em.add(fps)
        self.tm.tag('fps_display', fps)

        # Counters
        counters = {
            'high_score': (ces.ui.TextCounter, 430, 415, 'High score'),
            'score': (ces.ui.TextCounter, 430, 391, 'Score'),
            'lives': (ces.ui.IconCounter, 430, 361, 'Lives'),
            'bombs': (ces.ui.IconCounter, 430, 339, 'Bombs')}
        for tag, a in counters.items():
            c, x, y, tit = a
            counter = c(x, y, tit)
            self.em.add(counter)
            self.tm.tag(tag, counter)

        # Data
        data = ces.Wrapper(ces.gamedata.GameData())
        self.tm.tag('data', data)

        # Systems
        fps = ces.ui.FPSSystem()
        self.sm.add(fps)
        data = ces.gamedata.DataSystem()
        self.sm.add(data)

        # TODO finish this


class GameView(scene.View):

    _map = ('player', 'player_bullet', 'player_hb', 'enemy', 'item',
            'enemy_bullet', 'ui', 'ui_element')


def get_scene():
    return scene.Scene(GameModel(), GameView())
