import pyglet
import weakref

import Box2D as box2d
from settings import fwSettings

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
        sd = box2d.b2PolygonDef()
        sd.SetAsBox(10.0, 10.0)

        bd = box2d.b2BodyDef() 
        bd.position = (20.0, 20.0)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetMassFromShapes()

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
