import pygame

from GameObjects import *


class Scrabble:
    def __init__(self, seed: int, display_gameplay: bool):

        self.seed = seed
        np.random.seed(self.seed)
        self.display_gameplay = display_gameplay

        self.screen_color = (255, 255, 255)  # white in RGB
        self.display_gameplay = display_gameplay
        self.screen_size = self.screen_width, self.screen_height = 600, 800
        self.grid_size = self.rows, self.columns = 15, 15
        self.cell_size = self.screen_width / self.rows

        if self.display_gameplay:
            self.clock = pygame.time.Clock()
            self.fps = 60
            self.window_surface = pygame.display.set_mode(size=self.screen_size,
                                                          flags=pygame.DOUBLEBUF)

        self.board = Board(nr_rows=self.rows,
                           nr_cols=self.columns,
                           board_size=(self.screen_width,
                                       self.screen_width))

        self.hand = Hand(hand_size=7,
                         LU_anchor=(0, 600),  # Pixel coordinate for upper left corner
                         background_width=self.screen_width,
                         background_height=200)

        self.is_running = False

    def _render(self):
        # Painting over previous frame
        self.window_surface.fill(self.screen_color)
        # Rendering grid
        for _row in range(self.rows):
            for _col in range(self.columns):
                # Drawing cell fill color
                pygame.draw.rect(surface=self.window_surface,
                                 color=self.board.grid[_row][_col].color,
                                 rect=self.board.grid[_row][_col].rect,
                                 width=0)
                # Drawing cell edge color
                pygame.draw.rect(surface=self.window_surface,
                                 color=self.board.grid[_row][_col].edge_color,
                                 rect=self.board.grid[_row][_col].rect,
                                 width=1)
                # Setting text in cell
                if self.board.grid[_row][_col].is_occupied():
                    self.window_surface.blit(self.board.grid[_row][_col].content.text_surface,
                                             self.board.grid[_row][_col].content.text_rect)
        # Rendering hand
        pygame.draw.rect(surface=self.window_surface,
                         color=self.hand.background_color,
                         rect=self.hand.background_rect)
        for _letter in range(self.hand.hand_size):
            # Drawing cell fill color
            pygame.draw.rect(surface=self.window_surface,
                             color=self.hand.letter_cells[_letter].color,
                             rect=self.hand.letter_cells[_letter].rect,
                             width=0)
            # Drawing cell edge color
            pygame.draw.rect(surface=self.window_surface,
                             color=self.hand.letter_cells[_letter].edge_color,
                             rect=self.hand.letter_cells[_letter].rect,
                             width=2)
            # Setting text in cell
            if self.hand.letter_cells[_letter].is_occupied():
                self.window_surface.blit(self.hand.letter_cells[_letter].content.text_surface,
                                         self.hand.letter_cells[_letter].content.text_rect)
        # Updating screen and forcing specific framerate
        pygame.display.update()
        self.clock.tick(self.fps)

    # For handling user inputs
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def get_state(self):
        pass

    # For running game
    def run(self):
        self.is_running = True
        while self.is_running:
            self._handle_input()
            self._render()
        pygame.quit()
