import math
import copy
import numpy as np

"""
This part of the code was made by 'the ernis#9639' 
"""

# empty sudoku
empty_sudoku = [[], [], [], [], [], [], [], [], []]
for a in range(9):
    empty_sudoku[a] = [[], [], []]
    for b in range(3):
        empty_sudoku[a][b] = [0, 0, 0]
# sudoku for changing
work_sudoku = copy.deepcopy(empty_sudoku)
# output to show
output_sudoku = copy.deepcopy(work_sudoku)

# values to keep track of possible positions to place for each digit (track_list[0] is for 1s, track_list[1] is for 2s...)
track_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
track_list[0] = [[], [], [], [], [], [], [], [], []]
track_list[1] = [[], [], [], [], [], [], [], [], []]
track_list[2] = [[], [], [], [], [], [], [], [], []]
track_list[3] = [[], [], [], [], [], [], [], [], []]
track_list[4] = [[], [], [], [], [], [], [], [], []]
track_list[5] = [[], [], [], [], [], [], [], [], []]
track_list[6] = [[], [], [], [], [], [], [], [], []]
track_list[7] = [[], [], [], [], [], [], [], [], []]
track_list[8] = [[], [], [], [], [], [], [], [], []]


# resets values used for tracking possible placement places
def reset_checks():
    global track_list

    for a in range(9):
        track_list[0][a] = [[], [], []]
        for b in range(3):
            track_list[0][a][b] = [1, 1, 1]
    for a in range(9):
        track_list[1][a] = [[], [], []]
        for b in range(3):
            track_list[1][a][b] = [2, 2, 2]
    for a in range(9):
        track_list[2][a] = [[], [], []]
        for b in range(3):
            track_list[2][a][b] = [3, 3, 3]
    for a in range(9):
        track_list[3][a] = [[], [], []]
        for b in range(3):
            track_list[3][a][b] = [4, 4, 4]
    for a in range(9):
        track_list[4][a] = [[], [], []]
        for b in range(3):
            track_list[4][a][b] = [5, 5, 5]
    for a in range(9):
        track_list[5][a] = [[], [], []]
        for b in range(3):
            track_list[5][a][b] = [6, 6, 6]
    for a in range(9):
        track_list[6][a] = [[], [], []]
        for b in range(3):
            track_list[6][a][b] = [7, 7, 7]
    for a in range(9):
        track_list[7][a] = [[], [], []]
        for b in range(3):
            track_list[7][a][b] = [8, 8, 8]
    for a in range(9):
        track_list[8][a] = [[], [], []]
        for b in range(3):
            track_list[8][a][b] = [9, 9, 9]


# prints ssudoku in a readable format
def print_sudoku(list):
    string = ""
    for a in range(9):
        string += "\n"
        if a % 3 == 0 and a != 0:
            string += " - - - + - - - + - - -\n"
        for b in range(3):
            if b != 0:
                string += " |"
            for c in range(3):
                string += " " + str(list[a][b][c])
    print(string)
    print()


# goes trough each row to check if there is possibility to place specific number
def clear_row(list, num):
    for a in range(9):
        clear = False
        for b in range(3):
            for c in range(3):
                if work_sudoku[a][b][c] == num:
                    clear = True
                    break
            if clear:
                break

        if clear:
            for b in range(3):
                for c in range(3):
                    list[a][b][c] = 0

    return list


# goes trough each column to check if there is possibility to place specific number
def clear_column(list, num):
    for a in range(3):
        for b in range(3):
            clear = False
            for c in range(9):
                if work_sudoku[c][a][b] == num:
                    clear = True
                    break

            if clear:
                for c in range(9):
                    list[c][a][b] = 0

    return list


