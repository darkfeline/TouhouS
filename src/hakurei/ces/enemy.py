from gensokyo import ces
from gensokyo import primitives

from hakurei.ces import collision
from hakurei.ces import graphics
from hakurei.ces import ai

# TODO finish this
# TODO Enemy movement


class Life(ces.Component):

    def __init__(self, life):
        self.life = life


class Enemy(ces.Entity):

    sprite_img = None
    sprite_group = 'enemy'
    hb = None
    init_life = 200

    def __init__(self, x, y, script):

        """
        :param x: x coordinate
        :type x: int
        :param y: y coordinate
        :type y: int

        """

        super().__init__()
        hb = collision.Hitbox(self.hitbox)
        hb.x, hb.y = x, y
        self.add(hb)
        s = graphics.Sprite(self.sprite_group, self.sprite_img, x=x, y=y)
        self.add(s)
        ai = ai.EnemyAI(script)
        self.add(ai)
        l = Life(self.init_life)
        self.add(l)


class Enemy(Container):

    sprite_img = None
    sprite_group = 'enemy'
    hb = None
    init_life = 200

    def __init__(self, x, y):

        super().__init__()

        p = SmoothDestComp()
        c = EnemyCollisionComponent(x, y, self.sprite_img.width,
                self.sprite_img.height, self.hb)
        g = SpriteComponent(self.sprite_group, img=self.sprite_img)
        l = LifeComponent(self.init_life)

        p.speed = 0
        p.accel = 100
        p.max_speed = 300

        p.push_handlers(g)
        p.push_handlers(c)
        c.push_handlers(l)
        l.push_handlers(g)
        l.push_handlers(self)

        self.add(p)
        self.add(c)
        self.add(g)
        self.add(l)

        self.physics = p


class GenericEnemy(Enemy):

    sprite_img = resources.enemy['generic']
    hb = primitives.Circle(0, 0, sprite_img.width)
    init_life = 200

    def __init__(self, x, y):
        super().__init__(x, y)
        self.physics.max_speed = 300
        self.physics.accel = 100

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = bullet.RoundBullet(self.x, self.y, vector=v)
        self.bullets.add(b)