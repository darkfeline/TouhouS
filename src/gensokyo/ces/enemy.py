from gensokyo import ces
from gensokyo import primitives
from gensokyo.ces import collision
from gensokyo.ces import graphics
from gensokyo.ces import bullet
from gensokyo.ces import rails
from gensokyo.ces import script
from gensokyo import resources
from gensokyo import locator


# TODO move this and GrimReaper?
class Life(ces.Component):

    def __init__(self, life):
        self.life = life


class Enemy(ces.Entity):

    sprite_img = None
    sprite_group = 'enemy'
    hb = None
    init_life = 1

    def __init__(self, x, y):

        """
        Just add Rails (and Script)!

        :param x: x coordinate
        :type x: int
        :param y: y coordinate
        :type y: int

        """

        super().__init__()

        hb = EnemyHitbox(self.hitbox)
        hb.x, hb.y = x, y
        self.add(hb)

        s = EnemySprite(self.sprite_group, self.sprite_img, x=x, y=y)
        self.add(s)

        l = Life(self.init_life)
        self.add(l)


class EnemyHitbox(collision.Hitbox, rails.RailPosition):
    pass


class EnemySprite(graphics.Sprite, rails.RailPosition):
    pass


class GrimReaper(ces.System):

    req_components = (Life,)

    def update(self, dt):
        for entity in locator.em.get_with(self.req_components):
            data = entity.get(self.req_components[0])[0]
            if data.life <= 0:
                self.kill(entity)

    @classmethod
    def kill(enemy):
        locator.em.delete(enemy)


# TODO move everything below
class GenericEnemy(Enemy):

    sprite_img = resources.enemy['generic']
    hb = primitives.Rect(0, 0, sprite_img.width, sprite_img.height)
    init_life = 200

    def __init__(self, x, y):

        super().__init__(x, y)

        s = script.Script([LoopFireAtPlayer((x, y), 0.5)])
        self.add(s)


class LoopFireAtPlayer(script.ConditionUnit, rails.RailPosition):

    def __init__(self, pos, rate):
        self.pos = pos
        self.state = 0
        self.rate = rate

    @property
    def satisfied(self):
        if self.state > self.rate:
            return True
        else:
            return False

    def run(self, entity):
        self.state -= self.rate
        player = locator.tm['player']
        hb = player.get(collision.Hitbox)
        dest = hb.pos
        dest = primitives.Vector(dest[0], dest[1])
        v = dest - primitives.Vector(*self.pos)
        b = bullet.RoundBullet(*self.pos, vector=v)
        locator.em.add(b)
        locator.gm.add_to(b, 'enemy_bullet')

    def update(self, dt):
        self.state += dt
