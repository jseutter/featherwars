import helper

class Sprite(object):

    def __get_left(self):
        return self.x
    left = property(__get_left)

    def __get_right(self):
        return self.x + self.image.width
    right = property(__get_right)

    def __get_top(self):
        return self.y + self.image.height
    top = property(__get_top)

    def __get_bottom(self):
        return self.y
    bottom = property(__get_bottom)

    def __init__(self, image_file, image_data=None, **kwargs):

        #init standard variables
        self.image_file = image_file
        if (image_data is None):
            self.image = helper.load_image(image_file)
        else:
            self.image = image_data
        self.x = 0
        self.y = 0
        self.dead = False
        #Update the dict if they sent in any keywords
        self.__dict__.update(kwargs)

    def draw(self):
        self.image.blit(self.x, self.y)

    def update(self):
        pass

    def intersect(self, sprite):
        """Do the two sprites intersect?
        @param sprite - Sprite - The Sprite to test
        """
        return not ((self.left > sprite.right)
            or (self.right < sprite.left)
            or (self.top < sprite.bottom)
            or (self.bottom > sprite.top))

    def collide(self, sprite_list):
        """Determing ther are collisions with this
        sprite and the list of sprites
        @param sprite_list - A list of sprites
        @returns list - List of collisions"""

        lst_return = []
        for sprite in sprite_list:
            if (self.intersect(sprite)):
                lst_return.append(sprite)
        return lst_return

    def collide_once(self, sprite_list):
        """Determine if there is at least one
        collision between this sprite and the list
        @param sprite_list - A list of sprites
        @returns - None - No Collision, or the first
        sprite to collide
        """
        for sprite in sprite_list:
            if (self.intersect(sprite)):
                return sprite
        return None
