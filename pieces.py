"""Tetromino definitions and the Piece class.

Each shape is defined by its rotation states as a list of (col, row) offsets.
Offsets are relative to the piece's top-left origin so rotation is simply a
matter of swapping to the next state in the list.
"""

import random

from config import PIECE_COLORS

# Rotation states for each piece. Every state is a list of (x, y) cell offsets
# within a 4x4 (or 3x3 / 2x2) bounding box. Keeping explicit states avoids any
# ambiguity in rotation direction and keeps the classic Tetris look.
SHAPES = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    "O": [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

PIECE_TYPES = list(SHAPES.keys())


class Piece:
    """A single falling tetromino with a position and rotation state."""

    def __init__(self, kind, x=3, y=0):
        self.kind = kind
        self.color = PIECE_COLORS[kind]
        self.x = x                       # column of the piece origin
        self.y = y                       # row of the piece origin
        self.rotation = 0                # index into SHAPES[kind]

    @property
    def states(self):
        return SHAPES[self.kind]

    def cells(self, rotation=None, x=None, y=None):
        """Return absolute (col, row) board coordinates for the piece.

        Optional overrides let callers test a hypothetical rotation/position
        (used for collision checks and wall kicks) without mutating the piece.
        """
        rotation = self.rotation if rotation is None else rotation
        x = self.x if x is None else x
        y = self.y if y is None else y
        state = self.states[rotation % len(self.states)]
        return [(x + dx, y + dy) for dx, dy in state]

    def next_rotation(self):
        return (self.rotation + 1) % len(self.states)

    def copy(self):
        clone = Piece(self.kind, self.x, self.y)
        clone.rotation = self.rotation
        return clone


class Bag:
    """7-bag randomizer: yields all 7 pieces in random order before repeating.

    This is the standard Tetris randomizer and prevents long droughts of any
    particular piece.
    """

    def __init__(self):
        self._items = []

    def next(self):
        if not self._items:
            self._items = PIECE_TYPES[:]
            random.shuffle(self._items)
        return Piece(self._items.pop())
