from gensokyo import primitives
from gensokyo import resources
from gensokyo.ecs.enemy import EnemyBullet

BasicRedBullet = EnemyBullet(
    img=resources.bullet['basic_red'], hitbox=primitives.Circle(0, 0, 10))
