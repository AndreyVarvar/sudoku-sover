from interaction_stuff import *
import pygame as pg

# file contains mainly drawing and displaying functions

pg.init()

DISPLAY = pg.display.set_mode((WIDTH, HEIGHT))  # main display ~ decided to put it here, because its mainly for display purposes
pg.display.set_caption("SUDOKU SOLVER 2.0")

eraser_image = pg.image.load("sprites/eraser.png").convert_alpha()


def initialize_buttons_plus_switch():  # i had to do something with always creating a new class object, so i created 1, and use it continuously
    global choose_buttons, color_buttons, candidate_to_guessing_switch

    choose_buttons = [Button((235, 220), "You solve", "l", button_width=250),
                      Button((235, 300), "Computer solve", "l", button_width=250),
                      Button((235, 380), "Back", "l", button_width=250)]

    color_buttons = [Button((100, 200), "", "s", color=LIGHT_YELLOW, button_width=50),
                     Button((100, 260), "", "s", color=LIGHT_GREEN, button_width=50),
                     Button((160, 200), "", "s", color=LIGHT_BLUE, button_width=50),
                     Button((160, 260), "", "s", color=LIGHT_RED, button_width=50),
                     Button((220, 230), "", "s", color=WHITE, button_width=50, image=eraser_image)]

    candidate_to_guessing_switch = Switch((861, 100), "number", "candidate", "s")


def display_text(surface, text, pos, color, size, font_n):
    """
    draws text on the screen

    :param surface: ...
    :param text: ...
    :param pos: ...
    :param color: ...
    :param size: size of the text, "s", "m", "l", "xl"
    :param font_n: type of font: 1 or 2
    :return: nothing
    """
    font = get_font(font_n, size)

    text = font.render(text, True, color)  # convert text into a surface object

    text_rect = text.get_rect()  # get bounds of the surface object

    text_rect.center = pos  # set its position, so that its center is at coordinates "pos"

    surface.blit(text, text_rect)  # blit it on "surface"


