from gensokyo import scene

from hakurei import ces


class RailTestModel(scene.Model):

    def init(self):

        # Entities
        # FPS
        fps = ces.ui.FPSDisplay(570, 2)
        self.em.add(fps)
        self.tm.tag('fps_display', fps)

        # Systems
        fps = ces.ui.FPSSystem()
        self.sm.add(fps)

        # TODO finish this


class RailTestView(scene.View):

    _map = ('fg', 'ui')


def get_scene():
    return scene.Scene(RailTestModel(), RailTestView())
