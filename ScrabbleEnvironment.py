from GameObjects import *


class Scrabble:
    def __init__(self, seed: int, display_gameplay: bool):

        self.seed = seed
        np.random.seed(self.seed)
        self.display_gameplay = display_gameplay

        self.screen_color = (0, 0, 0)  # white in RGB
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

        self.is_running = False

    def _render(self):
        # Painting over previous frame
        self.window_surface.fill(self.screen_color)
        # Rendering grid
        for _row in range(self.rows):
            for _col in range(self.columns):
                pygame.draw.rect(surface=self.window_surface,
                                 color=self.board.grid[_row][_col].color,
                                 rect=self.board.grid[_row][_col].rect,
                                 width=2)
        pygame.display.update()
        self.clock.tick(self.fps)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                #raise SystemExit

    def get_state(self):
        pass

    def run(self):
        self.is_running = True
        while self.is_running:
            self._handle_input()
            self._render()
        pygame.quit()
