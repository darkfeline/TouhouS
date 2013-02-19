from collections import namedtuple
from functools import partial

from gensokyo import ces
from gensokyo import primitives
from gensokyo.ces import collision
from gensokyo.ces import graphics
from gensokyo.ces import bullet
from gensokyo.ces import rails
from gensokyo.ces import script
from gensokyo import resources

Enemy = namedtuple("Enemy", ['img', 'group', 'hitbox', 'life'])
Enemy = partial(Enemy, group='enemy')


def make_enemy(world, enemy, x, y):

    e = world.make_entity()

    hb = EnemyHitbox(enemy.hb.copy())
    hb.setpos((x, y))
    world.add_component(e, hb)

    sprite = graphics.Sprite(enemy.group, enemy.img, x=x, y=y)
    world.add_component(e, sprite)

    l = Life(enemy.life)
    world.add_component(e, l)


class Life(ces.Component):

    def __init__(self, life):
        self.life = life


class EnemyHitbox(collision.Hitbox):
    pass


class GrimReaper(ces.System):

    req_components = (Life,)

    def on_update(self, dt):
        for entity in self.env.em.get_with(self.req_components):
            life = entity.get(self.req_components[0])[0]
            if life.life <= 0:
                life.die(entity)
                self.env.em.delete(entity)


# TODO move everything below
class GenericEnemy(Enemy):

    sprite_img = resources.enemy['generic']
    hb = primitives.Rect(0, 0, sprite_img.width, sprite_img.height)
    init_life = 200

    def __init__(self, x, y):

        super().__init__(x, y)

        s = LoopFireAtPlayer((x, y), 0.5)
        self.add(s)


class LoopFireAtPlayer(script.Script, rails.RailPosition):

    def __init__(self, pos, rate):
        self.pos = pos
        self.state = 0
        self.rate = rate

    def run(self, entity, env, dt):
        self.state += dt
        if self.state >= self.rate:
            self.state -= self.rate
            player = env.tm['player']
            hb = player.get(collision.Hitbox)
            dest = hb.pos
            dest = primitives.Vector(dest[0], dest[1])
            v = dest - primitives.Vector(*self.pos)
            b = bullet.RoundBullet(*self.pos, vector=v)
            env.em.add(b)
            env.gm.add_to(b, 'enemy_bullet')
