#!/usr/bin/env python2

from __future__ import division

import pyglet

def center_image(image):
    """Sets an image's anchor point to center"""
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

icon1 = pyglet.resource.image('icon16.png')
icon2 = pyglet.resource.image('icon32.png')

player_image = pyglet.resource.image("player.png")
center_image(player_image)