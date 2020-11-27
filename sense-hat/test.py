from sense_emu import SenseHat
import time
import numpy as np


s = SenseHat()

R = RED = (255, 0, 0)
G = GREEN = (0, 255, 0)
B = BLUE = (0, 0, 255)
E = EMPTY = (0, 0, 0)
W = WHITE = (255, 255, 255)


class LightMatrix:

    def __init__(self):
        
        self.hat = SenseHat()

        self.dim = 8

        self.arr = np.array([
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]).reshape(8, 8, -1)

    def show(self):
        arr_list = self.arr.reshape(64, -1).tolist()
        self.hat.set_pixels(arr_list)

    def set_row(self, row_num, color):
        for i in range(self.dim):
            self.arr[row_num][i] = color

        print(self.arr)


if __name__ == '__main__':

    lm = LightMatrix()

    lm.show()

    lm.set_row(1, RED)
    lm.set_row(2, BLUE)
    lm.set_row(3, GREEN)
    lm.set_row(4, WHITE)
    lm.set_row(5, RED)
    lm.set_row(6, BLUE)

    lm.show()

    time.sleep(5)

    lm.hat.clear()