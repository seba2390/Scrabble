import random
from typing import List, Tuple

import pygame
import numpy as np

from Settings import *

# TODO: Fix problem with button is_pressed() gives multiple responses

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


class PygameButton:
    def __init__(self, LU_anchor: Tuple[int, int],  # Pixel coordinate for upper left corner
                 width: int,
                 height: int,
                 text: str = None,
                 text_size: int = 15,
                 text_color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        self.left, self.top = LU_anchor
        self.width, self.height = width, height

        self._unpressed_color = (120, 120, 120)
        self._pressed_color = (145, 145, 145)
        self.color = self._unpressed_color

        if text is not None:
            self.text_color = text_color
            self.text_size = text_size
            self.text = PygameText(text=text,
                                   text_size=self.text_size,
                                   text_color=self.text_color,
                                   center_x=self.left + self.width // 2,
                                   center_y=self.top + self.height // 2)
        self._initialize()

    def _initialize(self):
        # Setting pygame rectangle
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left, self.rect.top = self.left, self.top

    def is_pressed(self):
        mouse_position = pygame.mouse.get_pos()
        # Within x-range
        if self.rect.left <= mouse_position[0] <= self.rect.right:
            # Within y-range
            if self.rect.top <= mouse_position[1] <= self.rect.bottom:
                self.color = self._pressed_color
                left, middle, right = pygame.mouse.get_pressed()
                # Left mouse-button pressed
                if left:
                    return True

        else:
            self.color = self._unpressed_color
            return False


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

    def set_content(self, content: str | PygameText) -> None:
        self.occupied = True
        self.content = content

    def set_type(self, cell_type: str) -> None:
        assert cell_type in CELL_TYPES, f'Type: {self.type} is not known, use any of: {CELL_TYPES}.'
        self.type = cell_type
        self.color = MULTIPLIER_COLORS[self.type]
        if cell_type != "STANDARD":
            self.set_content(PygameText(text=self.type,
                                        text_size=self.text_size,
                                        text_color=(255, 255, 255),
                                        center_x=self.rect.centerx,
                                        center_y=self.rect.centery))

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

    def sample(self, size: int = 7) -> List[str]:
        assert size <= len(self.available_letters), f'Not enough letters remaining, wanted size: {size}, \
                                                     remaining letters: {len(self.available_letters)}.'
        random.shuffle(self.available_letters)
        _hand = self.available_letters[:size]
        self.available_letters = self.available_letters[size:]
        return _hand


class Hand:
    def __init__(self, hand_size: int = 7,
                 LU_anchor: Tuple[int, int] = (0, 600),  # Placement of left upper (LU) corner on screen.
                 background_width: int = 600,
                 background_height: int = 200) -> None:
        self.background_width = background_width
        self.background_height = background_height
        self.background_left, self.background_top = LU_anchor
        self.background_color = (0, 0, 0)
        self.background_rect = None
        self.top_buffer = 5  # Distance between top of hand background and top of hand cells

        self.cell_size = 50
        self.text_size = 20
        self.text_color = (255, 255, 255)

        self.hand_size = hand_size
        self.available_letters = Letters(distribution=LETTER_DISTRIBUTION)
        self.letter_cells = []
        self.letters = []

        self._initialize()

    def _initialize(self):
        # Setting pygame rectangle
        self.background_rect = pygame.Rect(0, 0, self.background_width, self.background_height)
        self.background_rect.top = self.background_top
        self.background_rect.left = self.background_left
        # Setting first 'Hand size' letters
        self.letters = self.available_letters.sample(size=self.hand_size)
        # Setting hand cells for letters
        self.letter_cells = [Cell(width=self.cell_size,
                                  height=self.cell_size,
                                  edge_color=(255, 255, 255))
                             for _ in range(self.hand_size)]
        # Setting text objects in cells
        start_x = (self.background_width - self.hand_size * self.cell_size) // 2
        for _cell_nr, _cell in enumerate(self.letter_cells):
            _cell.rect.left = start_x + _cell_nr * self.cell_size
            _cell.rect.top = self.background_top + self.top_buffer
            _cell.set_content(PygameText(text=self.letters[_cell_nr],
                                         text_size=self.text_size,
                                         text_color=self.text_color,
                                         center_x=_cell.rect.centerx,
                                         center_y=_cell.rect.centery))

    def shuffle_hand(self):
        # Shuffling letters
        assert len(self.letters) > 0, "No letters on hand."
        random.shuffle(self.letters)
        for _cell_nr, _cell in enumerate(self.letter_cells):
            _cell.set_content(PygameText(text=self.letters[_cell_nr],
                                         text_size=self.text_size,
                                         text_color=self.text_color,
                                         center_x=_cell.rect.centerx,
                                         center_y=_cell.rect.centery))
