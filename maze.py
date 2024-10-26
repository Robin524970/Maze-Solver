from cell import Cell
import random
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed != None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self._num_cols-1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True
        while True:
            to_visit = []
            # check_top
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1, 0))
            # check_bottom
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                to_visit.append((i,j+1,2))
            # check_left
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j,3))
            # check_right
            if i < self._num_cols-1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j,1))
            # No where to go
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            
            cell = random.randrange(0, len(to_visit))
            col, row, dir = to_visit.pop(cell)

            if dir == 0: # top
                current.has_top_wall = False
                self._cells[col][row].has_bottom_wall = False
            if dir == 2: # bottom
                current.has_bottom_wall = False
                self._cells[col][row].has_top_wall = False
            if dir == 1: # right
                current.has_right_wall = False
                self._cells[col][row].has_left_wall = False
            if dir == 3: # left
                current.has_left_wall = False
                self._cells[col][row].has_right_wall = False
            self._break_walls_r(col, row)
                
    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
    
    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i = 0, j = 0):
        num_cols = len(self._cells)
        num_rows = len(self._cells[0])
        self._animate()
        self._cells[i][j].visited = True
        if i == num_cols-1 and j == num_rows-1:
            return True
        # check_top
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j-1].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            result = self._solve_r(i, j-1)
            if result:
                return True
            self._cells[i][j].draw_move(self._cells[i][j-1], True)

        # check_bottom
        if j < self._num_rows - 1 and not self._cells[i][j+1].visited and not self._cells[i][j+1].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            result = self._solve_r(i, j+1)
            if result:
                return True
            self._cells[i][j].draw_move(self._cells[i][j+1], True)

        # check_left
        if i > 0 and not self._cells[i-1][j].visited and not self._cells[i-1][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            result = self._solve_r(i-1, j)
            if result:
                return True
            self._cells[i][j].draw_move(self._cells[i-1][j], True)

        # check_right
        if i < self._num_cols-1 and not self._cells[i+1][j].visited and not self._cells[i+1][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            result = self._solve_r(i+1, j)
            if result:
                return True
            self._cells[i][j].draw_move(self._cells[i+1][j], True)

        return False
