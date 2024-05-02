import random
import math
from constants import BOARD_SIZE  # Assuming BOARD_SIZE is defined in constants


class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.state = state
        self.untried_moves = state.get_legal_moves()

    def select_child(self):
        """Select a child node with the highest UCB1 value."""
        exploration_constant = 1.5
        return max(self.children, key=lambda c: (c.wins / c.visits) + math.sqrt(
            exploration_constant * math.log(self.visits) / c.visits))

    def add_child(self, move, state):
        """Add a new child node for the given move."""
        child = Node(move=move, parent=self, state=state)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        """Update this node - increment the visit count by 1 and increase wins by the result of the play-out."""
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return f"[M:{self.move} W/V:{self.wins}/{self.visits} U:{len(self.untried_moves)}]"


class MonteCarlo:
    def __init__(self, board, iterations=2000, time_limit=None):
        self.board = board
        self.iterations = iterations
        self.time_limit = time_limit

    def determine_goat_move(self, tigers, goats, empty_positions, remaining_goat_number):
        root = Node(state=State(tigers, goats, empty_positions, remaining_goat_number))

        for _ in range(self.iterations):
            node = root
            state = root.state.clone()

            # Selection
            while not node.untried_moves and node.children:
                node = node.select_child()
                state.do_move(node.move)

            # Expansion
            if node.untried_moves:
                m = random.choice(node.untried_moves)
                state.do_move(m)
                node = node.add_child(m, state)

            # Simulation
            while state.get_legal_moves():
                state.do_move(random.choice(state.get_legal_moves()))

            # Backpropagation
            while node:
                result = state.get_result()
                node.update(result)
                node = node.parent
                

        if not root.children:
            print("Legal moves: ", root.state.get_legal_moves())
            return None  # Handle no valid moves

        return max(root.children, key=lambda c: c.visits).move


