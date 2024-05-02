import math
import random

from constants import BOARD_SIZE


class Random_Play:
    def __init__(self, board, iterations=1000, time_limit=None):
        self.board = board
        self.iterations = iterations
        self.time_limit = time_limit

    def determine_goat_move(self, tigers, goats, empty_positions, remaining_goat_number):
        self.tigers = tigers
        self.remaining_goat_number = remaining_goat_number
        self.empty_positions = empty_positions
        self.goats = goats
        legal_moves = self.get_legal_moves()
        return random.choice(legal_moves)

    def get_legal_moves(self):
        #List all possible legal moves for the goats, considering safety and restricted positions.
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        restricted_positions = {
            (1, 0), (3, 0), (0, 1), (2, 1), (4, 1), (1, 2), (3, 2), (0, 3), (2, 3), (4, 3), (1, 4), (3, 4)
        }

        legal_moves = []
        if self.remaining_goat_number > 0:
            # Prioritize safe placements before risky ones
            safe_empty_positions = [empty for empty in self.empty_positions if not self.is_adjacent_to_tiger(empty)]
            risky_empty_positions = [empty for empty in self.empty_positions if self.is_adjacent_to_tiger(empty)]
            for empty in safe_empty_positions + risky_empty_positions:
                legal_moves.append((None, empty))  # None signifies placement of a new goat

        # Movement moves
        for goat in self.goats:
            allowed_directions = normal_directions if goat in restricted_positions else normal_directions + diagonal_directions
            for dx, dy in allowed_directions:
                nx, ny = goat[0] + dx, goat[1] + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) not in self.tigers and (
                        nx, ny) not in self.goats:
                    if not self.is_adjacent_to_tiger((nx, ny)):
                        legal_moves.insert(0, (goat, (nx, ny)))  # Prioritize safer moves
                    else:
                        legal_moves.append((goat, (nx, ny)))  # Add risky moves if necessary
        return legal_moves

    def do_move(self, move):
        # Update the state by performing a move
        goat_position, new_position = move
        if goat_position:
            # Move existing goat
            self.goats.remove(goat_position)
            self.goats.append(new_position)
            self.empty_positions.append(goat_position)
        else:
            # Place new goat
            self.goats.append(new_position)
        self.empty_positions.remove(new_position)

    def is_adjacent_to_tiger(self, position):
        # Check if a position is adjacent to any tiger
        px, py = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        return any((px + dx, py + dy) in self.tigers for dx, dy in directions)

    def can_move(self, position, direction):
       # Check if a move is valid given a position and direction, considering board boundaries and other pieces
        px, py = position
        dx, dy = direction
        nx, ny = px + dx, py + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if (nx, ny) not in self.tigers and (nx, ny) not in self.goats:
                return True
        return False

