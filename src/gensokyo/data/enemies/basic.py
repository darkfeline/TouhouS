import logging

from gensokyo import primitives
from gensokyo.ecs.enemy import Enemy
from gensokyo import resources

logger = logging.getLogger(__name__)

img = resources.enemies['basic_fairy']
BasicFairy = Enemy(
    img=img, hitbox=primitives.Rect(0, 0, img.width, img.height), life=200
)