def draw_board(pos, puzzle, invalid_pos=None, hints_pos=None, highlighted_cells=None, candidate_list=None):
    """
    draws the board on the screen

    :param pos: where to draw the board on the DISPLAY surface
    :param puzzle: the sudoku puzzle ~ the array
    :param invalid_pos: array of invalid hints position - they are gonna be highlighted with red color
    :param hints_pos: hints position in the array - to know which font to use for different type of numbers
    :param highlighted_cells: highlighters!
    :param candidate_list: see draw_numbers_on_board() (lower)
    :return: returns nothing, but instead draws the board on the given pos
    """

    if highlighted_cells is None:
        highlighted_cells = []

    board = pg.Surface((450, 450))  # b o a r d
    board.fill((250, 250, 250))  # f i l l   b o a r d

    for i in range(9):  # f o r   l o o p   o n   9   l o o p s
        for j in range(9):  # a n o t h e r   f o r   l o o p   o n   9   l o o p s
            rect_pos = (CELL_WIDTH * ((j % 3) + (3 * (i % 3))), CELL_WIDTH * ((j // 3) + (3 * (i // 3))))  # l e g e n d a r y   m a t h   t h a t   i m   t o o   l a z y   t o   e x p l a i n
            cell_pos = ((i % 3) * 3 + (j % 3), (i // 3) * 3 + (j // 3))

            highlighted_cells_pos = [elem[0] for elem in highlighted_cells]
            if cell_pos in highlighted_cells_pos:  # elements in highlighted_cells list are a bit different: instead of just the position, each element also has a "color" value, so we nee to somehow work around that
                # this basically checks, if the cell_pos is is the list of highlighted_cells

                highlight_color = highlighted_cells[highlighted_cells_pos.index(cell_pos)][1]  # on index 1 we have the color of the cell

                pg.draw.rect(board, highlight_color, (rect_pos[0], rect_pos[1], CELL_WIDTH, CELL_WIDTH))

            pg.draw.rect(board, (0, 0, 0), (rect_pos, (CELL_WIDTH, CELL_WIDTH)), 1)  # d r a w   e v e n   s m a l l e r   r e c t a n g l e


        pg.draw.rect(board, (0, 0, 0), (CELL_WIDTH * 3 * (i % 3), CELL_WIDTH * 3 * (i // 3), CELL_WIDTH * 3, CELL_WIDTH * 3), 2)  # d r a w   a   s m a l l e r   r e c t a n g l e

    pg.draw.rect(board, (0, 0, 0), (0, 0, 450, 450), 4)  # d r a w   a   r e c t a n g l e

    board = draw_numbers_on_board(puzzle, board, invalid_pos, hints_pos, candidate_list)  # d r a w   n u m b e r s   o n   b o a r d

    DISPLAY.blit(board, pos)  # d r a w   b o a r d


def draw_numbers_on_board(puzzle, board, invalid_pos=None, hints_pos=None, candidate_list=None):
    """
    draws the hints and user guesses on the board

    :param puzzle: sudoku~ see function higher
    :param board: surface, on which we draw the numbers
    :param invalid_pos: to highlight the invalid placed numbers
    :param hints_pos: to display with different font what the user is guessing and the hints position
    :param candidate_list: to display the candidates of the cells, that the player placed on
    :return: returns board surface with numbers on it displayed
    """

    if invalid_pos is None:
        invalid_pos = []

    if hints_pos is None:
        hints_pos = []

    if candidate_list is None:
        candidate_list = []

    for row_counter, row in enumerate(puzzle):
        for line_counter, line in enumerate(row):
            for cell_counter, cell_value in enumerate(line):
                if cell_value != 0:  # don't display number 0, since its an "empty" cell
                    cell_pos = (row_counter, line_counter, cell_counter)
                    number_pos = ((line_counter * 3 + cell_counter) * CELL_WIDTH + HALF_CELL_WIDTH, (
                            row_counter * CELL_WIDTH) + HALF_CELL_WIDTH)  # get the position of the number to display on

                    if cell_pos in invalid_pos:
                        color = RED
                    else:
                        color = BLACK

                    if len(hints_pos) > 0:
                        if cell_pos in hints_pos:
                            font_type = 1
                        else:
                            font_type = 2
                    else:  # we are still in the edit state, because ist the only state where the hints_pos list is empty
                        font_type = 1
                    display_text(board, str(cell_value), number_pos, color, "xl", font_type)

    for row_counter, row in enumerate(candidate_list):
        for cell_counter, candidates in enumerate(row):
            for candidate_counter, candidate in enumerate(candidates):
                cell_pos = (CELL_WIDTH * cell_counter, CELL_WIDTH * row_counter)

                candidate_list = ((9 + ((candidate - 1) % 3) * 15) + cell_pos[0],
                                 (8 + ((candidate - 1) // 3) * 15) + cell_pos[1])  # the CENTER, not the top-left corner

                display_text(board, str(candidate), candidate_list, BLACK, "vs", 1)

    return board


def edit_state_hints_display(board_is_valid, board_has_more_than_7_hints, selected_n, hint_count, show_error_message):
    """
    display continuing hints, as well som other stuff for editing the sudoku puzzle

    :param board_is_valid: boolean~ for continuing hints
    :param board_has_more_than_7_hints: boolean~ also for continuing hints
    :param selected_n: currently selected number to fill in
    :param hint_count: how many numbers you've placed
    :param show_error_message: to show or not to show? what the user has done wrong?
    :return: return nothing
    """
    display_text(DISPLAY, "Press num keys to select numbers.", (765, 100), BLACK, "m", 1)
    display_text(DISPLAY, f"Selected number: {selected_n if selected_n != 0 else 'eraser'}", (765, 140), BLACK, "m", 1)

    display_text(DISPLAY, f"Click on any cell to {'fill' if selected_n != 0 else 'erase'} it.", (765, 200), BLACK, "m", 1)

    if not show_error_message:
        pass  # casually ignore the rest ~ don't show anything to the user, when he tries to press "enter", the error message will appear and tell him what he needs to fix
    elif board_is_valid is False:
        color = RED
        display_text(DISPLAY, "No continue, cuz duplicates >:(", (765, 250), color, "l", 1)
        display_text(DISPLAY, "(sudoku cannot contain duplicates)", (765, 280), color, "s", 1)
    elif board_is_valid and board_has_more_than_7_hints is False:
        color = ORANGE
        display_text(DISPLAY, "Put more hints, c'mon", (765, 250), color, "l", 1)
        display_text(DISPLAY, "(sudoku must contain at least 8 hints)", (765, 280), color, "s", 1)
        display_text(DISPLAY, f"You currently have {hint_count} hint{'s' if hint_count != 1 else ''}", (765, 310), color, "s", 1)


    display_text(DISPLAY, "Press 'enter' when you are done!", (765, 350), GREEN, "l", 1)


def choosing_state_hints_display_and_button_stuff_idk():
    """
    draws buttons: user_solve and computer_solve, which user can press and be redirected to corresponding states

    :return: the button output
    """
    display_text(DISPLAY, "Choose one of the methods below:", (235, 150), BLACK, "m", 1)

    button_output = [0, 0, 0]

    for button_counter, button in enumerate(choose_buttons):
        mouse_pos = pg.mouse.get_pos()
        button.draw(DISPLAY, mouse_pos)

        output = button.action_if_press(mouse_pos, pg.mouse.get_pressed()[0])

        button_output[button_counter] = output

    return button_output


def user_solving_state_gui(selected_n, selected_color):
    """
    display user_solving state corresponding stuff, like highlighters and buttons and stuff

    :param selected_n: currently selected key
    :param selected_color: for highlighters
    :return: button output
    """
    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed()[0]

    display_text(DISPLAY, f"selected key: {selected_n if selected_n != 0 else 'eraser'}", (138, 100), BLACK, "m", 1)


    # --------------------HIGHLIGHTERS--------------------
    display_text(DISPLAY, "highlighters!", (138, 150), BLACK, "m", 1)

    display_text(DISPLAY, "press buttons to select", (138, 310), BLACK, "m", 1)
    display_text(DISPLAY, "press 'backspace' to deselect", (138, 350), BLACK, "s", 1)

    button_output = [0 for _ in range(len(color_buttons))]

    pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
    for button_counter, button in enumerate(color_buttons):
        button.draw(DISPLAY, mouse_pos)

        output = button.action_if_press(mouse_pos, mouse_pressed)

        button_output[button_counter] = output

    if selected_color is not None:  # i draw it at the end, to display it over everything else
        darker_color = (selected_color[0] - 30, selected_color[1] - 30, selected_color[2] - 30)
        pg.draw.circle(DISPLAY, darker_color, mouse_pos, 15)  # to show which color you selected

    # ---------------CANDIDATE-FILLING----------------
    candidate_to_guessing_switch.draw(DISPLAY, mouse_pos)
    candidate_to_guessing_switch.action_if_press(mouse_pos, mouse_pressed)

    switch_output = candidate_to_guessing_switch.switch_state


    return button_output, switch_output

