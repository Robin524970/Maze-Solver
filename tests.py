import unittest
from maze import Maze
from graphics import Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        win = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    def test_break_entrance_and_exit(self):
        win = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        m1._break_entrance_and_exit()
        self.assertFalse(
            m1._cells[0][0].has_top_wall
        )
        self.assertFalse(
            m1._cells[-1][-1].has_bottom_wall
        )

    def test_reset_cells_visisted(self):
        win = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        for col in m1._cells:
            for cell in col:
                self.assertFalse(cell.visited)
if __name__ == "__main__":
    unittest.main()