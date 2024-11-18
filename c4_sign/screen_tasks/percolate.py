import random
from c4_sign.base_task import ScreenTask
from c4_sign.consts import COLOR_GRAY, COLOR_TEAL

def percolates(grid):
    # check if the grid percolates
    # if there is a path from the top to a cell, set the cell to 2
    for x in range(32):
        if grid[x][0] == 1:
            grid[x][0] = 2
    changed = True

    while changed:
        changed = False
        for x in range(32):
            for y in range(31):
                if grid[x][y] == 2:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 32 and 0 <= ny < 32 and grid[nx][ny] == 1:
                            grid[nx][ny] = 2
                            changed = True
    # check if any cell in the bottom row is 2
    for x in range(32):
        if grid[x][31] == 2:
            return True
    return False

class Percolate(ScreenTask):
    title = "Percolate"
    artist = "Luna"
    
    def prepare(self):
        self.grid = [[0 for _ in range(32)] for _ in range(32)]
        return super().prepare()
    
    def draw_frame(self, canvas, delta_time):
        # each frame, add a new block somewhere on the grid if it's empty
        if not percolates(self.grid):
            while True:
                x, y = random.randint(0, 31), random.randint(0, 31)
                if self.grid[x][y] == 0:
                    self.grid[x][y] = 1
                    break
        # check if the grid percolates
        # copy grid to canvas
        result = percolates(self.grid)
        for x in range(32):
            for y in range(32):
                if self.grid[x][y] == 1:
                    canvas.set_pixel(x, y, COLOR_GRAY)
                elif self.grid[x][y] == 2:
                    canvas.set_pixel(x, y, COLOR_TEAL)
        return result
