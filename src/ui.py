#!/usr/bin/env python3

from gensokyo.model import ui

import resources

class IconCounter(ui.IconCounter):

    icon_img = resources.star


class UI(ui.UI):

    bg_img = resources.ui_image
    _counters = {'high_score': (ui.TextCounter, 430, 415, 'High score'),
        'score': (ui.TextCounter, 430, 391, 'Score'),
        'lives': (IconCounter, 430, 361, 'Lives'),
        'bombs': (IconCounter, 430, 339, 'Bombs')}
