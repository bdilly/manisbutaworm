from cocos.layer import Layer

class GameView(Layer):

    def __init__(self, model):
        super(GameView,self).__init__()

        self.model = model
        self.model.push_handlers(self.on_move)

    def on_enter(self):
        super(GameView,self).on_enter()

    def on_move(self):
        pass
