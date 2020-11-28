'''Some 8x8 pixel art.
'''
import numpy as np

class Special:
    o = (255,103,0)
    g = (176,191,26)
    w = (255, 255, 255)
    b = (0, 0, 0)
    pumpkin = [
        w, w, w, w, g, w, w, w,
        w, w, o, o, o, o, w, w,
        w, o, b, o, o, b, o, w,
        o, b, b, o, o, b, b, o,
        o, o, o, o, o, o, o, o,
        o, b, o, o, o, o, b, o,
        w, o, b, b, b, b, o, w,
        w, w, o, o, o, o, w, w,
    ]

    @staticmethod
    def random():
        random_rgb = lambda : (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        arr = [random_rgb() for _ in range(64)]
        return arr

class Face:
    y = (250,250,55)
    w = (255, 255, 255)
    b = (0, 0, 0)
    happy = [
        w, w, y, y, y, y, w, w,
        w, y, b, y, y, b, y, w, 
        y, b, b, y, y, b, b, y,
        y, y, y, y, y, y, y, y,
        y, b, y, y, y, y, b, y,
        y, b, b, y, y, b, b, y,
        w, y, b, b, b, b, y, w,
        w, w, y, y, y, y, w, w,
    ]
    sad = [
        w, w, y, y, y, y, w, w,
        w, y, b, y, y, b, y, w, 
        y, b, b, y, y, b, b, y,
        y, y, y, y, y, y, y, y,
        y, y, b, b, b, b, y, y,
        y, b, b, y, y, b, b, y,
        w, b, y, y, y, y, b, w,
        w, w, y, y, y, y, w, w,
    ]
    wink_left = [
        w, w, y, y, y, y, w, w,
        w, y, y, y, y, b, y, w, 
        y, b, b, y, y, b, b, y,
        y, y, y, y, y, y, y, y,
        y, b, y, y, y, y, b, y,
        y, b, b, y, y, b, b, y,
        w, y, b, b, b, b, y, w,
        w, w, y, y, y, y, w, w,
    ]
    wink_right = [
        w, w, y, y, y, y, w, w,
        w, y, b, y, y, y, y, w, 
        y, b, b, y, y, b, b, y,
        y, y, y, y, y, y, y, y,
        y, b, y, y, y, y, b, y,
        y, b, b, y, y, b, b, y,
        w, y, b, b, b, b, y, w,
        w, w, y, y, y, y, w, w,
    ]
    blink = [
        w, w, y, y, y, y, w, w,
        w, y, y, y, y, y, y, w, 
        y, b, b, y, y, b, b, y,
        y, y, y, y, y, y, y, y,
        y, b, y, y, y, y, b, y,
        y, b, b, y, y, b, b, y,
        w, y, b, b, b, b, y, w,
        w, w, y, y, y, y, w, w,
    ]
    shocked = [
        w, w, y, y, y, y, w, w,
        w, b, b, y, y, b, b, w, 
        y, b, b, y, y, b, b, y,
        y, y, y, y, y, y, y, y,
        y, y, b, b, b, b, y, y,
        y, y, b, y, y, b, y, y,
        w, y, b, b, b, b, y, w,
        w, w, y, y, y, y, w, w,
    ]
    cross = [
        w, w, y, y, y, y, w, w,
        w, y, b, y, y, y, b, w, 
        y, b, b, y, y, b, b, y,
        y, y, y, y, y, y, y, y,
        y, y, y, y, y, y, y, y,
        y, y, b, b, b, b, y, y,
        w, y, y, y, y, y, y, w,
        w, w, y, y, y, y, w, w,
    ]

class Animal:
    p = (224,33,138)
    w = (255, 255, 255)
    b = (0, 0, 0)
    s = (152,118,84)
    r = (255, 0, 0)
    pig = [
        w, p, p, p, p, p, p, w,
        p, p, p, p, p, p, p, p,
        b, w, p, p, p, p, w, b,
        p, p, p, p, p, p, p, p,
        p, p, s, s, s, s, p, p,
        p, p, r, s, s, r, p, p,
        p, p, s, s, s, s, p, p,
        w, p, p, p, p, p, p, w,
    ]

if __name__ == '__main__':

    from sense_emu import SenseHat
    import time

    hat = SenseHat()
    epsilon = 0.5

    # faces
    hat.set_pixels(Face.happy)
    time.sleep(epsilon)
    hat.set_pixels(Face.sad)
    time.sleep(epsilon)
    hat.set_pixels(Face.wink_left)
    time.sleep(epsilon)
    hat.set_pixels(Face.blink)
    time.sleep(epsilon)
    hat.set_pixels(Face.wink_right)
    time.sleep(epsilon)
    hat.set_pixels(Face.shocked)
    time.sleep(epsilon)
    hat.set_pixels(Face.cross)
    time.sleep(epsilon)

    # animals
    hat.set_pixels(Animal.pig)
    time.sleep(epsilon)

    # special
    hat.set_pixels(Special.pumpkin)
    time.sleep(epsilon)
    for _ in range(5):
        hat.set_pixels(Special.random())
        time.sleep(epsilon)
