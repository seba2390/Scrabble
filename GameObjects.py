import random
from typing import List, Tuple, Union

import pygame
import numpy as np

from Settings import *
from Structures import *


# TODO: Find a way to make set_pressed(coordinate) method shared for 'Hand' and 'Board' class instead of writing 2 times.

class PygameText:
    def __init__(self, text: str,
                 text_size: int,
                 text_color: Tuple[int, int, int],
                 center_x: int,
                 center_y: int) -> None:
        pygame.font.init()

        self.text = text
        self.text_size = text_size
        self.text_color = text_color

        self.font = pygame.font.Font("media/Scrabble_font.otf", self.text_size)

        self.text_surface = self.font.render(self.text, True, self.text_color)

        self.text_rect = self.text_surface.get_rect()

        self.text_rect.centerx, self.text_rect.centery = center_x, center_y


class PygameButton:
    def __init__(self, UL_anchor: Tuple[int, int],  # Pixel coordinate for upper left corner
                 width: int,
                 height: int,
                 color: Tuple[int, int, int] = GREY,
                 text: str = None,
                 text_size: int = 15,
                 text_color: Tuple[int, int, int] = WHITE) -> None:
        self.left, self.top = UL_anchor
        self.width, self.height = width, height

        self.color = color
        self.un_highlighted_color = self.color
        self.highlighted_color = (self.un_highlighted_color[0] + 25,
                                  self.un_highlighted_color[1] + 25,
                                  self.un_highlighted_color[2] + 25)

        self.pressed_color = (self.un_highlighted_color[0] + 45,
                              self.un_highlighted_color[1] + 45,
                              self.un_highlighted_color[2] + 45)

        self.is_pressed = False

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

    def get_color(self):
        if self.is_pressed:
            return self.pressed_color
        else:
            return self.color

    def set_color(self, color: Tuple[int, int, int]) -> None:
        self.color = color
        self.un_highlighted_color = self.color
        self.highlighted_color = (self.un_highlighted_color[0] + 25,
                                  self.un_highlighted_color[1] + 25,
                                  self.un_highlighted_color[2] + 25)

        self.pressed_color = (self.un_highlighted_color[0] + 45,
                              self.un_highlighted_color[1] + 45,
                              self.un_highlighted_color[2] + 45)

    def check_pressed(self, event):
        if self.is_highlighted():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False

    def is_highlighted(self) -> bool:
        mouse_position = pygame.mouse.get_pos()
        # Within x-range
        if self.rect.left <= mouse_position[0] <= self.rect.right:
            # Within y-range
            if self.rect.top <= mouse_position[1] <= self.rect.bottom:
                self.color = self.highlighted_color
                return True
            else:
                self.color = self.un_highlighted_color
                return False
        else:
            self.color = self.un_highlighted_color
            return False


