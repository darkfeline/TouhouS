from gensokyo import scene
from gensokyo import locator

from hakurei import ces
from hakurei.scene import game


class MenuModel(scene.Model):

    def init(self):
        self.title = ces.graphics.Label(
            x=20, y=globals.HEIGHT - 30, text="Welcome to TouhouS",
            color=(255, 255, 255, 255))

    def on_key_press(self, symbol, modifiers):
        locator.scene_stack.push(game.get_scene())


class MenuView(scene.View):

    _map = ('bg', 'text')


def get_scene():
    return scene.Scene(MenuModel(), MenuView())
