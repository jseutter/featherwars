#!/usr/bin/env python

from pyglet import window
from pyglet import clock
from pyglet import font
import random

import helper
from bird import Bird
from bullet import Bullet


class MainWindow(window.Window):

	def __init__(self, *args, **kwargs):
		self.max_monsters = 30
		#Let all of the standard stuff pass through
		window.Window.__init__(self, *args, **kwargs)
		# comment back in later
		#self.set_mouse_visible(False)
		self.init_sprites()

	def init_sprites(self):
		self.bullets = []
		self.bird = Bird(self.width - 150, 10, x=100,y=100)
		self.bullet_image = helper.load_image("bullet.png")
		
	def main_loop(self):
		clock.set_fps_limit(30)

		while not self.has_exit:
			self.dispatch_events()
			self.clear()

			self.update()
			self.draw()

			#Tick the clock
			clock.tick()

			self.flip()

	def update(self):
		
		# update bullets
		for sprite in self.bullets:
			sprite.update()

		self.bird.update()
		

	def draw(self):

		for sprite in self.bullets:
			sprite.draw()
		
		self.bird.draw()

	
	"""******************************************
	Event Handlers
	*********************************************"""
	def on_mouse_motion(self, x, y, dx, dy):
		self.bird.x = x
		self.bird.y = y

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.bird.x = x
		self.bird.y = y

	def on_mouse_press(self, x, y, button, modifiers):

		if (button == 1):
			self.bullets.append(Bullet(self.bird
					, self.bullet_image
					, self.height
					, x=x + (self.bird.image.width / 2) - (self.bullet_image.width / 2)
					, y=y))






if __name__ == "__main__":
	# Someone is launching this directly
	main = MainWindow()
	main.main_loop()

