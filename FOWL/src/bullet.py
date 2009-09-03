from sprite import Sprite

class Bullet(Sprite):

    def __init__(self, parent_ship, image_data, top, **kwargs):
        self.velocity = 5
        self.screen_top = top
        self.parent_ship = parent_ship
        Sprite.__init__(self,"", image_data, **kwargs)

    def update(self):
        self.y += self.velocity
        #Have we gone off the screen?
        if (self.bottom > self.screen_top):
            self.dead = True

    def on_kill(self):
        """We have hit a monster let the parent know"""
        self.parent_ship.on_kill()
