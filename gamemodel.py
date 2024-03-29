import pyglet
import weakref

import Box2D as box2d
from settings import fwSettings

class BodyProperties(object):
    isCharacter = False
    isBlock = True
    _sprite = None

    def __init__(self, isBlock=True, isCharacter=False):
        super(BodyProperties,self).__init__()
        if isCharacter:
            self.isBlock = False
            self.isCharacter = True

    def get_sprite(self):
        return self._sprite

    def set_sprite(self, sprite):
        self._sprite = sprite

class GameModel(pyglet.event.EventDispatcher):
    def __init__(self):
        super(GameModel,self).__init__()
        self.acting = False

        # Box2D Initialization
        self.zoom = 10
        self.worldAABB=box2d.b2AABB()
        self.worldAABB.lowerBound = (-200.0, -100.0)
        self.worldAABB.upperBound = ( 200.0, 200.0)
        gravity = (0.0, -10.0)
        doSleep = True

        self.world = box2d.b2World(self.worldAABB, gravity, doSleep)

        settings = fwSettings
        self.settings = settings
        self.flag_info = [ ('draw_shapes', settings.drawShapes,
                            box2d.b2DebugDraw.e_shapeBit),
                           ('draw_joints', settings.drawJoints,
                            box2d.b2DebugDraw.e_jointBit),
                           ('draw_controlers', settings.drawControllers,
                            box2d.b2DebugDraw.e_controllerBit),
                           ('draw_core_shapes', settings.drawCoreShapes,
                            box2d.b2DebugDraw.e_coreShapeBit),
                           ('draw_aabbs', settings.drawAABBs,
                            box2d.b2DebugDraw.e_aabbBit),
                           ('draw_obbs', settings.drawOBBs,
                            box2d.b2DebugDraw.e_obbBit),
                           ('draw_pairs', settings.drawPairs,
                            box2d.b2DebugDraw.e_pairBit),
                           ('draw_center_of_masses', settings.drawCOMs,
                            box2d.b2DebugDraw.e_centerOfMassBit),]

        # Create hero
        body = self.create_character(10, 20)
        body.SetMassFromShapes()
        if self.settings.debugLevel:
            print body

        # Create ground
        body = self.create_ground(0, 10, 20, 5)


    def create_character(self, x, y):
        props = BodyProperties(isCharacter=True)
        sd = box2d.b2PolygonDef()
        sd.SetAsBox(10.0, 10.0)
        sd.density = 1.0

        bd = box2d.b2BodyDef()
        bd.position = (x, y)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetUserData(props)
        return body

    def create_ground(self, x, y, w, h):
        props = BodyProperties()
        sd = box2d.b2PolygonDef()
        sd.SetAsBox(w, h)
        bd = box2d.b2BodyDef()
        bd.position = (x, y)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetUserData(props)
        return body

    def set_controller( self, ctrl ):
        self.ctrl = weakref.ref( ctrl )

    def act(self):
        if self.acting:
            return

        self.acting = True
        self.dispatch_event("on_move")


GameModel.register_event_type('on_move')
GameModel.register_event_type('on_colision')
GameModel.register_event_type('on_win')
GameModel.register_event_type('on_gameover')
