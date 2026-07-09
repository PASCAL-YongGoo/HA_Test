"""Core game logic and rendering for Tetris."""

import pygame

import config as cfg
from board import Board
from pieces import Bag, Piece
from sounds import SoundManager

# Simple wall-kick offsets tried in order when a rotation is blocked. Not the
# full SRS table, but enough to make rotations near walls feel natural.
WALL_KICKS = [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)]


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 22)
        self.big_font = pygame.font.SysFont("consolas", 40, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 16)
        self.sound = SoundManager()
        self.reset()

    # -- Setup --------------------------------------------------------------
    def reset(self):
        """Start a brand new game."""
        self.board = Board()
        self.bag = Bag()
        self.current = self.bag.next()
        self.next_piece = self.bag.next()
        self.hold_piece = None
        self.hold_used = False        # only one hold swap per drop
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.fall_timer = 0
        self._spawn_current()

    def _spawn_current(self):
        """Place the current piece at the top; detect immediate game over."""
        self.current.x, self.current.y, self.current.rotation = 3, 0, 0
        if not self.board.valid(self.current.cells()):
            self.game_over = True
            self.sound.play("gameover")

    def _fall_delay(self):
        """Milliseconds between gravity steps for the current level."""
        delay = cfg.BASE_FALL_MS - (self.level - 1) * cfg.FALL_STEP_MS
        return max(cfg.MIN_FALL_MS, delay)

    # -- Piece movement -----------------------------------------------------
    def _move(self, dx, dy):
        """Try to shift the current piece. Returns True on success."""
        cells = self.current.cells(x=self.current.x + dx, y=self.current.y + dy)
        if self.board.valid(cells):
            self.current.x += dx
            self.current.y += dy
            return True
        return False

    def _rotate(self):
        """Rotate with wall kicks so rotations near walls still work."""
        new_rot = self.current.next_rotation()
        for kx, ky in WALL_KICKS:
            cells = self.current.cells(
                rotation=new_rot,
                x=self.current.x + kx,
                y=self.current.y + ky,
            )
            if self.board.valid(cells):
                self.current.rotation = new_rot
                self.current.x += kx
                self.current.y += ky
                self.sound.play("rotate")
                return

    def _hard_drop(self):
        """Drop the piece straight down and lock it."""
        distance = 0
        while self._move(0, 1):
            distance += 1
        self.score += distance * cfg.HARD_DROP_POINTS
        self.sound.play("drop")
        self._lock_current()

    def _soft_drop(self):
        if self._move(0, 1):
            self.score += cfg.SOFT_DROP_POINTS

    def _hold(self):
        """Swap the current piece with the held one (once per drop)."""
        if self.hold_used:
            return
        self.hold_used = True
        if self.hold_piece is None:
            self.hold_piece = Piece(self.current.kind)
            self.current = self.next_piece
            self.next_piece = self.bag.next()
        else:
            self.current, self.hold_piece = (
                Piece(self.hold_piece.kind),
                Piece(self.current.kind),
            )
        self._spawn_current()

    def _lock_current(self):
        """Freeze the piece, clear lines, update score and spawn the next one."""
        self.board.lock(self.current)
        cleared = self.board.clear_lines()
        if cleared:
            self.score += cfg.LINE_SCORES.get(cleared, 0) * self.level
            self.lines += cleared
            new_level = self.lines // cfg.LINES_PER_LEVEL + 1
            if new_level > self.level:
                self.level = new_level
                self.sound.play("level")
            else:
                self.sound.play("clear")

        self.current = self.next_piece
        self.next_piece = self.bag.next()
        self.hold_used = False
        self._spawn_current()

    def _ghost_y(self):
        """Row the current piece would land on if hard dropped."""
        y = self.current.y
        while self.board.valid(self.current.cells(y=y + 1)):
            y += 1
        return y

    # -- Event / update loop ------------------------------------------------
    def handle_key(self, key):
        if self.game_over:
            if key == pygame.K_r:
                self.reset()
            return

        if key == pygame.K_LEFT:
            if self._move(-1, 0):
                self.sound.play("move")
        elif key == pygame.K_RIGHT:
            if self._move(1, 0):
                self.sound.play("move")
        elif key == pygame.K_DOWN:
            self._soft_drop()
        elif key == pygame.K_UP:
            self._rotate()
        elif key == pygame.K_SPACE:
            self._hard_drop()
        elif key == pygame.K_c:
            self._hold()
        elif key == pygame.K_r:
            self.reset()

    def update(self, dt):
        """Advance gravity by dt milliseconds."""
        if self.game_over:
            return
        self.fall_timer += dt
        if self.fall_timer >= self._fall_delay():
            self.fall_timer = 0
            if not self._move(0, 1):
                self._lock_current()

    # -- Rendering ----------------------------------------------------------
    def draw(self):
        self.screen.fill(cfg.BG_COLOR)
        self._draw_playfield()
        self._draw_panel()
        if self.game_over:
            self._draw_game_over()

    def _cell_rect(self, col, row):
        px = cfg.MARGIN + col * cfg.CELL
        py = cfg.MARGIN + row * cfg.CELL
        return pygame.Rect(px, py, cfg.CELL, cfg.CELL)

    def _draw_block(self, rect, color, outline=True):
        pygame.draw.rect(self.screen, color, rect)
        if outline:
            # A lighter top-left edge gives blocks a subtle beveled look.
            light = tuple(min(255, c + 50) for c in color)
            dark = tuple(max(0, c - 60) for c in color)
            pygame.draw.line(self.screen, light, rect.topleft, rect.topright)
            pygame.draw.line(self.screen, light, rect.topleft, rect.bottomleft)
            pygame.draw.line(self.screen, dark, rect.bottomleft, rect.bottomright)
            pygame.draw.line(self.screen, dark, rect.topright, rect.bottomright)

    def _draw_playfield(self):
        # Outer wall/border.
        wall = pygame.Rect(
            cfg.MARGIN - cfg.BORDER,
            cfg.MARGIN - cfg.BORDER,
            cfg.PLAY_WIDTH + cfg.BORDER * 2,
            cfg.PLAY_HEIGHT + cfg.BORDER * 2,
        )
        pygame.draw.rect(self.screen, cfg.BORDER_COLOR, wall, cfg.BORDER)

        # Grid lines.
        for col in range(cfg.COLS + 1):
            x = cfg.MARGIN + col * cfg.CELL
            pygame.draw.line(self.screen, cfg.GRID_COLOR,
                             (x, cfg.MARGIN), (x, cfg.MARGIN + cfg.PLAY_HEIGHT))
        for row in range(cfg.ROWS + 1):
            y = cfg.MARGIN + row * cfg.CELL
            pygame.draw.line(self.screen, cfg.GRID_COLOR,
                             (cfg.MARGIN, y), (cfg.MARGIN + cfg.PLAY_WIDTH, y))

        # Locked blocks.
        for row in range(cfg.ROWS):
            for col in range(cfg.COLS):
                color = self.board.grid[row][col]
                if color:
                    self._draw_block(self._cell_rect(col, row), color)

        if self.game_over:
            return

        # Ghost piece.
        ghost_y = self._ghost_y()
        for col, row in self.current.cells(y=ghost_y):
            if row >= 0:
                rect = self._cell_rect(col, row)
                pygame.draw.rect(self.screen, cfg.GHOST_COLOR, rect, 2)

        # Current piece.
        for col, row in self.current.cells():
            if row >= 0:
                self._draw_block(self._cell_rect(col, row), self.current.color)

    def _draw_panel(self):
        panel_x = cfg.MARGIN * 2 + cfg.PLAY_WIDTH
        panel = pygame.Rect(panel_x, cfg.MARGIN, cfg.PANEL_WIDTH, cfg.PLAY_HEIGHT)
        pygame.draw.rect(self.screen, cfg.PANEL_COLOR, panel, border_radius=8)

        pad = 16
        x = panel_x + pad
        y = cfg.MARGIN + pad

        def label(text, value, font=None):
            nonlocal y
            font = font or self.font
            self.screen.blit(font.render(text, True, cfg.TEXT_COLOR), (x, y))
            y += 26
            self.screen.blit(self.big_font.render(str(value), True, cfg.WHITE), (x, y))
            y += 50

        label("SCORE", self.score)
        label("LINES", self.lines)
        label("LEVEL", self.level)

        # Next piece preview.
        self.screen.blit(self.font.render("NEXT", True, cfg.TEXT_COLOR), (x, y))
        y += 30
        self._draw_preview(self.next_piece, x, y)
        y += 4 * cfg.CELL + 20

        # Hold piece preview.
        self.screen.blit(self.font.render("HOLD", True, cfg.TEXT_COLOR), (x, y))
        y += 30
        if self.hold_piece:
            self._draw_preview(self.hold_piece, x, y)

        # Controls hint at the bottom of the panel.
        hints = [
            "← →  move",
            "↑  rotate",
            "↓  soft drop",
            "space  hard drop",
            "C  hold",
            "R  restart",
        ]
        hy = cfg.MARGIN + cfg.PLAY_HEIGHT - len(hints) * 20 - pad
        for line in hints:
            self.screen.blit(self.small_font.render(line, True, cfg.TEXT_COLOR),
                             (x, hy))
            hy += 20

    def _draw_preview(self, piece, x, y):
        """Draw a piece inside a small 4x4 preview box."""
        cells = piece.states[0]
        min_x = min(c[0] for c in cells)
        min_y = min(c[1] for c in cells)
        for dx, dy in cells:
            rect = pygame.Rect(
                x + (dx - min_x) * cfg.CELL,
                y + (dy - min_y) * cfg.CELL,
                cfg.CELL, cfg.CELL,
            )
            self._draw_block(rect, piece.color)

    def _draw_game_over(self):
        overlay = pygame.Surface((cfg.PLAY_WIDTH, cfg.PLAY_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (cfg.MARGIN, cfg.MARGIN))

        cx = cfg.MARGIN + cfg.PLAY_WIDTH // 2
        cy = cfg.MARGIN + cfg.PLAY_HEIGHT // 2

        title = self.big_font.render("GAME OVER", True, (255, 80, 80))
        self.screen.blit(title, title.get_rect(center=(cx, cy - 30)))

        prompt = self.font.render("Press R to restart", True, cfg.WHITE)
        self.screen.blit(prompt, prompt.get_rect(center=(cx, cy + 20)))
