import pygame
import numpy as np

MULTIPLIER_TYPES = ["DLS",  # Double letter score
                    "TLS",  # Triple letter score
                    "DWS",  # Double word score
                    "TWS"]  # Triple word score

CELL_TYPES = MULTIPLIER_TYPES + ["STANDARD"]


class Cell:
    def __init__(self, width: int,
                 height: int,
                 cell_type: str = "STANDARD",
                 color: tuple[int, int, int] = (136, 136, 136)  # Grey as standard
                 ) -> None:
        self.rect = None

        self.width = width
        self.height = height
        assert width == height, f'Width and height of cell should be equal, but they are: {self.width, self.height}'

        self.color = color
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
                 board_size: tuple[int, int] = (600,600)) -> None:

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
                _cell.rect.top  = _row * self.cell_height
                self.grid[_row][_col] = _cell






