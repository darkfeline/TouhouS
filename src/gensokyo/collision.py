#!/usr/bin/env python3

from weakref import WeakKeyDictionary

class CollisionManager:

    """
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

    def add(self, component, handlers):
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
