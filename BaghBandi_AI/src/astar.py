import random
import heapq
import random
from constants import *
from constants import BOARD_SIZE


class ASTAR:
    # def determine_goat_move(board, tigers, goats, empty_positions):
    #         new_goat_position = random.choice(empty_positions)
    #         return new_goat_position

    def __init__(self, board):
        self.board = board

    def is_adjacent_to_tiger(self, position, tigers):
        """ Check if a position is adjacent to any tiger """
        px, py = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        adjacent_tigers = [(px + dx, py + dy) for dx, dy in directions if (px + dx, py + dy) in tigers]
        return adjacent_tigers

    def is_adjacent_to_empty_space(self, position, empty_positions):
        """ Check if a position is adjacent to any tiger """
        px, py = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        adjacent_empty_space = [(px + dx, py + dy) for dx, dy in directions if (px + dx, py + dy) in empty_positions]
        return adjacent_empty_space

    def determine_goat_move(self, tigers, goats, empty_positions, remaining_goat_number):
        # print("tigers", tigers, "goats", goats, "empty positions,", empty_positions)
        remaining_goats = remaining_goat_number
        count_goats = 0
        print(remaining_goats)
        normal_directions = [(0, -1), (1, 0), (0, -1), (0, 1)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        restricted_positions = {(1, 0), (3, 0), (0, 1), (2, 1), (4, 1), (1, 2), (3, 2), (0, 3), (2, 3), (4, 3), (1, 4),
                                (3, 4)}
        # checks to see if goat is empty at first and picks a random position from the optimal ones at first
        if goats == []:
            empty_position_to_pick = [(0, 2), (2, 0), (2, 2), (4, 2), (2, 4)]
            a = random.choice(empty_position_to_pick)
            return (None, a)
        else:

            closest_tiger = None
            closest_distance = float('inf')
            normal_directions = [(0, -1), (1, 0), (0, -1), (0, 1)]
            diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            restricted_positions = {(1, 0), (3, 0), (0, 1), (2, 1), (4, 1), (1, 2), (3, 2), (0, 3), (2, 3), (4, 3),
                                    (1, 4),
                                    (3, 4)}
            starting_slot = [2, 2]
            # print("goats", goats)
            # print("empty positions", empty_positions)
            legal_moves = []
            list_of_heuristic = []
            # count_goats = 0
            # print("check kori", count_goats)
            # legal_moves.append((slot, (nx, ny)))
            for slot in empty_positions:
                notiger = True
                oppos_goat = True
                if slot in restricted_positions:
                    directions = normal_directions  # Only horizontal and vertical moves
                else:
                    directions = normal_directions + diagonal_directions  # All possible moves

                for dx, dy in directions:
                    nx, ny = slot[0] + dx, slot[1] + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        if (nx, ny) not in tigers:
                            print("no tiger no goat in adjacent pos")
                        elif (nx, ny) in tigers:
                            diagx_end, diagy_end = slot[0] - dx, slot[1] - dy
                            # check if the opposite end is in the board
                            if 0 <= diagx_end < BOARD_SIZE and 0 <= diagy_end < BOARD_SIZE:
                                if (diagx_end, diagy_end) not in goats:
                                    oppos_goat = False  # opposite e goat nai, ek pash e tiger -> bad

                # Assigning heuristic value over here to see if any adjacenet side has tiger and the exact opposite of the adjacent side does not have a goat, then
                # it is really bad, since the tiger can go over the goat and capture it. So, assigning a negative heuristic value of -100.
                if oppos_goat == False:
                    a = [-100, goats[0], slot]
                    # list_of_heuristic.append([-100, goats[0], slot])
                    # if a[0] == -100:
                    #     if (count_goats <=16 or remaining_goats > 0):
                    #         list_of_heuristic.append([-100, None, slot])
                    #         count_goats += 1
                    list_of_heuristic.append([-100, goats[0], slot])
                else:
                    # Assigning heuristic value over here to see if any adjacent side has no tiger, irrespective of having or not having goats in adjacent sides.
                    # This implies, it's a good state since there's no tigers in the surrounding, so assigning a positive heuristic of +100.

                    print("count ki barse naki", count_goats)
                    a = [100, goats[0], slot]

                    # Please fix the counting here. I wanted to do something like, if the total placement of goats has already been 16, then, it will no longer place a new goat,
                    # and simply move the existing goats around. But it's not working.
                    if count_goats <= 15:
                        list_of_heuristic.append([100, None, slot])
                        count_goats += 1
                    else:
                        list_of_heuristic.append([100, goats[0], slot])
                        break
                    # print("current kotogula goat boashaisi", count_goats)
                    # list_of_heuristic.append([100, goats[0], slot])

                    # if (nx, ny) not in tigers and (nx, ny) not in goats:
                    #     legal_moves.append((slot, (nx, ny)))
                    #     heuristic = self.calculate_heuristic(slot, (nx, ny), goats, tigers)
                    #     list_of_heuristic.append(heuristic)
                    # print("ekhon kar position er jonno", list_of_heuristic)

            # print(legal_moves)
            # print(list_of_heuristic)

            # Over here, from the list of heuristics for a particular slot, we pick the highest one, and return the corresponding old and new positions for that heuristic
            for i in list_of_heuristic:
                if i[0] == 100:
                    return [i[1], i[2]]
            # return list_of_heuristic

