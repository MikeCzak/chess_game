# Michael Czak

###### CODE SUMMARY ######
# CODE.........................................................................................LINE

# "global" variables...........................................................................26

# FUNCTIONS
# rules for moving pieces......................................................................69
# visualiziation of possible moves.............................................................317
# pieces (dictionaries with attributes)........................................................343
# intro animation..............................................................................545
# fixed starting position when no game is loaded...............................................577
# read starting position (loaded or fixed) and write position to piece dictionaries............587
# draw chess board (called regularly)..........................................................597
# check if king is in check position...........................................................649
# save and quit................................................................................656
# start turn (user inputs for movement)........................................................668
# check for existing game (and load external savegame).........................................763
# continue game (if game exists)...............................................................785
# new game.....................................................................................798


import json
import os
from time import sleep
import sys

shutdown = [False]

red = "\x1b[31m"
red_bg = "\x1b[41m"
blue = "\x1b[34m"
white = "\x1b[0m"

check_text = f"{red}     ! CHECK ! {white}"
check_message = ""
check = False

col_map = {
    "a":0,
    "b":1,
    "c":2,
    "d":3,
    "e":4,
    "f":5,
    "g":6,
    "h":7,
}
board = [
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
]

possible_moves_board = []
possible_moves = []
for row in range(8):
    possible_moves_board.append([])
    for col in range(8):
        possible_moves_board[row].append([])

