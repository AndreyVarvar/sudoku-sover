import copy
from displaying_stuff import *
from calculator import *
import pygame as pg
import sudoku_solver
# this file is a bridge between all files. basically where everything is connected together

initialize_buttons_plus_switch()


the_sudoku_my_solver_MUST_solve = [[[6, 0, 0], [0, 0, 9], [0, 0, 0]],  # its a long history
                                   [[0, 0, 0], [0, 0, 0], [0, 0, 4]],  # it was the first one i chose, and yes, my solver couldn't solve it
                                   [[0, 0, 7], [6, 4, 8], [0, 0, 2]],  # so then i said 'my solver MUST solve this one, or im gonna be unsatisfied'
                                   [[0, 0, 2], [0, 5, 0], [8, 0, 0]],
                                   [[0, 0, 1], [8, 0, 0], [0, 2, 3]],
                                   [[7, 0, 4], [0, 0, 0], [0, 0, 0]],
                                   [[0, 0, 0], [3, 0, 0], [0, 4, 0]],
                                   [[0, 0, 0], [0, 6, 0], [5, 0, 0]],
                                   [[0, 2, 3], [0, 1, 0], [0, 0, 0]]]


if __name__ == '__main__':
    clock = pg.time.Clock()

    # puzzle = np.array([[[0, 0, 0] for _ in range(3)] for _ in range(9)])  # set puzzle

    puzzle = np.copy(the_sudoku_my_solver_MUST_solve)

    board_edit_state = "board edit"
    choosing_state = "choosing mode"
    user_soling_state = "user solves the puzzle"  # user is using their brains currently
    computer_solving_state = "computer solves the puzzle"  # lame, i knew user was weak and not smart (if you are seeing this, sorry dear user)

    current_state = board_edit_state  # current state is the most boring state of them all

    selected_n = 1  # initial selected number. selected_n - selected number. duh

    invalid_num_positions = None  # pre-initializing, to prevent errors and to make it global (kinda)
    board_is_valid = True  # this one too, like one line above
    hint_count = 0  # keep track of how many hints you placed
    board_has_more_than_7_hints = False  # 0_o ~ same thing as above
    fill_cell = False  # when the mouse is pressed, this becomes True, and the cell is filled. Easy :)

    selected_highlighter = None  # for user_solve state, for cell highlighting. thought it will be useful
    highlighted_cells_position = []  # for displaying highlighted cells

    show_error_message = False  # to tell the user, what is wrong in their sudoku

    candidate_list = [[[] for _ in range(9)] for _ in range(9)]  # to handle candidate filling
    candidate_fill = False

    sudoku_solved = False  # for computer solving
    attempted_to_solve = False  # also for computer solving


    hints_pos = None

    ex = False  # ex - exit. if true, program terminates
    while not ex:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ex = True

            if event.type == pg.KEYDOWN:
                if not pg.mouse.get_pressed()[0]:
                    if 48 <= event.key <= 57:
                        selected_n = event.key - 48  # number 1 on the keyboard has index 49, so in order to get the selected key, we need to subtract 48 from the key index (cuz subtracting 49 will give us 0 as a first element, not 1)
                        selected_highlighter = None

                if event.key == pg.K_RETURN:
                    if board_is_valid and board_has_more_than_7_hints and current_state == board_edit_state:
                        current_state = choosing_state
                        selected_n = 0
                    else:
                        show_error_message = True

                elif event.key == pg.K_BACKSPACE:
                    selected_highlighter = None


            if event.type == pg.MOUSEBUTTONDOWN:
                fill_cell = True
            else:
                fill_cell = False

        DISPLAY.fill(WHITE)

        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)


        if current_state == board_edit_state:  # do stuff depending on which state user is currently in
            board_x = 75
            board_rect = pg.Rect((board_x, 75, 450, 450))  # since its board edit state, board has this rect
            draw_board((board_x, 75), puzzle, invalid_num_positions)

            if fill_cell:  # cell filling
                show_error_message = False
                mouse_pos = pg.mouse.get_pos()

                if board_rect.collidepoint(mouse_pos[0], mouse_pos[1]):  # to know which cell we hit, cursor has to be inside the rect
                    cell_pressed = ((mouse_pos[0] - 75) // CELL_WIDTH, (mouse_pos[1] - 75) // CELL_WIDTH)  # confusing math
                    cell_index_in_puzzle = (cell_pressed[1], cell_pressed[0] // 3, cell_pressed[0] % 3)  # get its position

                    if puzzle[cell_index_in_puzzle] != selected_n:  # this is to prevent checking board validity every frame
                        puzzle[cell_index_in_puzzle] = selected_n

                        invalid_num_positions = get_invalid_nums_pos(puzzle)

                        board_is_valid = len(invalid_num_positions) == 0  # either true or false. duh

                        hint_count = 9**2 - np.count_nonzero(puzzle == 0)
                        board_has_more_than_7_hints = hint_count > 7  # its mathematically impossible for a sudoku with less than 7 hints to have only 1 solution

            edit_state_hints_display(board_is_valid, board_has_more_than_7_hints, selected_n, hint_count, show_error_message)  # display words that are relevant to this state


        elif current_state == choosing_state:  # very little calculations happen here, so not very much in here
            board_x = WIDTH - BOARD_WIDTH - 75
            draw_board((board_x, 75), puzzle)

            state_output = choosing_state_hints_display_and_button_stuff_idk()  # that function outputs the buttons output. a little confusing, but not very much

            state_output_decoder = {0: user_soling_state,
                                    1: computer_solving_state,
                                    2: board_edit_state}  # output is written in a mystical language, so we need a decoder for "current_state"

            if 1 in state_output:  # one of the buttons was pressed
                current_state = state_output_decoder[state_output.index(1)]


        elif current_state == user_soling_state:
            board_x = WIDTH//2 - BOARD_WIDTH//2
            board_rect = pg.Rect((board_x, 75, 450, 450))  # since its user_solve state, board has this rect
            draw_board((board_x, 75),  # center the board
                       puzzle, invalid_num_positions, hints_pos, highlighted_cells=highlighted_cells_position,
                       candidate_list=candidate_list)

            if hints_pos is None:  # to prevent constant looping and making every user-inputted value a "hint" value
                hints_pos = get_hints_positions(puzzle)  # since we did not edit the puzzle array, we can assign every value in it (non 0 values) as a hint numbers

            # yeah, i just copied this from the edit_state one, but i edited it. I know, im lazy :P. work smarter - not harder
            if fill_cell:  # cell filling
                fill_cell = False
                mouse_pos = pg.mouse.get_pos()

                if board_rect.collidepoint(mouse_pos[0], mouse_pos[1]):  # to know which cell we hit, cursor has to be inside this rect

                    cell_pressed = ((mouse_pos[0] - board_x) // CELL_WIDTH,
                                    (mouse_pos[1] - 75) // CELL_WIDTH)  # confusing math, get the pressed cell pos
                    cell_index_in_puzzle = (cell_pressed[1], cell_pressed[0] // 3, cell_pressed[0] % 3)  # get its position

                    if selected_highlighter is not None:  # if we have a highlighter selected, then highlight a cell! ez
                        if selected_highlighter != ERASING_COLOR:
                            if cell_pressed in [elem[0] for elem in highlighted_cells_position]:
                                highlighted_cells_position[[elem[0] for elem in highlighted_cells_position].index(cell_pressed)] = (cell_pressed, selected_highlighter)  # finally, some spaghetti. SO, this code finds the duplicate position values in the highlighter list, and replaces the position with different color
                            else:
                                highlighted_cells_position.append((cell_pressed, selected_highlighter))

                            highlighted_cells_position = list(set(highlighted_cells_position))  # remove duplicates

                        else:
                            if cell_pressed in [elem[0] for elem in highlighted_cells_position]:
                                highlighted_cells_position.pop([elem[0] for elem in highlighted_cells_position].index(cell_pressed))


                    elif candidate_fill:
                        cell_index_pos = (cell_index_in_puzzle[0], cell_index_in_puzzle[1] * 3 + cell_index_in_puzzle[2])

                        if selected_n != 0:  # we cant have a 0 as a candidate, am i right?
                            if selected_n in candidate_list[cell_index_pos[0]][cell_index_pos[1]]:
                                candidate_list[cell_index_pos[0]][cell_index_pos[1]].remove(selected_n)
                            else:
                                candidate_list[cell_index_pos[0]][cell_index_pos[1]].append(selected_n)
                        else:
                            candidate_list[cell_index_pos[0]][cell_index_pos[1]] = []  # we have 0 selected, or eraser. So we remove every single candidate from that cell


                    else:
                        if puzzle[cell_index_in_puzzle] != selected_n and cell_index_in_puzzle not in hints_pos:  # 1st condition) this is to prevent checking board validity every frame, 2nd condition) to not fill the hint number (you should NOT do this)
                            puzzle[cell_index_in_puzzle] = selected_n

                            invalid_num_positions = get_invalid_nums_pos(puzzle)
                else:
                    selected_highlighter = None

                candidate_list = remove_overlapping_values(candidate_list, puzzle)  # make sure the player DOESNT BREAK THE RULES, which they usually do


            color_output, switch_state = user_solving_state_gui(selected_n, selected_highlighter)  # display words that are relevant to this state

            color_output_decoder = {0: LIGHT_YELLOW,  # the output is a list of 0-os and probably a 1, and this 1 indicates that the button is pressed. So, to get the button pressed, we take the index of the 1 in the list, and we can find the color of that button
                                    1: LIGHT_GREEN,
                                    2: LIGHT_BLUE,
                                    3: LIGHT_RED,
                                    4: ERASING_COLOR}

            if 1 in color_output:
                selected_highlighter = color_output_decoder[color_output.index(1)]

            if switch_state:  # if 1 - True, if 0 - False
                candidate_fill = True  # doing this, because i don't want candidate_fill to become an integer
            else:
                candidate_fill = False

        elif current_state == computer_solving_state:
            if sudoku_solved is False and not attempted_to_solve:
                attempted_to_solve = True
                display_text(DISPLAY, "We ask you to wait a few seconds", (500, 300), BLACK, "xl", 1)
                pg.display.update()

                sudoku_solver.work_sudoku = puzzle
                sudoku_solver.solve()
                sudoku_solver.brute_force()
                puzzle = copy.deepcopy(sudoku_solver.output_sudoku)
                sudoku_solved = check_sudoku_solved(puzzle)

            else:
                hints_pos = get_hints_positions(puzzle)

                board_x = WIDTH // 2 - BOARD_WIDTH // 2
                board_rect = pg.Rect((board_x, 75, 450, 450))  # since its computer_solve state, board has this rect
                draw_board((board_x, 75),  # center the board
                           puzzle, invalid_num_positions, hints_pos, highlighted_cells=highlighted_cells_position,
                           candidate_list=candidate_list)



        clock.tick(100)
        display_text(DISPLAY, "SUDOKU SOLVER 2.0", (500, 40), BLACK, "xl", 1)
        display_text(DISPLAY, f"fps: {round(clock.get_fps())}", (50, 50), (52, 154, 227), "m", 1)

        pg.display.update()
