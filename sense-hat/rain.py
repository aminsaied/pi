from sense_emu import SenseHat
import time
import numpy as np


s = SenseHat()

R = RED = (255, 0, 0)
G = GREEN = (0, 255, 0)
B = BLUE = (0, 0, 255)
E = EMPTY = (0, 0, 0)
W = WHITE = (255, 255, 255)
D = RAIN_DROP = (0, 10, 255)


class Drop:

    min_speed = 4
    max_speed = 8

    def __init__(self, col, tick_total, dim=8):
        self.row = -1
        self.col = col
        self.tick_count = tick_total
        self.tick_total = tick_total
        self.dim = dim

        self.blank = (0, 0, 0)
        self.rain = (0, 10, 255)

    def take_step(self, arr):
        self.tick_count -= 1
        if self.tick_count == 0:
            self.tick_count = self.tick_total
            arr[self.row][self.col] = self.blank
            if self.row == self.dim - 1:
                return arr, 'splash'
            else:
                self.row += 1
                arr[self.row][self.col] = self.rain
        return arr, None

    def destroy(self, arr):
        return arr

class Cloud:

    min_speed = 5
    max_speed = 11

    def __init__(self, tick_total, upper=1, dim=8):
        self.tick_count = tick_total
        self.tick_total = tick_total
        self.blank = (0, 0, 0)
        self.cloud = (255, 255, 255)
        self.dim = dim

        # fix rows
        self.upper = upper
        self.lower = upper + 1

        # fix columns
        self.upper_right = -1

    def take_step(self, arr):
        self.tick_count -= 1
        if self.tick_count == 0:
            self.tick_count = self.tick_total
            arr = self.shift_cloud(arr)
            if self.upper_right - 2 >= self.dim:
                return arr, 'poof'
        return arr, None

    def shift_cloud(self, arr):
        arr = self.decloud(self.upper_right - 2, arr)
        arr = self.encloud(self.upper_right + 1, arr)
        self.upper_right += 1
        return arr

    def decloud(self, col, arr):
        if col >= 0 and col < self.dim:
            arr[self.upper][col] = self.blank
            arr[self.lower][col] = self.blank
        return arr

    def encloud(self, col, arr):
        if col >= 0 and col < self.dim:
            arr[self.upper][col] = self.cloud
            arr[self.lower][col] = self.cloud
        return arr

    def destroy(self, arr):
        return arr


class Lightning:

    min_speed = 1
    max_speed = 4

    def __init__(self, tick_total, row, col, dim=8):
        self.tick_count = tick_total
        self.tick_total = tick_total
        self.yellow = (255,255,0)
        self.blank = (0, 0, 0)
        self.dim = dim
        
        self.row = row
        self.col = col

        self.row_prev = row
        self.col_prev = col

        self.row_prev2 = row
        self.col_prev2 = col

    def take_step(self, arr):
        self.tick_count -= 1
        if self.tick_count == 0:
            self.tick_count = self.tick_total
            arr = self.move_bolt(arr)
            if self.row < 0 or self.row >= self.dim or self.col < 0 or self.col >= self.dim:
                return arr, 'zapp'
        return arr, None
    
    def move_bolt(self, arr):

        p = np.random.rand()
        if p < 0.05:
            row_delta = 0
        elif p < 0.2:
            row_delta = -1
        else:
            row_delta = 1

        p = np.random.rand()
        if p < 0.05:
            col_delta = 0
        elif p < 0.35:
            col_delta = 1
        else:
            col_delta = -1
        
        arr = self.deblot(self.row_prev2, self.col_prev2, arr)
        
        self.row_prev2 = self.row_prev
        self.col_prev2 = self.col_prev

        self.row_prev = self.row
        self.col_prev = self.col

        self.row += row_delta
        self.col += col_delta
        
        arr = self.enbolt(self.row, self.col, arr)

        return arr

    def deblot(self, row, col, arr):
        if row >= 0 and row < self.dim and col >= 0 and col < self.dim:
            arr[row][col] = self.blank
        return arr
    
    def enbolt(self, row, col, arr):
        if row >= 0 and row < self.dim and col >= 0 and col < self.dim:
            arr[row][col] = self.yellow
        return arr

    def destroy(self, arr):
        arr = self.deblot(self.row, self.col, arr)
        arr = self.deblot(self.row_prev, self.col_prev, arr)
        arr = self.deblot(self.row_prev2, self.col_prev2, arr)
        return arr


class Rain:

    def __init__(self, tick_duration=0.1):
        '''
        Args:
            tick_duration (float): Set duration for time step.
        '''
        
        self.hat = SenseHat()

        self.dim = 8
        self.tick_duration = tick_duration

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

        self.drops = []
        self.clouds = []
        self.lightnings = []

    def set_tick_duration(self, tick_duration):
        self.tick_duration = tick_duration

    def show(self):
        arr_list = self.arr.reshape(64, -1).tolist()
        self.hat.set_pixels(arr_list)

    def random_drop(self):
        col = np.random.randint(0, self.dim)
        tick_total = np.random.randint(Drop.min_speed, Drop.max_speed)

        drop = Drop(col=col, tick_total=tick_total, dim=self.dim)
        self.drops.append(drop)

    def random_cloud(self):
        upper = 1 if np.random.rand() > 0.5 else 2
        tick_total = np.random.randint(Cloud.min_speed, Cloud.max_speed)
        cloud = Cloud(upper=upper, tick_total=tick_total, dim=self.dim)
        self.clouds.append(cloud)

    def random_lightning(self):
        row = np.random.randint(0, self.dim - 3)
        col = np.random.randint(0, self.dim)
        tick_total = np.random.randint(Lightning.min_speed, Lightning.max_speed)
        lightning = Lightning(tick_total=tick_total, row=row, col=col, dim=self.dim)
        self.lightnings.append(lightning)

    def step(self):

        next_drops = []
        for drop in self.drops:
            self.arr, x = drop.take_step(self.arr)
            if x != 'splash':
                next_drops.append(drop)
            else:
                self.arr = drop.destroy(self.arr)
        self.drops = next_drops

        next_clouds = []
        for cloud in self.clouds:
            self.arr, x = cloud.take_step(self.arr)
            if x != 'poof':
                next_clouds.append(cloud)
            else:
                self.arr = cloud.destroy(self.arr)
        self.clouds = next_clouds

        next_lightninigs = []
        for lightning in self.lightnings:
            self.arr, x = lightning.take_step(self.arr)
            if x != 'zapp':
                next_lightninigs.append(lightning)
            else:
                self.arr = lightning.destroy(self.arr)
        self.lightnings = next_lightninigs

    def run(self, steps, tick_duration=0.1):
        self.set_tick_duration(tick_duration)
        for _ in range(steps):
            if np.random.rand() < 0.12:
                self.random_drop()
            if np.random.rand() < 0.01:
                self.random_cloud()
            if np.random.rand() < 0.01:
                self.random_lightning()
            self.step()
            self.show()
            time.sleep(self.tick_duration)

if __name__ == '__main__':
    rain = Rain()
    # rain.hat.show_message("LET IT RAIN!", text_colour=[255, 75, 0])
    rain.run(steps=1000, tick_duration=0.05)
    rain.hat.clear()