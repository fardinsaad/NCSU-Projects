import pygame
from constants import *
import pygame.font
# We draw all the staff o board by this class
class Board:
    def __init__(self, screen):
        self.screen = screen

    # Draw the game info at the top of the board
    def draw_info(self, goats_on_board, remaining_goat_number, number_of_moves, message):
        # Position the text at the bottom of the board
        info_y_position = SCREEN_SIZE  - 500  # Adjust this as necessary
        self.draw_text(f"Remaining Goats: {remaining_goat_number}", (MARGIN-50, info_y_position))
        self.draw_text(f"Goats on Board: {goats_on_board}", (MARGIN + 170, info_y_position))
        self.draw_text(f"Moves: {number_of_moves}", (MARGIN + 370, info_y_position))
        self.draw_text(f"Result: {message}", (MARGIN + 470, info_y_position))

    # Styling the text of the board
    def draw_text(self, text, position, font_size=25, color=(61, 52, 235)):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    # It will draw the lines of the board and create the base of the game : The Board
    def draw_lines(self):
        # Draw the horizontal and vertical lines
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE + MARGIN, MARGIN),
                             (i * CELL_SIZE + MARGIN, SCREEN_SIZE + MARGIN), 1)
            pygame.draw.line(self.screen, LINE_COLOR, (MARGIN, i * CELL_SIZE + MARGIN),
                             (SCREEN_SIZE + MARGIN, i * CELL_SIZE + MARGIN), 1)
        # Draw 6 diagonal Lines
        pygame.draw.line(self.screen, LINE_COLOR, (MARGIN, MARGIN),
                         (SCREEN_SIZE + MARGIN, SCREEN_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (SCREEN_SIZE + MARGIN, MARGIN),
                         (MARGIN, SCREEN_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, MARGIN),
                         (MARGIN, 2 * CELL_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, MARGIN),
                         (SCREEN_SIZE + MARGIN, 2 * CELL_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, SCREEN_SIZE + MARGIN),
                         (MARGIN, 2 * CELL_SIZE + MARGIN), 1)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE + MARGIN, SCREEN_SIZE + MARGIN),
                         (SCREEN_SIZE + MARGIN, 2 * CELL_SIZE + MARGIN), 1)

    # This method will draw the goats and tiger on the board after each move
    def draw_pieces(self, goats, tigers):
        for goat in goats:
            center = ((goat[1] * CELL_SIZE) + MARGIN, (goat[0] * CELL_SIZE) + MARGIN)
            pygame.draw.circle(self.screen, GOAT_COLOR, center, CELL_SIZE // 8)

        for tiger in tigers:
            center = ((tiger[1] * CELL_SIZE) + MARGIN, (tiger[0] * CELL_SIZE) + MARGIN)
            pygame.draw.circle(self.screen, TIGER_COLOR, center, CELL_SIZE // 8)

    # method fpr calling all relevant methods to draw everything on the board
    def draw(self, goats, tigers):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_lines()
        self.draw_pieces(goats, tigers)
        pygame.display.flip()