from GameObjects import *
from Util import *


class Scrabble:
    def __init__(self, seed: int, display_gameplay: bool):

        self.seed = seed
        np.random.seed(self.seed)
        self.display_gameplay = display_gameplay

        self.screen_color = WHITE  # white in RGB
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
                         UL_anchor=(0, 600),  # Pixel coordinate for upper left corner
                         background_width=self.screen_width,
                         background_height=200)

        self.shuffle_button = PygameButton(UL_anchor=(20, 610),
                                           width=70,
                                           height=40,
                                           text="Shuffle")

        self.submit_button = PygameButton(UL_anchor=(510, 610),
                                          width=70,
                                          height=40,
                                          text="Submit")

        self.is_running = False

    def _render(self):
        # Painting over previous frame
        self.window_surface.fill(self.screen_color)
        # Rendering grid
        for _row in range(self.rows):
            for _col in range(self.columns):
                # Drawing cell fill color and edge color
                draw_rect(surface=self.window_surface,
                          color=self.board.grid[_row][_col].button.get_color(),
                          rect=self.board.grid[_row][_col].button.rect,
                          border=1,
                          border_color=self.board.grid[_row][_col].edge_color)
        # Drawing multiplier text and content text
        draw_text(surface=self.window_surface, cells=self.board.grid)

        # Rendering hand
        pygame.draw.rect(surface=self.window_surface,
                         color=self.hand.background_color,
                         rect=self.hand.background_rect)

        # Drawing cell fill color and edge color
        for _letter in range(self.hand.hand_size):
            draw_rect(surface=self.window_surface,
                      color=self.hand.letter_cells[_letter].button.get_color(),
                      rect=self.hand.letter_cells[_letter].button.rect,
                      border=2,
                      border_color=self.hand.letter_cells[_letter].edge_color)

        # Drawing text in hand cells
        draw_text(surface=self.window_surface, cells=self.hand.letter_cells)

        # Drawing shuffle button
        draw_button(surface=self.window_surface, button=self.shuffle_button)

        # Drawing submit button
        draw_button(surface=self.window_surface, button=self.submit_button)

        # Updating screen and forcing specific framerate
        pygame.display.update()
        self.clock.tick(self.fps)

    # For handling user inputs
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
        
            # Checking if shuffle button is pressed
            # TODO: Check MOUSEBUTTONDOWN smarter while still updating unpressed color
            if self.shuffle_button.check_pressed(event=event):
                self.hand.shuffle_hand()

            # Checking if submit button is pressed
            if self.submit_button.check_pressed(event=event):
                # TODO: Add scoring functionality
                for _cell in range(len(self.hand.letter_cells)):
                    # Only check for pressed board cell if hand cell is pressed
                    if self.hand.letter_cells[_cell].button.is_pressed:
                        for _row in range(self.board.grid.shape[0]):
                            for _col in range(self.board.grid.shape[1]):
                                # Only setting letter if cell in board is marked
                                if self.board.grid[_row][_col].button.is_pressed:
                                    transfer_letter(hand_cell=self.hand.letter_cells[_cell],
                                                    board_cell=self.board.grid[_row][_col])
                                    update_hand_contents(hand=self.hand)

            # For handling buttons attached to board grid
            for _row in range(self.board.grid.shape[0]):
                for _col in range(self.board.grid.shape[1]):
                    if self.board.grid[_row][_col].button.check_pressed(event=event):
                        # First un-press all for having only one grid cell chosen at a time
                        un_press_all(cells=self.board.grid)
                        # Negating current state for handling "un-pressing" logic
                        self.board.grid[_row][_col].button.is_pressed = not self.board.grid[_row][_col].button.is_pressed

            # For handling buttons attached to hand cells
            for _cell in range(len(self.hand.letter_cells)):
                if self.hand.letter_cells[_cell].button.check_pressed(event=event):
                    # First un-press all for having only one hand cell chosen at a time
                    un_press_all(cells=self.hand.letter_cells)
                    self.hand.letter_cells[_cell].button.is_pressed = not self.hand.letter_cells[_cell].button.is_pressed

    def get_state(self):
        pass

    # For running game
    def run(self):
        self.is_running = True
        while self.is_running:
            self._handle_input()
            self._render()
        pygame.quit()


