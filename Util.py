from typing import List, Tuple, Union

import pygame
import numpy as np

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


def draw_button(surface: pygame.Surface, button: PygameButton) -> None:
    # Button rectangle
    pygame.draw.rect(surface=surface,
                     color=button.get_color(),
                     rect=button.rect)
    # Text on button
    surface.blit(button.text.text_surface, button.text.text_rect)


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
