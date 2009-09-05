from pyglet.gl import *
from pyglet import image
import os

# Load Bitmaps And Convert To Textures
def LoadGLTextures(filename):
    print os.getcwd()
    pic = image.load(filename)
    texture = pic.get_texture()
    glEnable(texture.target)
    return texture

def get_image_dir():
	"""Get the directory used to store the images
	@returns string - the directory
	"""
	directory = os.path.abspath(os.path.dirname(__file__))
	directory = os.path.join(directory, '../data')
	return directory

def load_image(image_file_name):

	full_path = os.path.join(get_image_dir(), image_file_name)
	return image.load(full_path)
