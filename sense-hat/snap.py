'''Take picture with camera module and convert to sense hat's 8x8 light grid.
'''
try:
    from sense_hat import SenseHat
except ImportError:
    from sense_emu import SenseHat
import time
from PIL import Image
import os


class Snap:

    def __init__(self):
        self.hat = SenseHat()
        self.hat.clear()
        self.dim = 8

    def show_image(self, image_name: str):
        # open file
        image_file = os.path.join('static', image_name)
        img = Image.open(image_file)
        
        # convert to rgb
        rgb_img = img.convert('RGB')
        
        # resize to 8x8 pixels
        rgb_img_small = rgb_img.resize((self.dim, self.dim))
        
        # get pixel data
        hat_img = rgb_img_small.getdata()
        
        # display on sense hat
        self.hat.set_pixels(hat_img)

if __name__ == '__main__':

    snap = Snap()
    snap.show_image('unicorn.jpg')
    time.sleep(10)
    snap.hat.clear()

