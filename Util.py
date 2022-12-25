import os
from itertools import combinations, permutations

import pygame

from GameObjects import *


def draw_rect(surface: pygame.Surface, color: Tuple[int, int, int], rect: pygame.Rect, border: int = None,
              border_color: Tuple[int, int, int] = WHITE) -> None:
    # Drawing rect fill
    pygame.draw.rect(surface=surface,
                     color=color,
                     rect=rect,
                     width=0)
    # Drawing rect border
    if border is not None:
        pygame.draw.rect(surface=surface,
                         color=border_color,
                         rect=rect,
                         width=border)


def draw_text(surface: pygame.Surface, cells: np.ndarray) -> None:
    # 2D array of cells (board)
    if len(cells.shape) == 2:
        for _row in range(cells.shape[0]):
            for _col in range(cells.shape[1]):
                # Rendering multiplier text in cell
                if cells[_row][_col].is_multiplier():
                    surface.blit(cells[_row][_col].multiplier.text_surface,
                                 cells[_row][_col].multiplier.text_rect)
                # Rendering letters in occupied cells
                if cells[_row][_col].is_occupied():
                    surface.blit(cells[_row][_col].content.text_surface,
                                 cells[_row][_col].content.text_rect)
                # Setting score val:
                if cells[_row][_col].is_score():
                    surface.blit(cells[_row][_col].score.text_surface,
                                 cells[_row][_col].score.text_rect)
    # 1D array of cells (hand)
    else:
        for _cell in range(len(cells)):
            # Setting text in cell
            if cells[_cell].is_occupied():
                surface.blit(cells[_cell].content.text_surface,
                             cells[_cell].content.text_rect)
            # Setting score val:
            if cells[_cell].is_score():
                surface.blit(cells[_cell].score.text_surface,
                             cells[_cell].score.text_rect)


def draw_button(surface: pygame.Surface, button: Union[PygameButton, LabeledTile]) -> None:
    # Button rectangle
    pygame.draw.rect(surface=surface,
                     color=button.get_color(),
                     rect=button.rect)
    # Text on button
    surface.blit(button.text.text_surface, button.text.text_rect)


def draw_tile(surface: pygame.Surface, tile: LabeledTile) -> None:
    draw_button(surface=surface, button=tile)


def transfer_letter(hand_cell: Cell, board_cell: Cell) -> None:
    """ Wrapper function for setting pygame text object in board cell. """
    if hand_cell.is_occupied() and not board_cell.is_occupied():
        pygame_letter = PygameText(text=hand_cell.content.text,
                                   text_size=board_cell.text_size,
                                   text_color=WHITE,
                                   center_x=board_cell.button.rect.centerx,
                                   center_y=board_cell.button.rect.centery)
        pygame_score = PygameText(text=hand_cell.score.text,
                                  text_size=board_cell.text_size // 2 + 1,
                                  text_color=WHITE,
                                  center_x=board_cell.button.rect.right - 6,
                                  center_y=board_cell.button.rect.bottom - 6)
        board_cell.set_content(content=pygame_letter)
        board_cell.set_score(score=pygame_score)
        hand_cell.remove_content()
        hand_cell.remove_score()
        if board_cell.is_multiplier():
            board_cell.remove_multiplier()


def update_hand_contents(hand: Hand) -> None:
    """ Helper function for updating the letters attr. in hand
        when letter is set on board."""

    # Updating letters on hand
    updated_letters = [lc.content.text for lc in hand.letter_cells if lc.content is not None]
    hand.letters = updated_letters
    # Changing color of empty hand cells
    for _cell in range(len(hand.letter_cells)):
        if not hand.letter_cells[_cell].is_occupied():
            hand.letter_cells[_cell].button.set_color(color=BLACK)
        else:
            hand.letter_cells[_cell].button.set_color(color=GREY)


def get_wordlist():
    CURRENT_DIR = os.getcwd()
    WORDLIST_DIR = CURRENT_DIR + "/Algorithm/word lists/"
    WORDLIST = os.listdir(WORDLIST_DIR)[0]
    _word_list = np.loadtxt(fname=WORDLIST_DIR + WORDLIST, dtype=str, skiprows=2).tolist()
    return _word_list


def words_in_dictionary(_string: str, dictionary: Trie) -> List[Tuple[str, int]]:
    """ Takes all possible subsets of string of size at least 2,
        finds all permutation of each of these, searches the dictionary
        and returns a list containing (word, word_score). """

    def word_score(_word: str) -> int:
        return sum([POINT_DISTRIBUTION[letter] for letter in _word])

    # Getting alle possible k-sized (at least k=2) permutations of string.
    all_unique_perms = []
    for _word_length in range(2, len(_string) + 1):
        combs = list(combinations(_string, r=_word_length))
        unique_perms = []
        for comb in combs:
            if comb not in unique_perms:
                unique_perms += ["".join(t) for t in list(permutations("".join(comb)))]
        all_unique_perms += unique_perms

    # Getting the words that are in dictionary
    return [(_str, word_score(_str)) for _str in all_unique_perms if dictionary.holds(word=_str)]
