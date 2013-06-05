from functools import partial

from gensokyo.ecs.bullet import Bullet

EnemyBullet = partial(Bullet, group='enemy_bullet', dmg=1)
