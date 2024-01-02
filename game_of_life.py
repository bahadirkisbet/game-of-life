import time
import pygame
from enum import Enum

class PatternType(Enum):
    GLIDER = 1
    BLINKER = 2
    TOAD = 3
    BEACON = 4
    LWSS = 5
    MWSS = 6
    HWSS = 7
    PULSAR = 8
    PENTADECATHLON = 9
    GOSPER_GLIDER_GUN = 10
    SIMKIN_GLIDER_GUN = 11
    GARDEN_OF_EDEN = 12
    R_PENTOMINO = 13
    DIEHARD = 14
    ACORN = 15
    INFINITE_GROWTH = 16
    

class GameOfLife:
    WIDTH: int = 1000
    HEIGHT: int = 1000
    PATTERNS: dict = {
        PatternType.GLIDER: [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
        PatternType.BLINKER: [(0, 0), (1, 0), (2, 0)],
        PatternType.TOAD: [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)],
        PatternType.BEACON: [(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)],
        PatternType.LWSS: [(0, 0), (3, 0), (4, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3)],
        PatternType.MWSS: [(0, 0), (4, 0), (5, 1), (0, 2), (5, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3)],
        PatternType.HWSS: [(0, 0), (5, 0), (6, 1), (0, 2), (6, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3)],
        PatternType.PULSAR: [(2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0), (0, 2), (5, 2), (7, 2), (12, 2), (0, 3), (5, 3), (7, 3), (12, 3), (0, 4), (5, 4), (7, 4), (12, 4), (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5), (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7), (0, 8), (5, 8), (7, 8), (12, 8), (0, 9), (5, 9), (7, 9), (12, 9), (0, 10), (5, 10), (7, 10), (12, 10), (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12)],
        PatternType.PENTADECATHLON: [(1, 0), (2, 0), (3, 0), (1, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (3, 3), (1, 4), (2, 4), (3, 4), (1, 5), (3, 5), (1, 6), (2, 6), (3, 6), (1, 7), (3, 7), (1, 8), (2, 8), (3, 8)],
        PatternType.GOSPER_GLIDER_GUN: [(0, 4), (0, 5), (1, 4), (1, 5), (10, 4), (10, 5), (10, 6), (11, 3), (11, 7), (12, 2), (12, 8), (13, 2), (13, 8), (14, 5), (15, 3), (15, 7), (16, 4), (16, 5), (16, 6), (17, 5), (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (22, 1), (22, 5), (24, 0), (24, 1), (24, 5), (24, 6), (34, 2), (34, 3), (35, 2), (35, 3)],
        PatternType.SIMKIN_GLIDER_GUN: [(0, 4), (0, 5), (1, 4), (1, 5), (10, 4), (10, 5), (10, 6), (11, 3), (11, 7), (12, 2), (12, 8), (13, 2), (13, 8), (14, 5), (15, 3), (15, 7), (16, 4), (16, 5), (16, 6), (17, 5), (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (22, 1), (22, 5), (24, 0), (24, 1), (24, 5), (24, 6), (34, 2), (34, 3), (35, 2), (35, 3)],
        PatternType.GARDEN_OF_EDEN: [(0, 0), (0, 1), (1, 0), (1, 1)],
        PatternType.R_PENTOMINO: [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)],
        PatternType.DIEHARD: [(0, 6), (1, 0), (1, 1), (2, 1), (2, 5), (2, 6), (2, 7)],
        PatternType.ACORN: [(0, 1), (1, 3), (2, 0), (2, 1), (2, 4), (2, 5), (2, 6)],
        PatternType.INFINITE_GROWTH: [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    }

    def __init__(self, row, col, sleep_time=1, verbose=False):
        self.row = row
        self.col = col
        self.VERBOSE = verbose
        self.rules = []
        self.set_initial_state(GameOfLife.PATTERNS[PatternType.GLIDER]) # default pattern
        self.sleep_time = sleep_time
        self.__set_draw_env__()
    
    def __set_draw_env__(self):
        pygame.init()
        pygame.display.set_caption("Game of Life")
        self.grid_display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.get_surface().fill((200, 200, 200))

    def __create_square__(self, x, y, color, grid_node_width=10, grid_node_height=10, scale=1):
        pygame.draw.rect(self.grid_display, color, [x, y, grid_node_width * scale, grid_node_height * scale])
    
    def __get_next_state__(self, row, col):
        is_alive = 0
        for rule in self.rules:
            is_alive = is_alive or rule(self, row, col)

        if self.VERBOSE: print(f"Next state of {row}, {col} is {is_alive}")
        return int(is_alive)
    
    def __next_generation__(self):
        next_gen = self.__create_matrix__(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                next_gen[i][j] = self.__get_next_state__(i, j)
        return next_gen            


    def __visualize_grid__(self):
        y = 0  # we start at the top of the screen
        grid_node_width = GameOfLife.WIDTH // len(self.matrix[0])
        grid_node_height = GameOfLife.HEIGHT // len(self.matrix)
        for row in self.matrix:
            x = 0 # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    self.__create_square__(x, y, (255, 255, 255), grid_node_width, grid_node_height, 0.95)
                else:
                    self.__create_square__(x, y, (0, 0, 0), grid_node_width, grid_node_height, 0.95)

                x += grid_node_width # for ever item/number in that row we move one "step" to the right
            y += grid_node_height   # for every new row we move one "step" downwards
        pygame.display.update()

    def __create_matrix__(self, rows, cols):
        return [[0 for _ in range(cols)] for _ in range(rows)]

    def add_rule(self, rule: callable):
        '''
        A rule is a function that takes in this object, row and column and returns a boolean value.
        It follows The Game of Life rules.
        '''
        self.rules.append(rule)

    def run(self, generations):
        for _ in range(generations):
            self.__visualize_grid__()
            self.matrix = self.__next_generation__()
            time.sleep(self.sleep_time)
            pygame.event.pump()

    def get_neighbours(self, row, col):
        neighbours = []
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                if i < 0 or i >= len(self.matrix):
                    continue
                if j < 0 or j >= len(self.matrix[0]):
                    continue
                neighbours.append(self.matrix[i][j])
        if self.VERBOSE: print(f"Neighbours of {row}, {col} are {neighbours}")
        return neighbours

    def set_initial_state(self, pattern: list, offset=(0, 0), use_old_state=False):
        '''
        Sets the initial state of the game, which may include one or more patterns.
        '''
        if not use_old_state:
            self.matrix = self.__create_matrix__(self.row, self.col)
        for x, y in pattern:
            self.matrix[x + offset[0]][y + offset[1]] = 1

def rule_1(game: GameOfLife, x, y) -> bool:
    neighbours = game.get_neighbours(x, y)
    return game.matrix[x][y] and 3 >= sum(neighbours) >= 2

def rule_2(game: GameOfLife, x, y) -> bool:
    neighbours = game.get_neighbours(x, y)
    return sum(neighbours) == 3

def main():
    rows, cols = map(int, input().split())
    generations = int(input())

    game_of_life = GameOfLife(rows, cols, sleep_time=0.2)
    game_of_life.add_rule(rule_1)
    game_of_life.add_rule(rule_2)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.LWSS])
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.GLIDER], offset=(5, 5), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.BLINKER], offset=(10, 10), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.TOAD], offset=(15, 15), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.BEACON], offset=(20, 50), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.MWSS], offset=(60, 60), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.HWSS], offset=(80, 80), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.PULSAR], offset=(100, 100), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.PENTADECATHLON], offset=(120, 100), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.GOSPER_GLIDER_GUN], offset=(130, 100), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.SIMKIN_GLIDER_GUN], offset=(140, 100), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.GARDEN_OF_EDEN], offset=(150, 100), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.R_PENTOMINO], offset=(160, 100), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.DIEHARD], offset=(100, 50), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.ACORN], offset=(100, 75), use_old_state=True)
    game_of_life.set_initial_state(GameOfLife.PATTERNS[PatternType.INFINITE_GROWTH], offset=(100, 0), use_old_state=True)

    game_of_life.run(generations)

if __name__ == '__main__':
    main()