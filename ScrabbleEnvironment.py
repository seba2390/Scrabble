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

        self.play = Play()

        self.shuffle_button = PygameButton(UL_anchor=(20, 610),
                                           width=70,
                                           height=40,
                                           text="Shuffle")

        self.clear_button = PygameButton(UL_anchor=(20, 610 + self.shuffle_button.height + 5),
                                         width=70,
                                         height=40,
                                         text="Clear")

        self.submit_button = PygameButton(UL_anchor=(510, 610),
                                          width=70,
                                          height=40,
                                          text="Submit")

        self.pass_button = PygameButton(UL_anchor=(510, 610 + self.submit_button.height + 5),
                                        width=70,
                                        height=40,
                                        text="Pass")

        tile_width = 90
        self.player_one_tile = LabeledTile(UL_anchor=(self.screen_width // 2 - tile_width - 2,
                                                      self.shuffle_button.rect.bottom + 13),
                                           width=tile_width,
                                           height=30,
                                           text="Player 1")
        self.player_one_tile.set_highlighted()

        self.player_two_tile = LabeledTile(UL_anchor=(self.screen_width // 2 + 2,
                                                      self.shuffle_button.rect.bottom + 13),
                                           width=tile_width,
                                           height=30,
                                           text="Player 2")

        self.UK_dictionary = Trie()
        self.UK_dictionary.add_strings(strings=get_wordlist())

        self.is_running = False
        self.round = 0

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

        # Drawing clear button
        draw_button(surface=self.window_surface, button=self.clear_button)

        # Drawing submit button
        draw_button(surface=self.window_surface, button=self.submit_button)

        # Drawing pass button
        draw_button(surface=self.window_surface, button=self.pass_button)

        # Draw Player tiles
        draw_tile(surface=self.window_surface, tile=self.player_one_tile)
        draw_tile(surface=self.window_surface, tile=self.player_two_tile)

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

            # Checking if clear button is pressed
            if self.clear_button.check_pressed(event=event):
                # Returning letters from board to hand
                self.play.return_letters(board=self.board,
                                         hand=self.hand)
                update_hand_contents(hand=self.hand)

            # Checking if submit button is pressed
            if self.submit_button.check_pressed(event=event):
                # Checking that word exists in dictionary
                if self.play.submit(round=self.round, board=self.board, dictionary=self.UK_dictionary):
                    self.hand.refill_hand()
                    self.round += 1
                else:
                    self.play.return_letters(board=self.board,
                                             hand=self.hand)
                update_hand_contents(hand=self.hand)

            # For handling buttons attached to board grid
            for _row in range(self.board.grid.shape[0]):
                for _col in range(self.board.grid.shape[1]):
                    if self.board.grid[_row][_col].button.check_pressed(event=event):
                        # Always setting pressed and un-pressing others
                        self.board.set_pressed(coordinate=(_row, _col))
                        # If hand cell was already marked -> move letter from hand to board
                        if self.hand.has_pressed:
                            self.play.add_played_cell(
                                letter_score=int(self.hand.letter_cells[self.hand.pressed_coord].score.text),
                                board_coordinate=(_row, _col))
                            transfer_letter(hand_cell=self.hand.letter_cells[self.hand.pressed_coord],
                                            board_cell=self.board.grid[_row][_col])
                            update_hand_contents(hand=self.hand)
                            self.hand.has_pressed = False

            # For handling buttons attached to hand cells
            for _cell in range(len(self.hand.letter_cells)):
                if self.hand.letter_cells[_cell].is_occupied():
                    if self.hand.letter_cells[_cell].button.check_pressed(event=event):
                        # Always setting pressed and un-pressing others
                        self.hand.set_pressed(coordinate=_cell)
        if self.round % 2 == 0:
            self.player_one_tile.set_highlighted()
            self.player_two_tile.highlighted = False
        else:
            self.player_two_tile.set_highlighted()
            self.player_one_tile.highlighted = False

    def get_state(self):
        pass

    # For running game
    def run(self):
        self.is_running = True
        while self.is_running:
            self._handle_input()
            self._render()
        pygame.quit()