class State:
    def __init__(self, tigers, goats, empty_positions, remaining_goat_number):
        self.tigers = tigers
        self.goats = goats
        self.empty_positions = empty_positions
        self.remaining_goat_number = remaining_goat_number
        self.restricted_positions = {(1, 0), (3, 0), (0, 1), (2, 1), (4, 1), (1, 2), (3, 2), (0, 3), (2, 3), (4, 3),
                                     (1, 4), (3, 4)}

    def is_adjacent_to_tiger(self, position):
        """ Check if the given position is adjacent to any tiger, considering restricted diagonal movements. """
        x, y = position
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Check for restricted movements: if either the current position or the tiger's position is restricted
        if position in self.restricted_positions:
            allowed_directions = normal_directions  # Only cardinal directions allowed
        else:
            allowed_directions = normal_directions + diagonal_directions  # Both cardinal and diagonal directions

        for dx, dy in allowed_directions:
            adj_position = (x + dx, y + dy)
            if (dx != 0 or dy != 0) and adj_position in self.tigers:
                if (x, y) not in self.restricted_positions and (x + dx, y + dy) not in self.restricted_positions:
                    return True
                elif (dx, dy) in normal_directions:  # Check cardinal directions regardless of restrictions
                    return True
        return False

    def is_within_bounds(self, position):
        """ Check if a position is within the board boundaries """
        x, y = position
        return 0 <= x <= BOARD_SIZE and 0 <= y <= BOARD_SIZE

    def can_move(self, tiger):
        """ Check if a tiger can move or jump to capture a goat, with restrictions on diagonal moves """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cardinal directions
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
        all_possible_moves = directions.copy()

        if tiger not in self.restricted_positions:
            all_possible_moves.extend(diagonal_directions)  # Allow diagonal moves only from non-restricted positions

        for d in all_possible_moves:
            normal_move = (tiger[0] + d[0], tiger[1] + d[1])
            jump_move = (tiger[0] + 2 * d[0], tiger[1] + 2 * d[1])
            if self.is_within_bounds(normal_move) and self.is_free(normal_move):
                return True
            if self.is_within_bounds(jump_move) and self.is_occupied_by_goat(normal_move) and self.is_free(jump_move):
                return True

        return False

    def is_free(self, position):
        """ Check if a position is free of both tigers and goats """
        return position not in self.tigers and position not in self.goats

    def is_occupied_by_goat(self, position):
        """ Check if a position is occupied by a goat """
        return position in self.goats

    def do_move(self, move):
        """ Update the state by performing a move """
        goat_position, new_position = move
        if goat_position:
            self.goats.remove(goat_position)
            self.goats.append(new_position)
            self.empty_positions.append(goat_position)
        else:
            self.goats.append(new_position)
        self.empty_positions.remove(new_position)

    def get_result(self):
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        boundary = [(0, 0), (0, 4), (4, 0), (4, 4)]
        if not self.goats:
            return -1000  # All goats are captured, tigers win. High penalty.

        if all(not self.can_move(tiger) for tiger in self.tigers):
            return 1000  # All tigers are immobilized, goats win. High reward.

        score = 0
        for goat in self.goats:
            if self.is_adjacent_to_tiger(goat):
                score -= 10  # Increased penalty for goats in immediate danger.
                if self.is_unprotected_in_capture_direction(goat):
                    score -= 120  # High penalty if no protective goat/tiger in the direct line of potential capture.

            # Reward for goats that are protected by another goat when under threat
            if self.is_capture_blocked_by_goat(goat):
                score += 100  # Increase the reward to reflect the strategic importance of protection.
            # Reward for goats that are protected by another tiger when under threat
            if self.is_capture_blocked_by_tiger(goat):
                score += 20  # Increase the reward to reflect the strategic importance of protection.

            #  Goat in boundary spaces
            #if goat in boundary:
            #    score += 1

            # Reward for goats that are protected by another goat.
            if self.has_protective_neighbor(goat):
                score += 10  # Increase the reward to reflect the strategic importance of protection.

            # Reward for goats are escape from imminent threat of capture
            allowed_directions = normal_directions + diagonal_directions if goat not in self.restricted_positions else normal_directions
            for direction in allowed_directions:
                nx, ny = goat[0] + direction[0], goat[1] + direction[1]
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.is_free(
                        (nx, ny)) and not self.is_adjacent_to_tiger((nx, ny)):
                    score += 1  # Reward for potential safe moves

        return score

    def has_protective_neighbor(self, goat):
        """Check if there is a protective neighbor goat next to the endangered goat that itself is not in immediate
        danger of capture."""
        x, y = goat

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor_pos = (x + dx, y + dy)
                if neighbor_pos in self.goats:
                    return True
        return False

    def is_capture_blocked_by_tiger(self, goat_position):
        """Check if a goat at this position is protected from capture by another tiger blocking the capture
        path."""
        x, y = goat_position
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        all_possible_moves = normal_directions + diagonal_directions

        for dx, dy in all_possible_moves:
            jump_position = (x + 2 * dx, y + 2 * dy)
            mid_position = (x + dx, y + dy)

            # Check movement restrictions for diagonals
            if (dx, dy) in diagonal_directions and (
                    goat_position in self.restricted_positions or mid_position in self.restricted_positions):
                continue  # Skip if the move is diagonal and either position is restricted

            if self.is_within_bounds(jump_position) and self.is_within_bounds(mid_position):
                if mid_position in self.tigers and jump_position in self.tigers:
                    return True  # Capture path is blocked by another tiger 

        return False

    def is_capture_blocked_by_goat(self, goat_position):
        """Check if a goat at this position is protected from capture by another goat blocking the capture
        path."""
        x, y = goat_position
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        all_possible_moves = normal_directions + diagonal_directions

        for dx, dy in all_possible_moves:
            jump_position = (x + 2 * dx, y + 2 * dy)
            mid_position = (x + dx, y + dy)

            # Check movement restrictions for diagonals
            if (dx, dy) in diagonal_directions and (
                    goat_position in self.restricted_positions or mid_position in self.restricted_positions):
                continue  # Skip if the move is diagonal and either position is restricted

            if self.is_within_bounds(jump_position) and self.is_within_bounds(mid_position):
                if mid_position in self.goats and jump_position in self.goats:
                    return True  # Capture path is blocked by another goat

        return False

    def is_unprotected_in_capture_direction(self, goat):
        """Check if the goat lacks protection directly in the line of a potential capture by an adjacent tiger,
        respecting restricted movements for diagonals."""
        x, y = goat
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Determine which directions are allowed based on the goat's position
        allowed_directions = normal_directions + diagonal_directions if goat not in self.restricted_positions else normal_directions

        for dx, dy in allowed_directions:
            tiger_position = (x + dx, y + dy)
            potential_goat_blocker = (x + 2 * dx, y + 2 * dy)
            if tiger_position in self.tigers:
                # Check if the position directly behind the goat is blocked by another goat or tiger or is outside of
                # bounds
                if not (self.is_within_bounds(potential_goat_blocker) and (
                        potential_goat_blocker in self.goats or potential_goat_blocker in self.tigers or potential_goat_blocker in self.tigers)):
                    return True  # There's a tiger, and no protective goat or tiger in the jump position
        return False

    def get_legal_moves(self):
        normal_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        legal_moves = []
        protective_moves = []
        escape_moves = []

        for goat in self.goats:
            if self.is_adjacent_to_tiger(goat):
                # Check each possible movement direction for protection and escape
                for direction in normal_directions + diagonal_directions:
                    next_position = (goat[0] + direction[0], goat[1] + direction[1])
                    if goat not in self.restricted_positions or direction in normal_directions:
                        # Directly next to the goat in the same line as the threat
                        if self.is_within_bounds(next_position) and self.is_free(next_position):
                            # Check if this position directly blocks the tiger
                            if self.directly_blocks_tiger(goat, next_position):
                                protective_moves.append((None, next_position))
                            elif not self.is_adjacent_to_tiger(next_position):
                                escape_moves.append((goat, next_position))

        # Evaluate and prioritize moves based on strategic importance
        if protective_moves:
            # Protective moves are prioritized over escape moves
            return protective_moves

        # Escape move come after protective moves
        if escape_moves:
            return escape_moves

        # Regular safe placements from goats not on the board and not adjacent to tigers
        if self.remaining_goat_number - len(self.goats) > 0:
            for empty in self.empty_positions:
                if not self.is_adjacent_to_tiger(empty):
                    legal_moves.append((None, empty))

        #  Regular safe placements from goats on the board and not adjacent to tigers
        for goat in self.goats:
            allowed_directions = normal_directions if goat in self.restricted_positions else normal_directions + diagonal_directions
            for dx, dy in allowed_directions:
                nx, ny = goat[0] + dx, goat[1] + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.is_free(
                        (nx, ny)) and not self.is_adjacent_to_tiger((nx, ny)):
                    legal_moves.append((goat, (nx, ny)))

        if legal_moves:
            return legal_moves

        # Regular safe placements from goats not on the board
        if self.remaining_goat_number - len(self.goats) > 0:
            for empty in self.empty_positions:
                legal_moves.append((None, empty))

        #  Regular safe placements from goats on the board
        for goat in self.goats:
            allowed_directions = normal_directions if goat in self.restricted_positions else normal_directions + diagonal_directions
            for dx, dy in allowed_directions:
                nx, ny = goat[0] + dx, goat[1] + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.is_free((nx, ny)):
                    legal_moves.append((goat, (nx, ny)))

        return legal_moves   # Include all moves

    def directly_blocks_tiger(self, goat, next_position):
        """ Check if placing a goat at next_position directly blocks a tiger from capturing the goat at goat_position"""
        # Assuming the tiger must jump over the goat to capture and needs an empty space directly beyond the goat
        dx = next_position[0] - goat[0]
        dy = next_position[1] - goat[1]
        tiger_position = (goat[0] - dx, goat[1] - dy)
        return tiger_position in self.tigers

    def clone(self):
        """ Create a deep copy of the current game state """
        return State(self.tigers.copy(), self.goats.copy(), self.empty_positions.copy(), self.remaining_goat_number)
