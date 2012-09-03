#!/usr/bin/env python3

from gensokyo import model

from reimu import Reimu
from stage import Stage
from ui import UI
import resources

class Model(model.Model):

    ui_class = UI
    player_class = Reimu
    stage_class = Stage
