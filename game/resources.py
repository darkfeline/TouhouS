#!/usr/bin/env python3

import os.path

from pyglet import resource

def centered_image(image):
    """Loads an image and centers it"""
    image = resource.image(image)
    center_image(image)
    return image

def center_image(image):
    """Sets an image's anchor point to center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

resource.path = ['resources']
resource.reindex()

# UI
ui_image = resource.image('ui.png')
icon1 = resource.image('icon16.png')
icon2 = resource.image('icon32.png')

# Players
player = {}
a = "players"
# Reimu
player['reimu'] = {}
b = os.path.join(a, "reimu")
player['reimu']['player'] = centered_image(os.path.join(b, "player.png"))
player['reimu']['shot'] = centered_image(os.path.join(b, 'shot.png'))
player['reimu']['hitbox'] = centered_image(os.path.join(b, 'hitbox.png'))

# Enemies
enemy = {}
a = "enemies"
enemy['generic'] = centered_image(os.path.join(a, 'generic.png'))

# Bullets
bullet = {}
a = "bullets"
bullet['round'] = centered_image(os.path.join(a, 'round.png'))
