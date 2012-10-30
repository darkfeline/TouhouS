from gensokyo import ces
from gensokyo import locator


class Script(ces.Component):

    def __init__(self, script):
        self.script = script
        self.step = 0
        self.sleep = 0


class ScriptSystem(ces.System):

    req_components = (Script,)
    callable_methods = set()

    def goto(self, entity, script, step=0):
        """
        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script
        :param step: index in script to jump to
        :type step: int

        """
        script.step = step - 1  # account for automated step in update()
    callable_methods.add(goto)

    def sleep(self, entity, script, time):
        """
        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script
        :param time: time to sleep in seconds
        :type time: int

        """
        script.sleep = time
    callable_methods.add(sleep)

    def die(self, entity, script):
        """
        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script

        """
        locator.em.delete(entity)
    callable_methods.add(die)

    def fire(self, entity, script, bullet):
        """
        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script
        :param bullet: Bullet constructor
        :type bullet: callable returning Bullet

        """
        # TODO Position?
        b = bullet()
        locator.em.add(b)
        locator.gm.add_to(b)
    callable_methods.add(fire)

    def call(self, entity, script, method_name, *args, **kwargs):

        """
        Call method with given name and pass it the given entity

        Valid methods for such calling have the type signature::

            method_name(self, entity, script, *args, **kwargs)

        `*args` and `**kwargs` are optional depending on method.

        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script
        :param method_name: name of method
        :type method_name: str

        """

        m = getattr(self, method_name)
        if m in self.callable_methods:
            return m(self, entity, script, *args, **kwargs)
        else:
            raise TypeError(method_name + " is not a callable method")

    def update(self, dt):
        for entity in locator.em.get_with(self.req_components):
            for script in entity.get(Script):
                if script.sleep > 0:
                    script.sleep -= dt
                else:
                    if script.step < len(script.script):
                        self.call(entity, script, *script.script[script.step])
                        script.step += 1
