#!/usr/bin/env python3

class Game:

    def __init__(self):
        self.stack = []

    def push(self, model):
        self.stack.append(model)

    def pop(self):
        return self.stack.pop()

    def update(self, dt):
        self.stack[-1].update(dt)
