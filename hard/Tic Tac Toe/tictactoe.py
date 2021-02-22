import random
from itertools import cycle
import math
import re

moves = ["X", "O"]
moves_cycle = cycle(moves)


def print_field(l):
    print("""
---------
| {} {} {} |
| {} {} {} |
| {} {} {} |
---------
""".format(*l))


def check_state(state):
    wins = [state[:3], state[3:6], state[6:], state[0:9:3], state[1:9:3], state[2:9:3], state[0:9:4], state[2:7:2]]
    if abs(state.count("X") - state.count("O")) > 1 or (['X', 'X', 'X'] in wins and ['O', 'O', 'O'] in wins):
        print("Impossible")
    elif ['X', 'X', 'X'] in wins:
        print_field(state)
        print("X wins\n")
        return True
    elif ['O', 'O', 'O'] in wins:
        print_field(state)
        print("O wins\n")
        return True
    elif state.count("_") == 0:
        print_field(state)
        print("Draw\n")
        return True
    else:
        return False


def calc_best_move(state, token):
    state_helper = list("012345678")
    wins = [state[:3], state[3:6], state[6:], state[0:9:3], state[1:9:3], state[2:9:3], state[0:9:4], state[2:7:2]]
    wins_helper = [state_helper[:3], state_helper[3:6], state_helper[6:], state_helper[0:9:3], state_helper[1:9:3],
                   state_helper[2:9:3], state_helper[0:9:4], state_helper[2:7:2]]
    for win, helper in list(zip(wins, wins_helper)):
        if win.count(token) == 2 and win.count("_") == 1:
            for i in range(len(win)):
                if win[i] != token:
                    return int(helper[i])


def easy_move(state):
    # Random moves
    print('Making move level "easy"')
    while True:
        placement = random.randrange(0, 9)
        if state[placement] in ["O", "X"]:
            continue
        else:
            state[placement] = next(moves_cycle)
            break
    return state


def human_move(state):
    if state.count("_") == 0:
        pass
    while True:
        coordinates = re.split("[ ]+", input("Enter the coordinates:"))
        if not coordinates[0].isdigit() or not coordinates[1].isdigit():
            print("You should enter numbers!")
            continue
        elif int(coordinates[0]) > 3 or int(coordinates[1]) > 3:
            print("Coordinates should be from 1 to 3!")
            continue
        cords_1d = ((int(coordinates[0]) - 1) * 3) + (int(coordinates[1]) - 1)
        if state[cords_1d] != "_":
            print("This cell is occupied! Choose another one!")
            continue
        else:
            state[cords_1d] = next(moves_cycle)
            break
    return state


def medium_move(state):
    print('Making move level "medium"')
    my_move = next(moves_cycle)
    if my_move == "X":
        opponent_move = "O"
    else:
        opponent_move = "X"

    my_placement = calc_best_move(state, my_move)
    opp_placement = calc_best_move(state, opponent_move)
    # calc win in one for myself:
    if my_placement is not None:
        state[my_placement] = my_move
        return state
    # calc win in one for the opponent:
    elif opp_placement is not None:
        state[opp_placement] = my_move
        return state
    # if no win in one or block of a win in one make a random move
    while True:
        placement = random.randrange(0, 9)
        if state[placement] in ["O", "X"]:
            continue
        else:
            state[placement] = my_move
            break
    return state


def minimax(board):
    depth = len(available_moves(board))

    if board.count("X") > board.count("O"):
        player = "O"
    elif board.count("_") == 9:
        player = "X"
    else:
        player = "X"

    if player == "X":
        best = [-1, -math.inf]
    else:
        best = [-1, math.inf]

    if depth == 0 or winning(board, "X") or winning(board, "O"):
        score = board_state(board, "X")
        return [-1, score * (depth + 1)]

    for cell in available_moves(board):
        sim_board = sim_move(board, cell, player)
        score = minimax(sim_board)[1]
        if player == "X":
            if score > best[1]:
                best[0], best[1] = cell, score
        else:
            if score < best[1]:
                best[0], best[1] = cell, score
    return best


def hard_move(state):
    print('Making move level "hard"')
    state[minimax(state)[0]] = next(moves_cycle)
    return state


def sim_move(state, move, player):
    sim_state = list(state)
    sim_state[move] = player
    return "".join(sim_state)


def start_game():
    state = list("_________")
    player_one, player_two = determine_game_type()
    play_game(state, player_one, player_two)


def play_game(state, player_one, player_two):

    print_field(state)
    while True:
        if not check_state(player_one(state)):
            print_field(state)
        else:
            break
        if not check_state(player_two(state)):
            print_field(state)
        else:
            break
    start_game()


def determine_game_type():
    fun_choices = {'easy': easy_move, 'user': human_move, 'medium': medium_move, 'hard': hard_move}
    while True:
        input_list = [i for i in input("Input command:").split()]
        if input_list[0] == "exit":
            exit(0)
        elif len(input_list) != 3 or input_list[1] not in fun_choices.keys() or input_list[2] not in fun_choices.keys()\
                or input_list[0] not in ["exit", "start"]:
            print("Bad parameters!")
        else:
            return fun_choices.get(input_list[1], incorrect_input), fun_choices.get(input_list[2], incorrect_input)


def incorrect_input():
    print("Incorrect input, try again\n")


def available_moves(board):
    return [p for p, char in enumerate(board) if char == "_"]


def winning(board, player):
    wins = [board[:3], board[3:6], board[6:], board[0:9:3], board[1:9:3], board[2:9:3], board[0:9:4], board[2:7:2]]
    return "".join(player*3) in wins


def board_state(board, player):
    wins = [board[:3], board[3:6], board[6:], board[0:9:3], board[1:9:3], board[2:9:3], board[0:9:4], board[2:7:2]]
    if player == "X":
        other_player = "O"
    else:
        other_player = "X"

    if "".join(player*3) in wins:
        return 10
    elif "".join(other_player*3) in wins:
        return -10
    elif board.count("_") == 0:
        return 0


start_game()
