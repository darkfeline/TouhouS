#!/usr/bin/env python3

from pyglet import clock

from game import player
from game import bullet
from game import enemy
from game import resources
from game.vector import Vector

class Player(player.Player):

    def __init__(self):
        super().__init__(img=resources.player_image)

    def update_fire(self, dt):
        period = 1 / self.shot_rate  # period of shot
        i = 0
        while self.shot_state > period:
            shot = PlayerBullet(x=self.x, y=self.y)
            shot.update(i)
            self.shots.add(shot)
            self.shot_state -= period
            i += period


class Enemy(enemy.Enemy):

    def __init__(self, x, y, bullet_group):
        super().__init__(x, y, bullet_group, img=resources.enemy_image)

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = EnemyBullet(self.x, self.y, vector=v)
        self.bullets.add(b)


class PlayerBullet(bullet.Bullet):

    def __init__(self, x, y):
        super().__init__(x, y, img=resources.shot_image)


class EnemyBullet(bullet.Bullet):

    def __init__(self, x, y, vector):
        super().__init__(x, y, img=resources.bullet_image, speed=300,
                vector=vector)


def start():
    pass
