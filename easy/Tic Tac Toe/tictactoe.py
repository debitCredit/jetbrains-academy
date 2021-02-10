import sys


def print_field(l):
    print("""
---------
| {} {} {} |
| {} {} {} |
| {} {} {} |
---------
""".format(*l))


def check_state():
    wins = [cells[:3], cells[3:6], cells[6:], cells[0:9:3], cells[1:9:3], cells[2:9:3], cells[0:9:4], cells[2:7:2]]

    if abs(cells.count("X") - cells.count("O")) > 1 or ("XXX" in wins and "OOO" in wins):
        print("Impossible")
    elif ['X', 'X', 'X'] in wins:
        print_field(cells)
        print("X wins")
        sys.exit()
    elif ['O', 'O', 'O'] in wins:
        print_field(cells)
        print("O wins")
        sys.exit()
    elif cells.count("_") == 0:
        print("Draw")


cells = list("_________")
print_field(cells)
previous_move = "O"
while True:
    if cells.count("_") == 0:
        break
    coordinates = input("Enter the coordinates:").split(" ")
    if not coordinates[0].isdigit() or not coordinates[1].isdigit():
        print("You should enter numbers!")
        continue
    elif int(coordinates[0]) > 3 or int(coordinates[1]) > 3:
        print("Coordinates should be from 1 to 3!")
        continue
    cords_1d = ((int(coordinates[0]) - 1) * 3) + (int(coordinates[1]) - 1)
    if cells[cords_1d] != "_":
        print("This cell is occupied! Choose another one!")
    else:
        if previous_move == "X":
            cells[cords_1d] = "O"
            previous_move = "O"
            check_state()
        else:
            cells[cords_1d] = "X"
            previous_move = "X"
            check_state()
        print_field(cells)
        check_state()
