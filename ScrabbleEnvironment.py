import pygame
import numpy as np


class Scrabble:
    def __init__(self, seed: int, display_gameplay: bool):

        self.seed = seed
        np.random.seed(self.seed)

        self.display_gameplay = display_gameplay
        self.screen_size = self.screen_width, self.screen_height = 800, 800

        self.clock = pygame.time.Clock()
        self.fps = 100
        self.window_surface = pygame.display.set_mode(size=self.screen_size,
                                                      flags=pygame.DOUBLEBUF)

        self.is_running = False

    def render(self):
        pass

    def get_state(self):
        pass

    def run(self):
        pass
