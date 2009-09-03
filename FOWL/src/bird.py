from sprite import Sprite

class Bird(Sprite):

    def __init__(self, text_x, text_y, **kwargs):
        self.kills = 0
        Sprite.__init__(self, "bird.png", **kwargs)

    def draw(self):
        Sprite.draw(self)
        
    def on_kill(self):
        self.kills += 1
