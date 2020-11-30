try:
    from sense_hat import SenseHat
except ImportError:
    from sense_emu import SenseHat
import time
import numpy as np
from art import Special, Face

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Layout:
    def __init__(self, arr, start, end):
        self.arr = arr
        self.start = Point(start[0], start[1])
        self.end = Point(end[0], end[1])
    
    def check_pixel(self, x, y):
        if self.arr[x, y] == 0:
            return True
        return False
        

class Maze:

    def __init__(self, layout: Layout, dim: int=8):
        self.dim = dim

        # prep hat
        self.hat = SenseHat()
        self.hat.clear()

        # set maze colors
        self.ball_color = (255, 0, 0)
        self.target_color = (0, 255, 0)
        self.background_color = (0, 0, 0)
        self.wall_color = (255, 255, 255)

        # set the layout of the maze
        self.layout = layout
        self.set_layout()

        # create ball
        self.x = self.layout.start.x
        self.y = self.layout.start.y
        self.hat.set_pixel(self.x, self.y, self.ball_color)

        # create target
        self.target_x = self.layout.end.x
        self.target_y = self.layout.end.y
        self.hat.set_pixel(self.target_x, self.target_y, self.target_color)

        # is ball == target?
        self.done = False

    def set_layout(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.layout.arr[i][j] == 1:
                    self.hat.set_pixel(i, j, self.wall_color)

    def celebrate_win(self):
        for _ in range(10):
            self.hat.set_pixels(Special.random())
            time.sleep(0.25)
        self.hat.set_pixels(Face.happy)
        time.sleep(1)
        self.hat.set_pixels(Face.wink_left)
        time.sleep(0.3)
        self.hat.set_pixels(Face.happy)
        time.sleep(1)

    def move_ball(self, direction):

        self.hat.set_pixel(self.x, self.y, self.background_color)

        if direction == 'up':
            if self.y - 1 >= 0:
                if self.layout.arr[self.x][self.y - 1] == 0:
                    self.y -= 1
        elif direction == 'down':
            if self.y + 1 < self.dim:
                if self.layout.arr[self.x][self.y + 1] == 0:
                    self.y += 1
        elif direction == 'left':
            if self.x - 1 >= 0:
                if self.layout.arr[self.x - 1][self.y] == 0:
                    self.x -= 1
        elif direction == 'right':
            if self.x + 1 < self.dim:
                if self.layout.arr[self.x + 1][self.y] == 0:
                    self.x += 1

        self.hat.set_pixel(self.x, self.y, self.ball_color)

    def run(self):
        
        while self.done is False:

            # read joystick input
            action = None
            while action not in ['pressed', 'held']:
                event = self.hat.stick.wait_for_event(emptybuffer=True)
                action = event.action

            self.move_ball(event.direction)

            if self.x == self.target_x and self.y == self.target_y:
                self.done = True
        
        self.celebrate_win()


if __name__ == '__main__':
    
    arr = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1,],
        [0, 0, 0, 0, 0, 0, 0, 0,],
        [1, 1, 1, 1, 1, 1, 1, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 1, 1, 1, 1, 1, 1, 1,],
        [0, 1, 0, 0, 0, 1, 0, 0,],
        [0, 1, 0, 1, 0, 1, 0, 1,],
        [0, 0, 0, 1, 0, 0, 0, 1,],
    ]).T
    start = (0, 1)
    end = (7, 5)

    layout = Layout(
        arr=arr,
        start=start,
        end=end,
    )
    
    maze = Maze(layout=layout)
    maze.hat.low_light = True
    maze.run()

    arr = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1,],
        [0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 1, 1, 1, 1, 0, 1, 0,],
        [0, 0, 0, 0, 0, 0, 1, 0,],
        [0, 1, 1, 1, 1, 1, 1, 1,],
        [0, 1, 0, 0, 0, 1, 0, 0,],
        [0, 1, 0, 1, 0, 1, 0, 1,],
        [0, 0, 0, 1, 0, 0, 0, 1,],
    ])
    start = (5, 7)
    end = (3, 7)

    layout = Layout(
        arr=arr,
        start=start,
        end=end,
    )

    maze = Maze(layout=layout)
    maze.hat.low_light = True
    maze.run()

    maze.hat.clear()

    arr = np.array([
        [0, 0, 0, 1, 1, 0, 0, 0,],
        [0, 1, 0, 0, 0, 0, 1, 0,],
        [0, 1, 1, 1, 1, 1, 1, 1,],
        [0, 1, 0, 1, 0, 0, 0, 1,],
        [0, 1, 0, 1, 0, 1, 0, 1,],
        [0, 1, 0, 1, 1, 1, 0, 1,],
        [0, 0, 0, 0, 0, 0, 0, 1,],
        [1, 1, 1, 1, 1, 1, 1, 1,],
    ]).T
    start = (4, 4)
    end = (7, 1)

    layout = Layout(
        arr=arr,
        start=start,
        end=end,
    )
    
    maze = Maze(layout=layout)
    maze.hat.low_light = True
    maze.run()