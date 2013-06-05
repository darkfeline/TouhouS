import logging
import sys
import os
import os.path

from pyglet import resource


def centered_image(image):
    """Loads an image and centers it"""
    image = resource.image(image)
    _center(image)
    return image


def _center(image):
    """Sets an image's anchor point to center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

__all__ = [
    'ui_image', 'icon16', 'icon32', 'star',
    'players', 'enemies', 'bullets'
]
logger = logging.getLogger(__name__)

logger.info("Initializing resources...")
logger.debug("Working directory is %s", os.getcwd())
resource.path = [os.path.join(sys.prefix, 'resources')]
logger.debug("Path is %s", resource.path)
resource.reindex()

# UI
ui_image = resource.image('ui.png')
icon16 = resource.image('icon16.png')
icon32 = resource.image('icon32.png')
star = resource.image('star.png')

# Players
players = {}
a = os.path.join(resource.path, 'players')
for player in os.listdir(a):
    current = {}
    players[player] = current
    b = os.path.join(a, player)
    for x in os.listdir(b):
        players[os.path.basename(x)] = centered_image(os.path.join(b, x))

# Enemies
enemies = {}
for x in os.listdir(os.path.join(resource.path, 'enemies')):
    enemies[os.path.basename(x)] = centered_image(os.path.join('enemies', x))

# Bullets
bullets = {}
for x in os.listdir(os.path.join(resource.path, 'bullets')):
    bullets[os.path.basename(x)] = centered_image(os.path.join('bullets', x))

logger.info("Finished initializing resources.")
