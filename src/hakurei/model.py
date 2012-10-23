from gensokyo.model import Model
from gensokyo.scene import Scene
from gensokyo import locator

from hakurei import ces
from hakurei import view
from hakurei import resources
from hakurei import globals


class GameModel(Model):

    player_class = ces.player.Reimu
    stage_class = ces.stage.StageOne
    ui_image = resources.ui_image

    def init(self):

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


class MenuModel(Model):

    def init(self):
        self.title = ces.graphics.Label(
            x=20, y=globals.HEIGHT - 30, text="Welcome to TouhouS",
            color=(255, 255, 255, 255))

    def on_key_press(self, symbol, modifiers):
        locator.scene_stack.push(Scene(GameModel(), view.GameView()))
