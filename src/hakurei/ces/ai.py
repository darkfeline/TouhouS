from gensokyo import ces


class AI(ces.Component):

    def __init__(self, script):
        self.script = script
        self.step = 0
        self.sleep = 0


class AISystem(ces.System):

    req_components = (AI,)

    def goto(self, entity, ai, step=0):

        """
        :param entity: entity passed to call
        :type entity: Entity
        :param ai: AI component passed to call
        :type entity: AI
        :param step: index in script to jump to
        :type step: int

        """

        ai.step = step

    def sleep(self, entity, ai, time):

        """
        :param entity: entity passed to call
        :type entity: Entity
        :param ai: AI component passed to call
        :type entity: AI
        :param time: time to sleep in seconds
        :type time: int

        """

        ai.sleep = time

    def call(self, entity, ai, method_name, *args, **kwargs):

        """
        Call method with given name and pass it the given entity

        Valid methods for such calling have the type signature::

            method_name(self, entity, ai, *args, **kwargs)

        `*args` and `**kwargs` are optional depending on method.

        :param entity: entity passed to call
        :type entity: Entity
        :param ai: AI component passed to call
        :type entity: AI
        :param method_name: name of method
        :type method_name: str

        """

        return getattr(self, method_name)(self, entity, ai, *args, **kwargs)

    # TODO implement this
    def move_to(self, entity, ai, dest):
        pass

    def update(self, dt):
        entities = self.get_with(self.req_components)
        for e in entities:
            for ai in e.get(AI):
                if ai.sleep > 0:
                    ai.sleep -= dt
                else:
                    if ai.step < len(ai.script):
                        self.call(e, ai, *ai.script[ai.step])
                        ai.step += 1
