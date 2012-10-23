from gensokyo import scene

from hakurei import ces


class RailTestModel(scene.Model):

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

        # Systems
        fps = ces.ui.FPSSystem()
        self.sm.add(fps)

        # TODO finish this


class RailTestView(scene.View):

    _map = ('fg', 'ui')


def get_scene():
    return scene.Scene(RailTestModel(), RailTestView())
