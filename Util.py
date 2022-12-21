import random
from typing import List, Tuple, Union

import pygame
import numpy as np


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
