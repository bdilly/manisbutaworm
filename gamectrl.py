import pyglet
from pyglet.gl import *
import Box2D as box2d
import math

from cocos.director import director
from cocos.layer import Layer
from cocos.sprite import Sprite

from constants import WIDTH, HEIGHT

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
            userdata = b.GetUserData()
            if not userdata:
                userdata = {}
                b.SetUserData(userdata)
            sprite = userdata.get("sprite")
            if not sprite:
                sprite = Sprite(self.image)
                self.add(sprite)
                userdata["sprite"] = sprite

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
