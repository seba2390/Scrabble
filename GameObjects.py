import pygame
import numpy as np
import random

MULTIPLIER_TYPES = ["DLS",  # Double letter score
                    "TLS",  # Triple letter score
                    "DWS",  # Double word score
                    "TWS"]  # Triple word score

CELL_TYPES = MULTIPLIER_TYPES + ["STANDARD"]

ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
            "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
            "W", "X", "Y", "Z"]

# Using https://en.wikipedia.org/wiki/Scrabble_letter_distributions
LETTER_DISTRIBUTION = {
                       "E": 12, "A": 9, "I": 9, "O": 8, "N": 6, "R": 6, "T": 6, "L": 4, "S": 4, "U": 4,  # 1 point
                       "D": 4, "G": 3,                                                                   # 2 points
                       "B": 2, "C": 2, "M": 2, "P": 2,                                                   # 3 points
                       "F": 2, "H": 2, "V": 2, "W": 2, "Y": 2,                                           # 4 points
                       "K": 1,                                                                           # 5 points
                       "J": 1, "X": 1,                                                                   # 8 points
                       "Q": 1, "Z": 1,                                                                   # 10 points
                       }


class Cell:
    def __init__(self, width: int,
                 height: int,
                 cell_type: str = "STANDARD",
                 color: tuple[int, int, int] = (136, 136, 136),  # Grey as standard
                 edge_color: tuple[int, int, int] = (0, 0, 0)
                 ) -> None:
        self.rect = None

        self.width = width
        self.height = height
        assert width == height, f'Width and height of cell should be equal, but they are: {self.width, self.height}'

        self.color = color
        self.edge_color = edge_color
        self.type = cell_type
        assert cell_type in CELL_TYPES + ["STANDARD"], f'Type: {self.type} is not known, use any of: {CELL_TYPES}.'

        self.occupied = False
        self.content = None

        self._initialize()

    def _initialize(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def is_occupied(self) -> bool:
        return self.occupied

    def set_content(self, letter: str) -> None:
        self.content = letter

    def set_type(self, cell_type: str) -> None:
        assert cell_type in CELL_TYPES, f'Type: {self.type} is not known, use any of: {CELL_TYPES}.'
        self.type = cell_type

    def get_type(self) -> str:
        return self.type


class Board:
    def __init__(self, nr_rows: int = 15,
                 nr_cols: int = 15,
                 board_size: tuple[int, int] = (600, 600)) -> None:

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
        for _row in range(0, self.nr_rows):
            for _col in range(0, self.nr_cols):
                _cell = Cell(width=self.cell_width, height=self.cell_height)
                _cell.rect.left = _col * self.cell_width
                _cell.rect.top = _row * self.cell_height
                self.grid[_row][_col] = _cell


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
        random.shuffle(self.available_letters)

    def sample_hand(self, size: int = 7) -> list[int, ...]:
        assert size <= len(self.available_letters), f'Not enough letters remaining, wanted size: {size}, \
                                                     remaining letters: {len(self.available_letters)}.'
        random.shuffle(self.available_letters)
        _hand = self.available_letters[:size]
        self.available_letters = self.available_letters[size:]
        return _hand

