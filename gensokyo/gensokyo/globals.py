#!/usr/bin/env python3

from gensokyo.primitives import Rect

FPS = 60
HEIGHT = 480
WIDTH = 640
WINDOW = Rect(0, 0, WIDTH, HEIGHT)
GAME_AREA = Rect(32, 16, 384, 448)
DEF_PLAYER_XY = GAME_AREA.width//2+GAME_AREA.left, GAME_AREA.bottom+40
WINDOW = None
KEYS = None
