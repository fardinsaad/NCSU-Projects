import pygame
import sys
from game import Game
from constants import WINDOW_SIZE


def main():
    # Command line argument for passing the Algorithm name
    algorithm = sys.argv[1].lower()
    if algorithm not in ["random", "bfs", "dfs", "monte_carlo", "astar"]:
        sys.exit("Invalid Algorithm specified, Valid Options: random, bfs, dfs, astar, monte_carlo")
    # Initialize our game
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Bagh Bandi Game')
    # Passing the algorithm name and run the name
    game = Game(screen, algorithm)
    game.run()
    sys.exit()


if __name__ == '__main__':
    main()
