#!/usr/bin/env python3

"""
Pyglet-based 2D game engine.

gensokyo is designed for TouhouS, a Touhou-like shoot-em-up.

gensokyo primarily uses MVC and a Component/System based design pattern.

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

Update
    SceneStack
        Scene
            Model
                SystemManager
                    System
            View

"""