# goes trough each cell to check if there is possibility to place specific number
def clear_cell(list, num):
    for a in range(9):
        clear = False
        for b in range(9):
            if work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == num:
                clear = True
                break

        if clear:
            for b in range(9):
                list[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 0

    return list


# goes trough each square to check if there is possibility to place specific number
def clear_digit(list):
    for a in range(9):
        for b in range(3):
            for c in range(3):
                if work_sudoku[a][b][c] != 0:
                    list[a][b][c] = 0

    return list


# checks for every placement condition
def clear(list, num):
    return clear_row(clear_column(clear_cell(clear_digit(list), num), num), num)


# checks for every number for every placement condition
def check_all():
    global track_list
    track_list[0] = clear(track_list[0], 1)
    track_list[1] = clear(track_list[1], 2)
    track_list[2] = clear(track_list[2], 3)
    track_list[3] = clear(track_list[3], 4)
    track_list[4] = clear(track_list[4], 5)
    track_list[5] = clear(track_list[5], 6)
    track_list[6] = clear(track_list[6], 7)
    track_list[7] = clear(track_list[7], 8)
    track_list[8] = clear(track_list[8], 9)


# checks for rows with one empty spot and fills it
def fill_row():
    global work_sudoku
    for a in range(9):
        b1 = 0
        b2 = 0
        b3 = 0
        b4 = 0
        b5 = 0
        b6 = 0
        b7 = 0
        b8 = 0
        b9 = 0
        for b in range(3):
            for c in range(3):
                if track_list[0][a][b][c] == 1:
                    b1 += 1
                if track_list[1][a][b][c] == 2:
                    b2 += 1
                if track_list[2][a][b][c] == 3:
                    b3 += 1
                if track_list[3][a][b][c] == 4:
                    b4 += 1
                if track_list[4][a][b][c] == 5:
                    b5 += 1
                if track_list[5][a][b][c] == 6:
                    b6 += 1
                if track_list[6][a][b][c] == 7:
                    b7 += 1
                if track_list[7][a][b][c] == 8:
                    b8 += 1
                if track_list[8][a][b][c] == 9:
                    b9 += 1

        for b in range(3):
            for c in range(3):
                if track_list[0][a][b][c] == 1 and b1 == 1:
                    work_sudoku[a][b][c] = 1
                if track_list[1][a][b][c] == 2 and b2 == 1:
                    work_sudoku[a][b][c] = 2
                if track_list[2][a][b][c] == 3 and b3 == 1:
                    work_sudoku[a][b][c] = 3
                if track_list[3][a][b][c] == 4 and b4 == 1:
                    work_sudoku[a][b][c] = 4
                if track_list[4][a][b][c] == 5 and b5 == 1:
                    work_sudoku[a][b][c] = 5
                if track_list[5][a][b][c] == 6 and b6 == 1:
                    work_sudoku[a][b][c] = 6
                if track_list[6][a][b][c] == 7 and b7 == 1:
                    work_sudoku[a][b][c] = 7
                if track_list[7][a][b][c] == 8 and b8 == 1:
                    work_sudoku[a][b][c] = 8
                if track_list[8][a][b][c] == 9 and b9 == 1:
                    work_sudoku[a][b][c] = 9


# checks for columns with one empty spot and fills it
def fill_column():
    global work_sudoku
    for a in range(3):
        for b in range(3):
            b1 = 0
            b2 = 0
            b3 = 0
            b4 = 0
            b5 = 0
            b6 = 0
            b7 = 0
            b8 = 0
            b9 = 0
            for c in range(9):
                if track_list[0][c][a][b] == 1:
                    b1 += 1
                if track_list[1][c][a][b] == 2:
                    b2 += 1
                if track_list[2][c][a][b] == 3:
                    b3 += 1
                if track_list[3][c][a][b] == 4:
                    b4 += 1
                if track_list[4][c][a][b] == 5:
                    b5 += 1
                if track_list[5][c][a][b] == 6:
                    b6 += 1
                if track_list[6][c][a][b] == 7:
                    b7 += 1
                if track_list[7][c][a][b] == 8:
                    b8 += 1
                if track_list[8][c][a][b] == 9:
                    b9 += 1

            for c in range(9):
                if track_list[0][c][a][b] == 1 and b1 == 1:
                    work_sudoku[c][a][b] = 1
                if track_list[1][c][a][b] == 2 and b2 == 1:
                    work_sudoku[c][a][b] = 2
                if track_list[2][c][a][b] == 3 and b3 == 1:
                    work_sudoku[c][a][b] = 3
                if track_list[3][c][a][b] == 4 and b4 == 1:
                    work_sudoku[c][a][b] = 4
                if track_list[4][c][a][b] == 5 and b5 == 1:
                    work_sudoku[c][a][b] = 5
                if track_list[5][c][a][b] == 6 and b6 == 1:
                    work_sudoku[c][a][b] = 6
                if track_list[6][c][a][b] == 7 and b7 == 1:
                    work_sudoku[c][a][b] = 7
                if track_list[7][c][a][b] == 8 and b8 == 1:
                    work_sudoku[c][a][b] = 8
                if track_list[8][c][a][b] == 9 and b9 == 1:
                    work_sudoku[c][a][b] = 9


# check for cells with one empty spot and fills it
def fill_cell():
    for a in range(9):
        b1 = 0
        b2 = 0
        b3 = 0
        b4 = 0
        b5 = 0
        b6 = 0
        b7 = 0
        b8 = 0
        b9 = 0
        for b in range(9):
            if track_list[0][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1:
                b1 += 1
            if track_list[1][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 2:
                b2 += 1
            if track_list[2][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 3:
                b3 += 1
            if track_list[3][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 4:
                b4 += 1
            if track_list[4][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 5:
                b5 += 1
            if track_list[5][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 6:
                b6 += 1
            if track_list[6][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 7:
                b7 += 1
            if track_list[7][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 8:
                b8 += 1
            if track_list[8][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 9:
                b9 += 1

        for b in range(9):
            if track_list[0][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1 and b1 == 1:
                work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 1
            if track_list[1][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1 and b2 == 1:
                work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 2
            if track_list[2][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1 and b3 == 1:
                work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 3
            if track_list[3][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1 and b4 == 1:
                work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 4
            if track_list[4][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1 and b5 == 1:
                work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 5
            if track_list[5][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1 and b6 == 1:
                work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 6
            if track_list[6][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1 and b7 == 1:
                work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 7
            if track_list[7][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1 and b8 == 1:
                work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 8
            if track_list[8][math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] == 1 and b9 == 1:
                work_sudoku[math.floor(a / 3) * 3 + math.floor(b / 3)][a % 3][b % 3] = 9


# goes trough possible positions and if only one number can be placed places it
def fill_digit():
    global work_sudoku
    for a in range(9):
        for b in range(3):
            for c in range(3):
                if work_sudoku[a][b][c] == 0:
                    if (track_list[0][a][b][c] != 0) + (track_list[1][a][b][c] != 0) + (track_list[2][a][b][c] != 0) + (
                            track_list[3][a][b][c] != 0) + (track_list[4][a][b][c] != 0) + (
                            track_list[5][a][b][c] != 0) + (track_list[6][a][b][c] != 0) + (
                            track_list[7][a][b][c] != 0) + (track_list[8][a][b][c] != 0) == 1:
                        work_sudoku[a][b][c] = track_list[0][a][b][c] + track_list[1][a][b][c] + track_list[2][a][b][
                            c] + track_list[3][a][b][c] + track_list[4][a][b][c] + track_list[5][a][b][c] + \
                                               track_list[6][a][b][c] + track_list[7][a][b][c] + track_list[8][a][b][c]


# fills all possible spots
def fill():
    fill_row()
    fill_column()
    fill_cell()
    fill_digit()


# tries to solve without brute forcing it
def solve():
    reset_checks()
    while True:
        global output_sudoku

        check_all()
        fill()

        # if it is unable to solve further breaks out of solving loop
        if np.array_equal(np.array(work_sudoku), np.array(output_sudoku)):
            break
        output_sudoku = copy.deepcopy(work_sudoku)


# checks one row, column and cell for duplicate numbers
def verify(list, iteration):
    for num in range(9):
        # checks in a row
        n = 0
        for a in range(9):
            if list[math.floor(iteration / 9)][math.floor(a / 3)][a % 3] == num + 1:
                n += 1

            if n > 1:
                return False

        # checks in a column
        n = 0
        for a in range(9):
            if list[a][math.floor(iteration % 9 / 3)][iteration % 9 % 3] == num + 1:
                n += 1

            if n > 1:
                return False

        # checks in a cell
        n = 0
        for a in range(9):
            if list[(math.floor(iteration / 9) - math.floor(iteration / 9) % 3) + math.floor(a / 3)][
                math.floor(iteration % 9 / 3)][a % 3] == num + 1:
                n += 1

            if n > 1:
                return False
    return True


# bruteforces using recursion
def recursion_check(checklist, worklist, iteration):
    progresslist = []
    # stops recursion
    if iteration < 81:
        # checks if it already has a number in specified spot
        if checklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] == 0:
            # if it does not have have a number loops trough all possible numbers
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = 1
            if track_list[0][math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][
                iteration % 9 % 3] != 0 and verify(worklist, iteration):
                progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = 2
            if track_list[1][math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][
                iteration % 9 % 3] != 0 and verify(worklist, iteration):
                progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = 3
            if track_list[2][math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][
                iteration % 9 % 3] != 0 and verify(worklist, iteration):
                progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = 4
            if track_list[3][math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][
                iteration % 9 % 3] != 0 and verify(worklist, iteration):
                progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = 5
            if track_list[4][math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][
                iteration % 9 % 3] != 0 and verify(worklist, iteration):
                progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = 6
            if track_list[5][math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][
                iteration % 9 % 3] != 0 and verify(worklist, iteration):
                progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = 7
            if track_list[6][math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][
                iteration % 9 % 3] != 0 and verify(worklist, iteration):
                progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = 8
            if track_list[7][math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][
                iteration % 9 % 3] != 0 and verify(worklist, iteration):
                progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = 9
            if track_list[8][math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][
                iteration % 9 % 3] != 0 and verify(worklist, iteration):
                progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
        else:
            worklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3] = \
            checklist[math.floor(iteration / 9)][math.floor(iteration % 9 / 3)][iteration % 9 % 3]
            progresslist += recursion_check(checklist, copy.deepcopy(worklist), iteration + 1)
    else:
        progresslist.append(copy.deepcopy(worklist))
    # returns all found solves
    return progresslist


# tries to solve using brute forcing
def brute_force():
    reset_checks()
    check_all()
    global work_sudoku
    global output_sudoku
    possible_solves = recursion_check(work_sudoku, copy.deepcopy(empty_sudoku), 0)

    if len(possible_solves) == 0:
        print("cant solve it")
        return
    output_sudoku = copy.deepcopy(possible_solves[0])
