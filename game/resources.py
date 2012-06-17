#!/usr/bin/env python3

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

icon1 = resource.image('icon16.png')
icon2 = resource.image('icon32.png')

ui_image = resource.image('ui.png')

player_image = centered_image("player.png")
shot_image = centered_image('shot.png')
enemy_image = centered_image('enemy.png')
bullet_image = centered_image('bullet.png')
hitbox_image = centered_image('hitbox.png')