class Cell:
    def __init__(self, width: int,
                 height: int,
                 cell_type: str = "STANDARD",
                 color: Tuple[int, int, int] = (136, 136, 136),  # Grey as standard
                 edge_color: Tuple[int, int, int] = BLACK,
                 with_button: bool = False,
                 ) -> None:

        self.width = width
        self.height = height
        assert width == height, f'Width and height of cell should be equal, but they are: {self.width, self.height}'

        self.color = color
        self.edge_color = edge_color
        self.text_size = 14
        self.type = cell_type
        assert cell_type in CELL_TYPES + ["STANDARD"], f'Type: {self.type} is not known, use any of: {CELL_TYPES}.'

        self.has_multiplier = False
        self.multiplier = None

        self.has_score = False
        self.score = None

        self.occupied = False
        self.content = None

        self.button = None
        if with_button:  # Bool for checking if cell has button attached to it
            self.button = PygameButton(UL_anchor=(0, 0),  # initializing to random spot
                                       width=self.width,
                                       height=self.height)

    def is_occupied(self) -> bool:
        return self.occupied

    def is_score(self) -> bool:
        return self.has_score

    def is_multiplier(self) -> bool:
        return self.has_multiplier

    def set_content(self, content: Union[str, PygameText]) -> None:
        self.occupied = True
        self.content = content

    def set_score(self, score: Union[str, PygameText]) -> None:
        self.has_score = True
        self.score = score

    def set_multiplier(self, multiplier: Union[str, PygameText]) -> None:
        self.has_multiplier = True
        self.multiplier = multiplier

    def remove_content(self) -> None:
        self.content = None
        self.button.is_pressed = False
        if self.is_occupied():
            self.occupied = False

    def remove_score(self) -> None:
        self.score = None
        if self.is_score():
            self.has_score = False

    def remove_multiplier(self) -> None:
        self.multiplier = None
        if self.is_multiplier():
            self.has_multiplier = False

    def set_type(self, cell_type: str) -> None:
        assert cell_type in CELL_TYPES, f'Type: {self.type} is not known, use any of: {CELL_TYPES}.'
        self.type = cell_type
        self.color = MULTIPLIER_COLORS[self.type]
        if cell_type != "STANDARD":
            self.set_multiplier(multiplier=PygameText(text=self.type,
                                                      text_size=self.text_size,
                                                      text_color=WHITE,
                                                      center_x=self.button.rect.centerx,
                                                      center_y=self.button.rect.centery))

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

        self.has_pressed = False  # Bool for checking if any button on board is pressed
        self.pressed_coord = None  # Tuple of index coordinates of pressed button

        self._initialize()

    def _initialize(self):
        # Setting cells in grid
        for _row in range(0, self.nr_rows):
            for _col in range(0, self.nr_cols):
                _cell = Cell(width=self.cell_width, height=self.cell_height, with_button=True)
                # Setting button on top of cell
                _cell.button.rect.left = _col * self.cell_width
                _cell.button.rect.top = _row * self.cell_height
                self.grid[_row][_col] = _cell  # Setting cell

        # Setting type of cells in grid
        for _multiplier_type in list(MULTIPLIER_ARRANGEMENT.keys()):
            for _row, _col in MULTIPLIER_ARRANGEMENT[_multiplier_type]:
                self.grid[_row][_col].set_type(_multiplier_type)
                # Updating button color according to cell type
                self.grid[_row][_col].button.color = self.grid[_row][_col].color
                self.grid[_row][_col].button.un_highlighted_color = self.grid[_row][_col].color

    def get_board_state(self) -> np.ndarray:
        _EMPTY_TOKEN = "NaN"
        # Entries of (content, cell type)
        _board_array = np.empty(shape=(self.nr_rows, self.nr_cols), dtype=object)
        # Getting cells in grid
        for _row in range(0, self.nr_rows):
            for _col in range(0, self.nr_cols):
                _type = self.grid[_row, _col].get_type()
                _content = self.grid[_row, _col].content.text if self.grid[_row, _col].is_occupied() else _EMPTY_TOKEN
                _board_array[_row, _col] = (_content, _type)
        return _board_array

    # TODO: fix order w. respect to most commonly occurring
    def set_pressed(self, coordinate: Tuple[int, int]) -> None:
        # Same button clicked
        if self.has_pressed and self.pressed_coord == coordinate:
            self.grid[coordinate[0], coordinate[1]].button.is_pressed = False
            self.has_pressed = False
        # New button pressed while one already pressed
        elif self.has_pressed and self.pressed_coord != coordinate:
            # Un-pressing old one
            self.grid[self.pressed_coord[0], self.pressed_coord[1]].button.is_pressed = False
            self.pressed_coord = coordinate
            # Pressing new one
            self.grid[self.pressed_coord[0], self.pressed_coord[1]].button.is_pressed = True
            self.has_pressed = True
        # New button pressed with no one already pressed
        elif not self.has_pressed:
            self.pressed_coord = coordinate
            self.grid[self.pressed_coord[0], self.pressed_coord[1]].button.is_pressed = True
            self.has_pressed = True


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
                 UL_anchor: Tuple[int, int] = (0, 600),  # Placement of upper left (UL) corner on screen.
                 background_width: int = 600,
                 background_height: int = 200) -> None:
        self.background_width = background_width
        self.background_height = background_height
        self.background_left, self.background_top = UL_anchor
        self.background_color = (0, 0, 0)
        self.background_rect = None
        self.top_buffer = 5  # Distance between top of hand background and top of hand cells

        self.cell_size = 50
        self.text_size = 20
        self.text_color = (255, 255, 255)

        self.hand_size = hand_size
        self.available_letters = Letters(distribution=LETTER_DISTRIBUTION)
        self.letter_cells = np.empty(shape=(7,), dtype=object)
        self.letters = []

        self.has_pressed = False  # Bool for checking if any button on board is pressed
        self.pressed_coord = None  # Index coordinate for pressed button

        self._initialize()

    def _initialize(self):
        # Setting pygame rectangle
        self.background_rect = pygame.Rect(0, 0, self.background_width, self.background_height)
        self.background_rect.top = self.background_top
        self.background_rect.left = self.background_left
        # Setting first 'Hand size' letters
        self.letters = self.available_letters.sample(size=self.hand_size)
        # Setting hand cells for letters
        for _cell in range(len(self.letter_cells)):
            self.letter_cells[_cell] = Cell(width=self.cell_size,
                                            height=self.cell_size,
                                            edge_color=WHITE,
                                            with_button=True)
        # Setting text objects in cells
        start_x = (self.background_width - self.hand_size * self.cell_size) // 2
        for _cell_nr, _cell in enumerate(self.letter_cells):
            # Setting letter
            _cell.button.rect.left = start_x + _cell_nr * self.cell_size
            _cell.button.rect.top = self.background_top + self.top_buffer
            _cell.set_content(PygameText(text=self.letters[_cell_nr],
                                         text_size=self.text_size,
                                         text_color=self.text_color,
                                         center_x=_cell.button.rect.centerx,
                                         center_y=_cell.button.rect.centery))
            # Setting score val in lower right corner
            _cell.set_score(PygameText(text=str(POINT_DISTRIBUTION[self.letters[_cell_nr]]),
                                       text_size=12,
                                       text_color=self.text_color,
                                       center_x=_cell.button.rect.right - 9,
                                       center_y=_cell.button.rect.bottom - 9))

    def shuffle_hand(self):
        # Shuffling letters
        assert len(self.letters) > 0, "No letters on hand."
        random.shuffle(self.letters)
        _letter_counter = 0
        for _cell_nr, _cell in enumerate(self.letter_cells):
            if _cell.content is not None:
                _cell.set_content(PygameText(text=self.letters[_letter_counter],
                                             text_size=self.text_size,
                                             text_color=self.text_color,
                                             center_x=_cell.button.rect.centerx,
                                             center_y=_cell.button.rect.centery))
                # Setting score val in lower right corner
                _cell.set_score(PygameText(text=str(POINT_DISTRIBUTION[self.letters[_cell_nr]]),
                                           text_size=12,
                                           text_color=self.text_color,
                                           center_x=_cell.button.rect.right - 9,
                                           center_y=_cell.button.rect.bottom - 9))
                _letter_counter += 1

    def refill_hand(self):
        letters_on_hand = sum([1 for _cell in self.letter_cells if _cell.is_occupied()])
        assert letters_on_hand < self.hand_size, f'Hand is already full.'

        # Sampling new letters
        new_letters = self.available_letters.sample(size=self.hand_size - letters_on_hand)

        # Filling hand
        for _cell_nr, _cell in enumerate(self.letter_cells):
            if not _cell.is_occupied():
                # Setting letter
                _letter = new_letters.pop(-1)
                _cell.set_content(PygameText(text=_letter,
                                             text_size=self.text_size,
                                             text_color=self.text_color,
                                             center_x=_cell.button.rect.centerx,
                                             center_y=_cell.button.rect.centery))
                # Setting score val in lower right corner
                _cell.set_score(PygameText(text=str(POINT_DISTRIBUTION[_letter]),
                                           text_size=12,
                                           text_color=self.text_color,
                                           center_x=_cell.button.rect.right - 9,
                                           center_y=_cell.button.rect.bottom - 9))

    def set_pressed(self, coordinate: int) -> None:
        # Same button clicked
        if self.has_pressed and self.pressed_coord == coordinate:
            self.letter_cells[coordinate].button.is_pressed = False
            self.has_pressed = False
        # New button pressed while one already pressed
        elif self.has_pressed and self.pressed_coord != coordinate:
            # Un-pressing old one
            self.letter_cells[self.pressed_coord].button.is_pressed = False
            self.pressed_coord = coordinate
            # Pressing new one
            self.letter_cells[self.pressed_coord].button.is_pressed = True
            self.has_pressed = True
        # New button pressed with no one already pressed
        elif not self.has_pressed:
            self.pressed_coord = coordinate
            self.letter_cells[self.pressed_coord].button.is_pressed = True
            self.has_pressed = True


