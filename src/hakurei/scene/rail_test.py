from gensokyo import scene
from gensokyo.ces import graphics

from hakurei import ces


class RailTestScene(scene.Scene):

    def init(self):

        # Entities
        # FPS
        fps = ces.ui.FPSDisplay(570, 2)
        self.em.add(fps)
        self.tm.tag('fps_display', fps)

        # Systems
        g = RailTestGraphics()
        self.sm.add(g)
        fps = ces.ui.FPSSystem()
        self.sm.add(fps)

        # TODO finish this


class RailTestGraphics(graphics.Graphics):

    _map = ('fg', 'ui')
