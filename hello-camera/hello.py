import time
from picamera import PiCamera
from PIL import Image
try:
    from sense_hat import SenseHat
except ImportError:
    from sense_emu import SenseHat


def sequence(n_pics=20):
    '''Take a sequence of pictures.'''
    with PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.capture_sequence([
            'image%02d.jpg' % i
            for i in range(n_pics)
            ])
        camera.stop_preview()

if __name__ == '__main__':

    camera = PiCamera()
    hat = SenseHat()

    while True:

        # take picture
        camera.capture('snap.jpg')

        # convert to 8x8 pixels
        img = Image.open('snap.jpg').resize((8, 8))

        # display on sense hat
        hat.set_pixels(img.getdata())

        # save small image
        img.save('snap-small.jpg')

        # wait
        time.sleep(3)

    camera.close()
