#!/usr/bin/env python3

from pyglet import resource

def load_image(image):
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

player_image = load_image("player.png")
shot_image = load_image('shot.png')
enemy_image = load_image('enemy.png')
bullet_image = load_image('bullet.png')
hitbox_image = load_image('hitbox.png')
