#!/usr/bin/env python3

from pyglet import resource

def center_image(image):
    """Sets an image's anchor point to center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

resource.path = ['resources']
resource.reindex()

icon1 = resource.image('icon16.png')
icon2 = resource.image('icon32.png')

player_image = resource.image("player.png")
center_image(player_image)
shot_image = resource.image('shot.png')
center_image(shot_image)
enemy_image = resource.image('enemy.png')
center_image(enemy_image)
bullet_image = resource.image('bullet.png')
center_image(bullet_image)
