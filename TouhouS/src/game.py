#!/usr/bin/env python3

from gensokyo import game
from gensokyo.ui import UI

from reimu import Reimu
from stage import Stage
import resources

class Game(game.Game):

    def __init__(self, keys):
        super().__init__(keys, UI(resources.ui_image, resources.star), Reimu,
                Stage)