# SET OF RULES
def moves_acc_to_rules(id):
    possible_moves = []
    row = id["position"][0]
    col = id["position"][1]
    u = 0  #up
    d = 0  #down
    l = 0  #left
    r = 0  #right
    ur = 0 #up right
    dr = 0 #down right
    dl = 0 #down left
    ul = 0 #up left
    match id["piece"]:
        case "king":
            possible_steps = [
                [0, 1],
                [1, 1],
                [1, 0],
                [1, -1],
                [0, -1],
                [-1, -1],
                [-1, 0],
                [-1, 1]
            ]
            for step in possible_steps:
                if row + step[0] > -1 and row + step[0] < 8 and col + step[1] > -1 and col + step[1] < 8:
                    if board[row+step[0]][col+step[1]] == "  ":
                        possible_moves.append([row+step[0], col+step[1], "\u2B1C"])
                    else:
                        if board[row+step[0]][col+step[1]]["side"] != id["side"]:
                            possible_moves.append([row+step[0], col+step[1], "\u274C"])
        case "queen":
            for rows in range(1, 8):
                if row + rows < 8:                                  #down
                    if board[row+rows][col] == "  ":
                        possible_moves.append([(row+rows), col, "\u2B1C"])
                    else:
                        if board[row+rows][col]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([(row+rows), col, "\u274C"])
                            break
                else: break
            for rows in range(1, 8):
                if row - rows > -1:                                  #up
                    if board[row-rows][col] == "  ":
                        possible_moves.append([(row-rows), col, "\u2B1C"])
                    else:
                        if board[row-rows][col]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([(row-rows), col, "\u274C"])
                            break
                else: break

            for cols in range(1, 8):
                if col + cols < 8:                                   #right
                    if board[row][col+cols] == "  ":
                        possible_moves.append([row, (col+cols), "\u2B1C"])
                    else:
                        if board[row][col+cols]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row, (col+cols), "\u274C"])
                            break
            for cols in range(1, 8):
                if col - cols > -1:                                  #left
                    if board[row][col-cols] == "  ":
                        possible_moves.append([row, (col-cols), "\u2B1C"])
                    else:
                        if board[row][col-cols]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row, (col-cols), "\u274C"])
                            break
                else: break
            for fields in range(1, 8):
                if row + fields < 8 and col + fields < 8:       #down right
                    if board[row+fields][col+fields] == "  ":
                        possible_moves.append([row+fields, col+fields, "\u2B1C"])
                    else:
                        if board[row+fields][col+fields]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row+fields, col+fields, "\u274C"])
                            break
            for fields in range(1, 8):
                if row + fields < 8 and col - fields > -1:       #down left
                    if board[row+fields][col-fields] == "  ":
                        possible_moves.append([row+fields, col-fields, "\u2B1C"])
                    else:
                        if board[row+fields][col-fields]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row+fields, col-fields, "\u274C"])
                            break
            for fields in range(1, 8):
                if row - fields > -1 and col + fields < 8:       #up right
                    if board[row-fields][col+fields] == "  ":
                        possible_moves.append([row-fields, col+fields, "\u2B1C"])
                    else:
                        if board[row-fields][col+fields]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row-fields, col+fields, "\u274C"])
                            break
            for fields in range(1, 8):
                if row - fields > -1 and col - fields > -1:       #up left
                    if board[row-fields][col-fields] == "  ":
                        possible_moves.append([row-fields, col-fields, "\u2B1C"])
                    else:
                        if board[row-fields][col-fields]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row-fields, col-fields, "\u274C"])
                            break
        case "knight":
            possible_jumps = [
                [2, 1],
                [2, -1],
                [1, 2],
                [1, -2],
                [-2, 1],
                [-2, -1],
                [-1, 2],
                [-1, -2],
            ]
            for jump in possible_jumps:
                if row + jump[0] < 8 and row + jump[0] > -1 and col + jump[1] > -1 and col + jump[1] < 8:
                    if board[row+jump[0]][col+jump[1]] == "  ":
                        possible_moves.append([row+jump[0], col+jump[1], "\u2B1C"])
                    else:
                        if board[row+jump[0]][col+jump[1]]["side"] != id["side"]:
                            possible_moves.append([row+jump[0], col+jump[1], "\u274C"])
        case "bishop":
            for fields in range(1, 8):
                if row + fields < 8 and col + fields < 8:       #down right
                    if board[row+fields][col+fields] == "  ":
                        possible_moves.append([row+fields, col+fields, "\u2B1C"])
                    else:
                        if board[row+fields][col+fields]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row+fields, col+fields, "\u274C"])
                            break
            for fields in range(1, 8):
                if row + fields < 8 and col - fields > -1:       #down left
                    if board[row+fields][col-fields] == "  ":
                        possible_moves.append([row+fields, col-fields, "\u2B1C"])
                    else:
                        if board[row+fields][col-fields]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row+fields, col-fields, "\u274C"])
                            break
            for fields in range(1, 8):
                if row - fields > -1 and col + fields < 8:       #up right
                    if board[row-fields][col+fields] == "  ":
                        possible_moves.append([row-fields, col+fields, "\u2B1C"])
                    else:
                        if board[row-fields][col+fields]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row-fields, col+fields, "\u274C"])
                            break
            for fields in range(1, 8):
                if row - fields > -1 and col - fields > -1:       #up left
                    if board[row-fields][col-fields] == "  ":
                        possible_moves.append([row-fields, col-fields, "\u2B1C"])
                    else:
                        if board[row-fields][col-fields]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row-fields, col-fields, "\u274C"])
                            break
        case "pawn":
            match id["side"]:
                case "white":
                    if board[row-1][col] == "  ":
                        possible_moves.append([row-1, col, "\u2B1C"])
                        if row == 6 and board[row-2][col] == "  ":
                            possible_moves.append([row-2, col, "\u2B1C"])
                    if col > 0:        
                        if board[row-1][col-1] != "  " and board[row-1][col-1]["side"] != id["side"]:
                            possible_moves.append([row-1, col-1, "\u274C"])
                    if col < 7:
                        if board[row-1][col+1] != "  " and board[row-1][col+1]["side"] != id["side"]:
                            possible_moves.append([row-1, col+1, "\u274C"])

                case "black":
                    if board[row+1][col] == "  ":
                        possible_moves.append([row+1, col, "\u2B1C"])
                        if row == 1 and board[row+2][col] == "  ":
                            possible_moves.append([row+2, col, "\u2B1C"])
                    if col > 0: 
                        if board[row+1][col-1] != "  " and board[row+1][col-1]["side"] != id["side"]:
                            possible_moves.append([row+1, col-1, "\u274C"])
                    if col < 7:
                        if board[row+1][col+1] != "  " and board[row+1][col+1]["side"] != id["side"]:
                            possible_moves.append([row+1, col+1, "\u274C"])
        case "tower":
            for rows in range(1, 8):
                if row + rows < 8:                                  #down
                    if board[row+rows][col] == "  ":
                        possible_moves.append([(row+rows), col, "\u2B1C"])
                    else:
                        if board[row+rows][col]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([(row+rows), col, "\u274C"])
                            break
                else: break
            for rows in range(1, 8):
                if row - rows > -1:                                  #up
                    if board[row-rows][col] == "  ":
                        possible_moves.append([(row-rows), col, "\u2B1C"])
                    else:
                        if board[row-rows][col]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([(row-rows), col, "\u274C"])
                            break
                else: break

            for cols in range(1, 8):
                if col + cols < 8:                                   #right
                    if board[row][col+cols] == "  ":
                        possible_moves.append([row, (col+cols), "\u2B1C"])
                    else:
                        if board[row][col+cols]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row, (col+cols), "\u274C"])
                            break
            for cols in range(1, 8):
                if col - cols > -1:                                  #left
                    if board[row][col-cols] == "  ":
                        possible_moves.append([row, (col-cols), "\u2B1C"])
                    else:
                        if board[row][col-cols]["side"] == id["side"]:
                            break
                        else:
                            possible_moves.append([row, (col-cols), "\u274C"])
                            break
                else: break
    return possible_moves