class Play:
    """ Class for handling a play in a round."""

    def __init__(self):
        self.score = 0
        self.board_coordinates = []  # Index coordinates of played cells on board

    def add_played_cell(self, letter_score: int, board_coordinate: Tuple[int, int]) -> None:
        assert len(self.board_coordinates) <= 6, 'Should only be able to play a maximum of 7 letters in a round.'
        self.score += letter_score
        self.board_coordinates.append(board_coordinate)

    def get_board_coordinates(self) -> np.ndarray:
        return np.array(self.board_coordinates)

    # TODO: Account for multiplier score 
    def get_score(self):
        return self.score

    def clear_play(self):
        self.board_coordinates = []
        self.score = 0

    def return_letters(self, board: Board, hand: Hand):
        """ Returning played letters from board to hand. """

        cells = [board.grid[coord[0], coord[1]] for coord in self.board_coordinates]

        # Setting in hand
        for _cell in range(len(hand.letter_cells)):
            if not hand.letter_cells[_cell].is_occupied():
                cell = cells.pop(-1)
                pygame_letter = PygameText(text=cell.content.text,
                                           text_size=hand.text_size,
                                           text_color=hand.text_color,
                                           center_x=hand.letter_cells[_cell].button.rect.centerx,
                                           center_y=hand.letter_cells[_cell].button.rect.centery)
                pygame_score = PygameText(text=cell.score.text,
                                          text_size=12,
                                          text_color=hand.text_color,
                                          center_x=hand.letter_cells[_cell].button.rect.right - 9,
                                          center_y=hand.letter_cells[_cell].button.rect.bottom - 9)
                hand.letter_cells[_cell].set_content(content=pygame_letter)
                hand.letter_cells[_cell].set_score(score=pygame_score)

        # Removing from board
        for _ in range(len(self.board_coordinates)):
            _row, _col = self.board_coordinates[_]
            board.grid[_row, _col].remove_content()
            board.grid[_row, _col].remove_score()
            # Re-inserting multiplier type text
            for _multiplier_type, _coordinates in MULTIPLIER_ARRANGEMENT.items():
                if (_row, _col) in _coordinates:
                    board.grid[_row][_col].set_type(_multiplier_type)
                    # Updating button color according to cell type
                    board.grid[_row][_col].button.color = board.grid[_row][_col].color
                    board.grid[_row][_col].button.un_highlighted_color = board.grid[_row][_col].color

        self.clear_play()

    @staticmethod
    def same_row(_coordinates: List[Tuple[int, int]]) -> bool:
        _initial = _coordinates[0]
        # Checking that they are in same row
        for _count, _coord in enumerate(_coordinates):
            if _coord[0] != _initial[0]:
                return False
        return True

    @staticmethod
    def same_column(_coordinates: List[Tuple[int, int]]) -> bool:
        _initial = _coordinates[0]
        # Checking that they are in same col
        for _count, _coord in enumerate(_coordinates):
            if _coord[1] != _initial[1]:
                return False
        return True

    @staticmethod
    def horizontally_adjacent(_coordinates: List[Tuple[int, int]]) -> bool:
        _initial = _coordinates[0]
        for _count, _coord in enumerate(_coordinates):
            if _coord[1] != _initial[1] + _count:
                return False
        return True

    @staticmethod
    def vertically_adjacent(_coordinates: List[Tuple[int, int]]) -> bool:
        _initial = _coordinates[0]
        for _count, _coord in enumerate(_coordinates):
            if _coord[0] != _initial[0] + _count:
                return False
        return True

    @staticmethod
    def get_words(line: np.ndarray) -> List[str]:
        sequences = []
        current_sequence = ""
        for cell in line:
            if cell.content is not None:
                current_sequence += cell.content.text
            elif len(current_sequence) >= 2:
                sequences.append(current_sequence)
                current_sequence = ""
            else:
                current_sequence = ""
        if len(current_sequence) >= 2:
            sequences.append(current_sequence)
        return sequences

    def get_word(self, _board: Board, coordinates: List[Tuple[int, int]]) -> str:
        if self.same_row(_coordinates=coordinates):
            sorted_rows = [coord[0] for coord in coordinates]
            sorted_coordinates = np.array(coordinates)[np.argsort(sorted_rows)].tolist()
        else:
            sorted_cols = [coord[1] for coord in coordinates]
            sorted_coordinates = np.array(coordinates)[np.argsort(sorted_cols)].tolist()
        _word = ""
        for _coord in sorted_coordinates:
            _row, _col = _coord
            _word += _board.grid[_row, _col].content.text
        return _word

    def submit(self, round: int, board: Board, dictionary: Trie) -> bool:
        # First word placed doesn't have to be adjacent to other letters
        if round == 1:
            if self.same_row(_coordinates=self.board_coordinates) or self.same_column(_coordinates=self.board_coordinates):
                if self.horizontally_adjacent(_coordinates=self.board_coordinates) or self.vertically_adjacent(_coordinates=self.board_coordinates):
                    _placed_word = self.get_word(_board=board, coordinates=self.board_coordinates)
                    print("playing word:", _placed_word)
                    if dictionary.holds(word=_placed_word):
                        print("GREAT SUCCESS - WORD EXISTS IN DICTIONARY")
                        self.clear_play()
                        return True
                    else:
                        print("NOT SO GREAT SUCCESS - WORD DOESNT EXIST IN DICTIONARY")
                        return False
            else:
                print("INVALID ARRANGEMENT OF LETTERS...")
                return False
        # All words except first one has to be adjacent to other letters
        else:
            _words = []
            if self.same_row(_coordinates=self.board_coordinates) or self.same_column(_coordinates=self.board_coordinates):
                for _row in range(board.grid.shape[0]):
                    _current_words = self.get_words(line=board.grid[_row])
                    for _word in _current_words:
                        _words.append(_word)
                for _col in range(board.grid.shape[1]):
                    _current_words = self.get_words(line=board.grid[:,_col])
                    for _word in _current_words:
                        _words.append(_word)
                for _word in _words:
                    if not dictionary.holds(word=_word):
                        return False
                print("Made legal play and found words:", _words)
                self.clear_play()
                return True
            else:
                print("INVALID ARRANGEMENT OF LETTERS...")
                return False
