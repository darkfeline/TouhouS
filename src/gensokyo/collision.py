#!/usr/bin/env python3

from weakref import WeakKeyDictionary

class CollisionManager:

    """
    Collision Manager

    On every tick/update, checks all added collision components for collisions.
    Uses weak references so components garbage collect normally.
    Each component is associated with a dictionary of collision handlers.
    The key is the class whose collision against triggers the handler.

    {
        class: {
            component: {
                type: method,
                ...
            },
            ...
        }
    }

    self.components[class][component][other_class] = method
    component.method(other)

    """

    def __init__(self):
        self.components = {}

    def add(self, component):
        """Adds handlers of component.

        First checks for instance attribute chandlers and adds handlers if has.
        Else checks for class attribute chandlers.

        """
        if hasattr(component, 'chandlers'):
            self.add_handlers(component, component.chandlers)
        elif hasattr(component.__class__, 'chandlers'):
            self.add_handlers(component, component.__class__chandlers)

    def add_handlers(self, component, handlers):
        """
        handlers = {class: method,...}
        """
        cls = component.__class__
        if cls not in self.components.keys():
            self.components[cls] = WeakKeyDictionary()
        self.components[cls][component] = handlers

    def update(self, dt):
        c = self.components
        items = ((comp, c[cls][comp]) for cls in c.keys()
                for comp in c[cls].keys())
        for comp, hands in items:
            for type, meth in hands.items():
                for other_comp in (comp for comp in c[type].keys()):
                    if comp.collide(other_comp):
                        meth(comp, other_comp)