# VISUALIZE POSSIBLE MOVES
def visualize_moves(possible_targets, piece):
    # copy board
    for rows in range(8):
        for cols in range(8):
            possible_moves_board[rows][cols] = board[rows][cols]

    # imprint possible moves
    for row, col, isEnemy in possible_targets:
        possible_moves_board[row][col] = isEnemy

    os.system("cls" if os.name == "nt" else "clear")
    print()
    print("  A B C D E F G H")

    for row in range(8):
        print(8-(row), end =" ")
        for cell in range(8):
            if type(possible_moves_board[row][cell]) == dict:
                if possible_moves_board[row][cell] == piece:
                    print(blue, possible_moves_board[row][cell]["image"], white, sep="", end="")  ########
                else:
                    print(possible_moves_board[row][cell]["image"], end="")
            else:
                print(possible_moves_board[row][cell], end="")
        print()

# PIECES
no_piece = {
    "image": "  "
}
w_tower_l = {
    "piece": "tower",
    "position": [],
    "side": "white",
    "image": "\u2656 ",
}
w_tower_r = {
    "piece": "tower",
    "position": [],
    "side": "white",
    "image": "\u2656 ",
}
w_knight_l = {
    "piece": "knight",
    "position": [],
    "side": "white",
    "image": "\u2658 ",
}
w_knight_r = {
    "piece": "knight",
    "position": [],
    "side": "white",
    "image": "\u2658 ",
}
w_bishop_l = {
    "piece": "bishop",
    "position": [],
    "side": "white",
    "image": "\u2657 ",
}
w_bishop_r = {
    "piece": "bishop",
    "position": [],
    "side": "white",
    "image": "\u2657 ",
}
w_queen = {
    "piece": "queen",
    "position": [],
    "side": "white",
    "image": "\u2655 ",
}
w_king = {
    "piece": "king",
    "position": [],
    "side": "white",
    "image": "\u2654 ",
}
w_pawn_a = {
    "piece": "pawn",
    "position": [],
    "side": "white",
    "image": "\u2659 ",
}
w_pawn_b = {
    "piece": "pawn",
    "position": [],
    "side": "white",
    "image": "\u2659 ",
}
w_pawn_c = {
    "piece": "pawn",
    "position": [],
    "side": "white",
    "image": "\u2659 ",
}
w_pawn_d = {
    "piece": "pawn",
    "position": [],
    "side": "white",
    "image": "\u2659 ",
}
w_pawn_e = {
    "piece": "pawn",
    "position": [],
    "side": "white",
    "image": "\u2659 ",
}
w_pawn_f = {
    "piece": "pawn",
    "position": [],
    "side": "white",
    "image": "\u2659 ",
}
w_pawn_g = {
    "piece": "pawn",
    "position": [],
    "side": "white",
    "image": "\u2659 ",
}
w_pawn_h = {
    "piece": "pawn",
    "position": [],
    "side": "white",
    "image": "\u2659 ",
}
b_tower_l = {
    "piece": "tower",
    "position": [],
    "side": "black",
    "image": "\u265c ",
}
b_tower_r = {
    "piece": "tower",
    "position": [],
    "side": "black",
    "image": "\u265c ",
}
b_knight_l = {
    "piece": "knight",
    "position": [],
    "side": "black",
    "image": "\u265e ",
}
b_knight_r = {
    "piece": "knight",
    "position": [],
    "side": "black",
    "image": "\u265e ",
}
b_bishop_l = {
    "piece": "bishop",
    "position": [],
    "side": "black",
    "image": "\u265d ",
}
b_bishop_r = {
    "piece": "bishop",
    "position": [],
    "side": "black",
    "image": "\u265d ",
}
b_queen = {
    "piece": "queen",
    "position": [],
    "side": "black",
    "image": "\u265b ",
}
b_king = {
    "piece": "king",
    "position": [],
    "side": "black",
    "image": "\u265a ",
}
b_pawn_a = {
    "piece": "pawn",
    "position": [],
    "side": "black",
    "image": "\u265f ",
}
b_pawn_b = {
    "piece": "pawn",
    "position": [],
    "side": "black",
    "image": "\u265f ",
}
b_pawn_c = {
    "piece": "pawn",
    "position": [],
    "side": "black",
    "image": "\u265f ",
}
b_pawn_d = {
    "piece": "pawn",
    "position": [],
    "side": "black",
    "image": "\u265f ",
}
b_pawn_e = {
    "piece": "pawn",
    "position": [],
    "side": "black",
    "image": "\u265f ",
}
b_pawn_f = {
    "piece": "pawn",
    "position": [],
    "side": "black",
    "image": "\u265f ",
}
b_pawn_g = {
    "piece": "pawn",
    "position": [],
    "side": "black",
    "image": "\u265f ",
}
b_pawn_h = {
    "piece": "pawn",
    "position": [],
    "side": "black",
    "image": "\u265f ",
}
active_pieces = []
defeated_pieces = []
#🅲🄷🅴🅂🆂
#🅼🄰🆂🅃🅴🅁
#🄼🄸🄺🄴🅂
#🅼🅸🅺🅴🆂
def draw_intro_board():
    spaces_even = 0
    spaces_odd = 1
    os.system("cls" if os.name == "nt" else "clear")
    print()
    print("  A B C D E F G H")
    for row in range(2):
        print(8-(row), end =" ")
        sleep(0.05)
        for cell in range(4):
            print(f"{'  '*(spaces_even%2)}" + "\u2B1C" + f"{'  '*(spaces_odd%2)}", end="")
        print("")
        spaces_even += 1
        spaces_odd += 1
    sleep(0.05)
    print("6 🅼 🄸 🅺 🄴 🆂   \u2B1C")
    sleep(0.05)
    print("5   🅲 🄷 🅴 🅂 🆂   \u2B1C")
    sleep(0.05)
    print("4 \u2B1C  🅼 🄰 🆂 🅃 🅴 🅁  ")
    sleep(0.05)
    spaces_even = 1
    spaces_odd = 0
    for row in range(3):
        print(3-(row), end =" ")
        for cell in range(4):
            print(f"{'  '*(spaces_even%2)}" + "\u2B1C" + f"{'  '*(spaces_odd%2)}", end="")
        print("")
        spaces_even += 1
        spaces_odd += 1
        sleep(0.05)
    input("Press <enter> to start")
