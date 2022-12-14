import random
from typing import List, Tuple

import pygame
import numpy as np

from Settings import *


class Cell:
    def __init__(self, width: int,
                 height: int,
                 cell_type: str = "STANDARD",
                 color: Tuple[int, int, int] = (136, 136, 136),  # Grey as standard
                 edge_color: Tuple[int, int, int] = (0, 0, 0)
                 ) -> None:
        self.rect = None

        self.width = width
        self.height = height
        assert width == height, f'Width and height of cell should be equal, but they are: {self.width, self.height}'

        self.color = color
        self.edge_color = edge_color
        self.text_size = 14
        self.type = cell_type
        assert cell_type in CELL_TYPES + ["STANDARD"], f'Type: {self.type} is not known, use any of: {CELL_TYPES}.'

        self.occupied = False
        self.content = None

        self._initialize()

    def _initialize(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def is_occupied(self) -> bool:
        return self.occupied

    def set_type(self, cell_type: str) -> None:
        assert cell_type in CELL_TYPES, f'Type: {self.type} is not known, use any of: {CELL_TYPES}.'
        self.type = cell_type
        self.color = MULTIPLIER_COLORS[self.type]
        if cell_type != "STANDARD":
            self.occupied = True
            self.content = PygameText(text=self.type,
                                      text_size=self.text_size,
                                      text_color=(255, 255, 255),
                                      center_x=self.rect.centerx,
                                      center_y=self.rect.centery)

    def get_type(self) -> str:
        return self.type


class Board:
    def __init__(self, nr_rows: int = 15,
                 nr_cols: int = 15,
                 board_size: Tuple[int, int] = (600, 600)) -> None:

        self.nr_rows = nr_rows
        self.nr_cols = nr_cols
        assert self.nr_rows == self.nr_cols, f'nr_rows and nr_cols should be equal, \
                                               but they are: {self.nr_rows, self.nr_cols}'

        self.board_size = self.board_width, self.board_height = board_size
        assert self.board_width == self.board_height, f'Width and height of screen should be equal, \
                                                          but they are: {self.board_width, self.board_height}'
        self.cell_width = self.cell_height = self.board_width / self.nr_cols

        self.grid = np.empty(shape=(self.nr_rows, self.nr_cols), dtype=object)

        self._initialize()

    def _initialize(self):
        # Setting cells in grid
        for _row in range(0, self.nr_rows):
            for _col in range(0, self.nr_cols):
                _cell = Cell(width=self.cell_width, height=self.cell_height)
                _cell.rect.left = _col * self.cell_width
                _cell.rect.top = _row * self.cell_height
                self.grid[_row][_col] = _cell
        # Setting type of cells in grid
        for _multiplier_type in list(MULTIPLIER_ARRANGEMENT.keys()):
            for _row, _col in MULTIPLIER_ARRANGEMENT[_multiplier_type]:
                self.grid[_row][_col].set_type(_multiplier_type)


class Letters:
    def __init__(self, distribution=None):
        if distribution is None:
            distribution = LETTER_DISTRIBUTION
        self._distribution = distribution
        self.available_letters = []

        self._initialize()

    def _initialize(self):
        for _letter in ALPHABET:
            for _nr_letters in range(self._distribution[_letter]):
                self.available_letters.append(_letter)

    def sample_hand(self, size: int = 7) -> List[int]:
        assert size <= len(self.available_letters), f'Not enough letters remaining, wanted size: {size}, \
                                                     remaining letters: {len(self.available_letters)}.'
        random.shuffle(self.available_letters)
        _hand = self.available_letters[:size]
        self.available_letters = self.available_letters[size:]
        return _hand


class PygameText:
    def __init__(self, text: str,
                 text_size: int,
                 text_color: Tuple[int, int, int],
                 center_x: int,
                 center_y: int) -> None:
        pygame.font.init()

        self.text_size = text_size
        self.text_color = text_color

        self.font = pygame.font.Font("media/Scrabble_font.otf", self.text_size)

        self.text_surface = self.font.render(text, True, self.text_color, None)

        self.text_rect = self.text_surface.get_rect()

        self.text_rect.centerx, self.text_rect.centery = center_x, center_y
