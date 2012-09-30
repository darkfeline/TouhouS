#!/usr/bin/env python3

from gensokyo import manager


class Model:

    def __init__(self):
        self.em = manager.EntityManager()
        self.sm = manager.SystemManager()

    def update(self, dt):
        self.sm.update(dt)
