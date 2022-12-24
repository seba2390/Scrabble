from typing import List, Tuple, Union

import pygame
import numpy as np

from GameObjects import *


def draw_rect(surface: pygame.Surface, color: Tuple[int, int, int], rect: pygame.Rect, border: int = None,
              border_color: Tuple[int, int, int] = (255, 255, 255)) -> None:
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


def un_press_all(cells: np.ndarray):
    # If passing board, it is 2D array
    if len(cells.shape) == 2:
        for row in range(cells.shape[0]):
            for col in range(cells.shape[1]):
                cells[row, col].button.is_pressed = False
    # If passing hand, it is 1D array
    else:
        for cell in cells:
            cell.button.is_pressed = False


def transfer_letter(hand_cell: Cell, board_cell: Cell) -> None:
    """ Wrapper function for setting pygame text object in board cell. """
    if hand_cell.is_occupied() and not board_cell.is_occupied():
        pygame_letter = PygameText(text=hand_cell.content.text,
                                   text_size=board_cell.text_size,
                                   text_color=(255, 255, 255),
                                   center_x=board_cell.button.rect.centerx,
                                   center_y=board_cell.button.rect.centery)
        board_cell.set_content(content=pygame_letter)
        hand_cell.remove_content()


def update_hand_contents(hand: Hand) -> None:
    """ Helper function for updating the letters attr. in hand
        when letter is set on board."""
    updated_letters = [lc.content.text for lc in hand.letter_cells if lc.content is not None]
    hand.letters = updated_letters
    #for letter_cell in hand.letter_cells:
    #    if letter_cell.content is not None:
    #        letter = letter_cell.content.text
    #[lc.content.text for lc in hand.letter_cells if lc.content is not None]