STARTING_POSITION = [
    [ b_tower_l, b_knight_l, b_bishop_l, b_queen, b_king, b_bishop_r, b_knight_r, b_tower_r ],
    [ b_pawn_a, b_pawn_b, b_pawn_c, b_pawn_d, b_pawn_e, b_pawn_f, b_pawn_g, b_pawn_h ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  " ],
    [ w_pawn_a, w_pawn_b, w_pawn_c, w_pawn_d, w_pawn_e, w_pawn_f, w_pawn_g, w_pawn_h ],
    [ w_tower_l, w_knight_l, w_bishop_l, w_queen, w_king, w_bishop_r, w_knight_r, w_tower_r ],
]
def read_starting_position_and_write_to_pieces():
    for row in range(len(STARTING_POSITION)):
        for cell in range(len(STARTING_POSITION[row])):
            if type(STARTING_POSITION[row][cell]) == dict:
                board[row][cell] = STARTING_POSITION[row][cell]
                board[row][cell]["position"] = [row, cell]
                active_pieces.append(board[row][cell])
            elif STARTING_POSITION[row][cell] == "  ":
                board[row][cell] = "  "

def draw_board(side: str, message = "", check = None):
    even_odd_counter = 0
    even_odd = ['\x1b[44m', '\x1b[0m']
    print(f"{side.upper()} player, make your move!")
    print("  A B C D E F G H")
    for row in range(8):
        print(8-(row), end = even_odd[1] + " ")
        even_odd_counter += 1
        for cell in range(8):
            if type(board[row][cell]) == dict:
                if check != None:
                    if board[row][cell] == check[0]:
                        print(red_bg + board[row][cell]["image"] + white, end="\033[0m")
                        even_odd_counter += 1
                        continue
                    if board[row][cell] == check[1]:
                        print(red_bg + board[row][cell]["image"] + white, end="\033[0m")
                        even_odd_counter += 1
                        continue
                print(even_odd[even_odd_counter%2] + board[row][cell]["image"], end="\x1b[0m")
            else:
                print(even_odd[even_odd_counter%2] + board[row][cell], end="\x1b[0m")
            even_odd_counter += 1
        if row == 0:
            print("", end = " "*5)
            if len(defeated_pieces) >= 1:
                for piece in defeated_pieces:
                    if piece["side"] == "black":
                        print(piece["image"], end="")
                print()
            else:
                print()
        elif row == 7:
            print("", end = " "*5)
            if len(defeated_pieces) >= 1:
                for piece in defeated_pieces:
                    if piece["side"] == "white":
                        print(piece["image"], end="")
                print()
            else:
                print()
        else:
            print()
    print('\x1b[0m', end="")
    if check:
        check_message = check_text
    else:
        check_message = ""
    print(check_message)
    print(message)

#check check
def check_check():
    for piece in active_pieces:
        for moves in moves_acc_to_rules(piece):
            if board[moves[0]][moves[1]] != "  ":
                if board[moves[0]][moves[1]]["piece"] == "king" and board[moves[0]][moves[1]]["side"] != piece["side"]:
                    return [board[moves[0]][moves[1]], piece]

def save_and_quit(side):
    with open("board.json", "w") as save_board:
        json.dump(board, save_board)
    with open("side.txt", "w") as save_side:
        save_side.write(side)
    with open("defeated.json", "w") as save_defeated:
        json.dump(defeated_pieces, save_defeated)
    print("Saved successfully, shutting down...")
    shutdown[0] = True
    sys.exit()
    

def start_turn(side):
    chosen_piece = None
    target = None
    message = ""
    while chosen_piece == None:
        os.system("cls" if os.name == "nt" else "clear")
        draw_board(side, message, check_check())
        chosen_piece_input = input("Choose piece (examples: a2, e7) or (s)ave and quit: ")
        if chosen_piece_input == "s":
            save_and_quit(side)
        if len(chosen_piece_input) == 2 and chosen_piece_input[0].isalpha() and chosen_piece_input[1].isdecimal():
            if int(chosen_piece_input[1]) > 0 and int(chosen_piece_input[1]) < 9:
                chosen_row = 8 - int(chosen_piece_input[1])
            else:
                message = "Invalid input. Please choose a position between a1 and h8!"
                
                continue
            if chosen_piece_input[0].lower() in "abcdefgh":
                chosen_col = col_map[chosen_piece_input[0].lower()]
            else:
                message = "Invalid input. Please choose a position between a1 and h8!"
                
                continue
        else:
            message = "Invalid input. Please choose a position between a1 and h8!"
            
            continue
        
        if board[chosen_row][chosen_col] == "  ":
            message = f"Invalid input. There is no piece at position {chosen_piece_input[0].upper()}{chosen_piece_input[1]}."
            
            continue
        else:
            if side != board[chosen_row][chosen_col]["side"]:
                message = f"Invalid input. It is {side}'s turn."
                
                continue
            else:
                chosen_piece = board[chosen_row][chosen_col]
####### TARGET ########
    show_moves = True
    target = None
    message = "Press <return> to show possible moves or type 0 to choose another piece"
    possible_targets = moves_acc_to_rules(chosen_piece)
    while target == None:
        if show_moves:
            visualize_moves(possible_targets, chosen_piece)
            sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
        draw_board(side, message, check_check())
        show_moves = False
        piece_name = chosen_piece["piece"]
        print(f"Move {piece_name.upper()} to: ", end="")
        target_input = input()  ############
        if target_input == "":
            show_moves = True
            continue
        elif target_input == "0":
            chosen_piece = None
            start_turn(side)
            break
        elif len(target_input) == 2 and target_input[0].isalpha() and target_input[1].isdecimal():
            if int(target_input[1]) > 0 and int(target_input[1]) < 9:
                chosen_target_row = 8 - int(target_input[1])
            else:
                message = "Invalid input. Please choose a position between a1 and h8!"
                continue
            if target_input[0].lower() in "abcdefgh":
                chosen_target_col = col_map[target_input[0].lower()]
            else:
                message = "Invalid input. Please choose a position between a1 and h8!"
                continue
        else:
            message ="Invalid input. Please choose a position between a1 and h8!"
            continue
        
        for row, col, isEnemy in possible_targets:
            if chosen_target_row == row and chosen_target_col == col:
                target = "OK"
                board[chosen_row][chosen_col] = "  "
                if type(board[chosen_target_row][chosen_target_col]) == dict:
                    defeated_pieces.append(board[chosen_target_row][chosen_target_col])
                    active_pieces.remove(board[chosen_target_row][chosen_target_col])
                board[chosen_target_row][chosen_target_col] = chosen_piece
                chosen_piece["position"][0] = chosen_target_row
                chosen_piece["position"][1] = chosen_target_col
                
                if side == "white":
                    start_turn("black")
                else:
                    start_turn("white")
                break
            
        message = "Invalid target."

def check_for_game():
    try:
        with open("board.json") as load_game:
            game = json.load(load_game)
                    
        with open("side.txt", "r") as load_side:
            side = load_side.read()
        
        with open("defeated.json", "r") as load_defeated:
            defeated = json.load(load_defeated)
        resume = "a"
        while resume != "y" and resume != "n":
            resume = input("Existing game found - do you want to continue? y/n\n> ")
        if resume == "y":
            continue_game(game, side, defeated)
        else:
            new_game()
    except:
        if shutdown[0] == False:
            new_game()
    

def continue_game(game, side, defeated):
    for row in range(len(game)):
            for cell in range(len(game[row])):
                if type(game[row][cell]) == dict:
                    board[row][cell] = game[row][cell]
                    board[row][cell]["position"] = [row, cell]
                    active_pieces.append(board[row][cell])
                elif game[row][cell] == "  ":
                    board[row][cell] = "  "
    for piece in defeated:
        defeated_pieces.append(piece)
    start_turn(side)

def new_game():
    read_starting_position_and_write_to_pieces()
    os.system("cls" if os.name == "nt" else "clear")
    start_turn("white")


draw_intro_board()
check_for_game()