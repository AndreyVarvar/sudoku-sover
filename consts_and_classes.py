import pygame as pg
pg.init()

WIDTH, HEIGHT = 1000, 600
CELL_WIDTH = 50
HALF_CELL_WIDTH = 25
BOARD_WIDTH = CELL_WIDTH * 9

WHITE = (250, 250, 250)
ERASING_COLOR = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (222, 11, 44)
GREEN = (120, 186, 6)
ORANGE = (237, 115, 0)
LIGHT_RED = (250, 112, 112)
LIGHT_GREEN = (112, 250, 112)
LIGHT_BLUE = (112, 250, 250)
LIGHT_YELLOW = (250, 250, 112)

font1_size15 = pg.font.SysFont("ヒラキノ明朝pron", 15)
font1_size20 = pg.font.SysFont("ヒラキノ明朝pron", 20)
font1_size25 = pg.font.SysFont("ヒラキノ明朝pron", 25)
font1_size30 = pg.font.SysFont("ヒラキノ明朝pron", 30)
font1_size40 = pg.font.SysFont("ヒラキノ明朝pron", 40)
font2_size80 = pg.font.SysFont("waseem", 80)


def get_font(font, size):  # its used project-wide
    """
    based on the data inputted, return the corresponding font

    :param font: font type: 1 or 2
    :param size: ...
    :return: font variable
    """
    if font == 1:  # font type 1
        if size == "vs":  # vs - very small - yes, i am very creative
            return font1_size15
        elif size == "s":  # s - small
            return font1_size20
        elif size == "m":  # m - medium
            return font1_size25
        elif size == "l":  # l - large
            return font1_size30
        elif size == "xl":  # xl - extra large i think
            return font1_size40
        else:  # for debugging
            raise ValueError

    elif font == 2:
        if size == "xl":
            return font2_size80
        else:
            raise ValueError  # also for debugging
    else:
        raise ValueError  # also for debugging
