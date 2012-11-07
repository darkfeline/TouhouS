from gensokyo import scene
from gensokyo import locator
from gensokyo.ces import graphics

from hakurei import ces
from hakurei.scene import game


class MenuScene(scene.Scene):

    def init(self):
        self.title = ces.graphics.Label(
            x=20, y=globals.HEIGHT - 30, text="Welcome to TouhouS",
            color=(255, 255, 255, 255))

    def on_key_press(self, symbol, modifiers):
        locator.scene_stack.push(game.GameScene())


class MenuGraphics(graphics.Graphics):

    _map = ('bg', 'text')
