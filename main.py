"""Entry point. Run with:  python main.py"""

import sys

import pygame

import config as cfg
from game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    game = Game(screen)

    running = True
    while running:
        dt = clock.tick(cfg.FPS)  # milliseconds since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    game.handle_key(event.key)

        game.update(dt)
        game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
