import pyglet
from pyglet.gl import *
import Box2D as box2d
import math

from cocos import draw
from cocos.director import director
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.rect import Rect

from constants import WIDTH, HEIGHT


class RectBlock(draw.Canvas):
    p1 = (-1.0, -1.0)
    p2 = (1.0, -1.0)
    p3 = (1.0, 1.0)
    p4 = (-1.0, 1.0)

    def __init__(self, points=None):
        super(RectBlock, self).__init__()

        if not points:
            return

        self.p1 = points[0][0],points[0][1]
        self.p2 = points[1][0],points[1][1]
        self.p3 = points[2][0],points[2][1]
        self.p4 = points[3][0],points[3][1]

        self.set_color((255,255,0,255))
        self.set_stroke_width(5)

    def render(self):
        print "rendering block"
        self.set_join(draw.MITER_JOIN)
        self.move_to(self.p1)
        self.line_to(self.p2)
        self.line_to(self.p3)
        self.line_to(self.p4)
        self.line_to(self.p1)

class GameCtrl(Layer):
    is_event_handler = True

    def __init__(self, model):
        super(GameCtrl,self).__init__()

        self.model = model

        self.image = pyglet.resource.image('hero.png')

    def on_key_pressed(self, k, m):
        if k in [key.SPACE, key.RETURN]:
            self.model.act()

    def step(self, dt):
        self.elapsed += dt
        self.model.world.Step(dt, self.model.settings.velocityIterations,
            self.model.settings.positionIterations)

    def draw( self ):
        super(GameCtrl, self).draw()

        glLoadIdentity()

        bodies = self.model.world.GetBodyList()
        i = 0
        for b in bodies:
            props = b.GetUserData()
            if not props:
                continue
            sprite = props.get_sprite()
            if not sprite:
                if props.isCharacter:
                    sprite = Sprite(self.image)
                elif props.isBlock:
                    shape = b.GetShapeList()[0]
                    vertices = shape.getVertices_b2Vec2()
                    sprite = RectBlock(vertices)
                    print sprite.p1, sprite.p2, sprite.p3, sprite.p4
                else:
                    continue

            props.set_sprite(sprite)
            self.add(sprite)
            sprite.position = (b.position.x * self.model.zoom), \
                (b.position.y * self.model.zoom)
            degrees = (b.GetAngle() * 180) / math.pi
            sprite.rotation = degrees

        # center the image
        glTranslatef(-320, -240, -320.0)

    def on_enter(self):
        super(GameCtrl, self).on_enter()

        director.push_handlers(self.on_resize)
        self.elapsed = 0
        self.schedule(self.step)

    def on_resize( self, width, height ):
        # change the 2D projection to 3D
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 1.0*width/height, 0.1, 400.0)
        glMatrixMode(GL_MODELVIEW)
