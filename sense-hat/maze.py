import random
import time
from typing import Optional

import numpy as np

try:
    from sense_hat import SenseHat
except ImportError:
    from sense_emu import SenseHat

from art import Special, Face
from maze_graph import Graph

HAT_DIM = 8
# set maze colors
BALL_COLOR = (255, 0, 0)
TARGET_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other_point):
        return self.x == other_point.x and self.y == other_point.y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y

    @classmethod
    def random(cls, max_x: int = HAT_DIM, max_y: int = HAT_DIM):
        i = np.random.randint(max_x)
        j = np.random.randint(max_y)
        return cls(x=i, y=j)

class Layout:
    def __init__(self, arr, start, end):
        self.arr = arr
        self.start = Point(start[0], start[1])
        self.end = Point(end[0], end[1])
    
    def check_pixel(self, x, y):
        if self.arr[x, y] == 0:
            return True
        return False

    def set_layout(self, hat, wall_color=WALL_COLOR, background_color=BACKGROUND_COLOR):
        dim = len(self.arr)
        for i in range(dim):
            for j in range(dim):
                if self.arr[i][j] == 1:
                    hat.set_pixel(i, j, wall_color)
                else:
                    hat.set_pixel(i, j, background_color)

    @staticmethod
    def point_to_vertex(point, arr):
        _, m = arr.shape
        return point.x * m + point.y

    def is_solvable_from_array(arr, start, end):
        graph = Graph.from_maze_array(arr)
        start_vertex = Graph.point_to_vertex(start, arr)
        end_vertex = Graph.point_to_vertex(end, arr)
        return graph.is_solvable(start_vertex, end_vertex)

    @classmethod
    def generate_random_layout(
        cls,
        hat: SenseHat,
        initial_layout: Optional["Layout"] = None,
        patience: Optional[int] = 5,
        is_additive: bool = True,
        ):
        """Generates random solvable layout based on initial starting array."""
        if initial_layout is None:
            n = HAT_DIM
            arr = np.zeros((n, n))
            start = Point(0, 0)
            end = Point(n - 1, n - 1)
            layout = cls(arr=arr, start=start, end=end)
        else:
            layout = initial_layout

        layout.set_layout(hat)

        start_time = time.time()

        while time.time() - start_time < patience:
            while Graph.is_solvable_from_array(arr=layout.arr, start=layout.start, end=layout.end):
                time.sleep(0.08)
                r = Point.random()
                if r == layout.start or r == layout.end:
                    continue
                if is_additive:    
                    layout.arr[r.x, r.y] = 1
                else:
                    layout.arr[r.x, r.y] = (layout.arr[r.x, r.y] + 1) % 2
                layout.set_layout(hat)

            # remove last point
            layout.arr[r.x, r.y] = 0
            layout.set_layout(hat)

        return layout
        

class Maze:

    def __init__(self, layout: Layout, hat: Optional[SenseHat] = None, dim: int = 8):
        self.dim = dim

        # prep hat
        if hat is None:
            self.hat = SenseHat()
            self.hat.clear()
        else:
            self.hat = hat

        # set maze colors
        self.ball_color = BALL_COLOR
        self.target_color = TARGET_COLOR
        self.background_color = BACKGROUND_COLOR
        self.wall_color = WALL_COLOR

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

def initial_layouts():
    layouts = []
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
    layouts.append(layout)

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
    layouts.append(layout)

    return layouts

if __name__ == '__main__':

    hat = SenseHat()
    hat.clear()

    score = 9

    layouts = initial_layouts()

    while True:

        if np.random.rand() < 0.7:
            layout = Layout.generate_random_layout(
                hat=hat,
                patience=score,
                )
        else:
            initial_layout = random.choice(layouts)
            layout = Layout.generate_random_layout(
                hat=hat,
                initial_layout=initial_layout,
                patience=min(score, 5),
                is_additive=False,
                )
        
        maze = Maze(layout=layout)
        maze.hat.low_light = True
        maze.run()
        hat.clear()
        
        score += 1
        if len(str(score)) == 1:
            hat.show_letter(str(score))
        else:
            hat.show_message(text_string=str(score))
        
        time.sleep(1)
