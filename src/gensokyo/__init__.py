#!/usr/bin/env python3

"""
Pyglet-based 2D game engine/wrapper

gensokyo is designed for TouhouS, a Touhou-like shoot-em-up.  It provides a
basic game engine structure and some commonly used objects, such as Rects,
Circles, Vectors.

gensokyo primarily uses an MVC and a Component/System based design pattern.

`ces` provides the basics for a CES (Component, Entity, System) design, and can
be used minimalistically with `manager` or `model`, but is intended to be used
with `scene` for scene management and `locator` as a global service locator.
`view` provides an easy way to manage pyglet Sprites, Batches, and draw order,
and can also be used with `scene` scene management.

Design Hierarchy
################

Game
    Controller
    SceneStack
        Scene
            Model
                EntityManager
                    Entity
                        Component
                SystemManager
                    System
            View

Update Hierarchy
################

Update
    SceneStack
        Scene
            Model
                SystemManager
                    System

on_draw Hierarchy
#################

on_draw
    SceneStack
        Scene
            View

"""
