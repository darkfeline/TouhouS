import logging
import sys
import os.path

from pyglet import resource


def centered_image(image):
    """Loads an image and centers it"""
    image = resource.image(image)
    center(image)
    return image


def center(image):
    """Sets an image's anchor point to center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

logger = logging.getLogger(__name__)

resource.path = [os.path.join(sys.prefix, 'resources')]
resource.reindex()

# UI
ui_image = resource.image('ui.png')
icon16 = resource.image('icon16.png')
icon32 = resource.image('icon32.png')
star = resource.image('star.png')

# Players
player = {}
a = "players"
# Reimu
player['reimu'] = {}
b = a + "/reimu"
player['reimu']['player'] = centered_image(b + "/player.png")
player['reimu']['shot'] = centered_image(b + '/shot.png')
player['reimu']['hitbox'] = centered_image(b + '/hitbox.png')

# Enemies
enemy = {}
a = "enemies"
enemy['generic'] = centered_image(a + '/generic.png')

# Bullets
bullet = {}
a = "bullets"
bullet['round'] = centered_image(a + '/round.png')
