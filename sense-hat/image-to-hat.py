'''Convert image to SenseHat light grid.
'''
from sense_emu import SenseHat
import time
from PIL import Image
import os


# Open image file
image_file = os.path.join('images', 'pi-logo.png')
print(image_file)
img = Image.open(image_file)

# Generate rgb values for image pixels
rgb_img = img.convert('RGB')

sense_hat = SenseHat()

x_step = rgb_img.width // 7
y_step = rgb_img.height // 7

for i in range(8):
    x = i * x_step
    for j in range(8):
        y = j * y_step
        xy = (x, y)
        rgb = rgb_img.getpixel(xy)
        sense_hat.set_pixel(i, j, rgb)

time.sleep(10)

sense_hat.clear()