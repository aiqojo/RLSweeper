def calculate_nearby(self):
        xr, yr = self.grid.shape
        for i in range(xr):
            for j in range(yr):
                self.count_near_mines(i, j)

    def count_near_mines(self, x, y):
        if self.grid[x][y] == -1:
            return

        dx = [0, 1, 0, -1]
        dy = [-1, 0, 1, 0]
        ret = 0

        for a in dx:
            for b in dy:
                if self.check_bounds(x + a, y + b):
                    if self.grid[x + a][y + b] == -1:
                        # print(x, y, "mine at:", x + a, y + b)
                        ret += 1

        if self.grid[x][y] != -1:
            self.grid[x][y] = ret