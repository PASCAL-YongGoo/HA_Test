"""The playfield grid: locking pieces, collision checks and line clearing."""

from config import COLS, ROWS


class Board:
    """A COLS x ROWS grid. Empty cells are None, filled cells store a color."""

    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def reset(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def inside(self, x, y):
        """True if (x, y) is within horizontal bounds and not below the floor.

        Cells above the top (y < 0) are allowed so pieces can spawn/rotate
        partly off-screen, which is standard behaviour.
        """
        return 0 <= x < COLS and y < ROWS

    def valid(self, cells):
        """True if every cell is in-bounds and not overlapping a locked block."""
        for x, y in cells:
            if not self.inside(x, y):
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True

    def lock(self, piece):
        """Freeze a piece's cells into the grid."""
        for x, y in piece.cells():
            if 0 <= y < ROWS and 0 <= x < COLS:
                self.grid[y][x] = piece.color

    def clear_lines(self):
        """Remove full rows and drop everything above. Returns lines cleared."""
        remaining = [row for row in self.grid if any(c is None for c in row)]
        cleared = ROWS - len(remaining)
        if cleared:
            empty = [[None for _ in range(COLS)] for _ in range(cleared)]
            self.grid = empty + remaining
        return cleared
