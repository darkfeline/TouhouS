from gensokyo import primitives
from gensokyo import resources
from gensokyo.data.bullets import EnemyBullet

BasicRedBullet = EnemyBullet(
    img=resources.bullet['basic_red'], hitbox=primitives.Circle(0, 0, 10))
