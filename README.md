# Tetris

A complete, playable Tetris game built with Python and Pygame. It features all
seven standard tetrominoes, ghost piece, next-piece preview, hold, increasing
levels, scoring, and synthesized sound effects.

![Tetris](https://img.shields.io/badge/python-3.8%2B-blue) ![Pygame](https://img.shields.io/badge/pygame-2.x-green)

## Features

- All 7 tetromino pieces (I, O, T, S, Z, J, L) with a vibrant color scheme
- 7-bag randomizer for fair piece distribution
- Ghost piece showing where the current piece will land
- Next-piece preview and **hold** functionality
- Line clearing with classic scoring (100 / 300 / 500 / 800, scaled by level)
- Levels that speed up gravity as you clear more lines
- Wall-kick rotations near the borders
- Game-over detection with instant restart
- Optional synthesized sound effects (no audio files needed)

## Requirements

- Python 3.8+
- [Pygame](https://www.pygame.org/) (required)
- [NumPy](https://numpy.org/) (optional — enables sound effects)

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Controls

| Key            | Action        |
| -------------- | ------------- |
| ← / →          | Move left / right |
| ↑              | Rotate        |
| ↓              | Soft drop     |
| Space          | Hard drop     |
| C              | Hold piece    |
| R              | Restart       |
| Esc            | Quit          |

## Scoring

| Lines cleared | Base points |
| ------------- | ----------- |
| 1             | 100         |
| 2             | 300         |
| 3             | 500         |
| 4 (Tetris)    | 800         |

Line-clear points are multiplied by the current level. Soft drops earn 1 point
per cell and hard drops earn 2 points per cell. Every 10 lines advances the
level and increases the falling speed.

## Project Structure

```
.
├── main.py            # Entry point and main loop
├── game.py            # Core game logic and rendering
├── board.py           # Playfield grid, collision, line clearing
├── pieces.py          # Tetromino shapes, Piece class, 7-bag randomizer
├── sounds.py          # Optional synthesized sound effects
├── config.py          # Dimensions, colors, timing and scoring constants
├── requirements.txt
└── README.md
```
