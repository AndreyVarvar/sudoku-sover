from consts_and_classes import *


class Button:  # a button class, has a draw functions that draws it on screen, action function that does something when its pressed
    def __init__(self, pos, text, text_size, color=WHITE, button_width=None, image=None):
        self.pos = pos
        self.text_size = text_size
        self.font = get_font(1, self.text_size)
        self.text = self.font.render(text, True, BLACK)
        self.text_rect = self.text.get_rect()
        self.color = color
        self.darker_color = (self.color[0] - 30, self.color[1] - 30, self.color[2] - 30)
        self.offset = 15  # how much distance is between the button border and the text (in px)
        self.button_width = button_width

        self.image = image

        if self.image is not None:
            self.rect = self.image.get_rect()
        else:
            self.rect = pg.Rect(0, 0,  # calculating the position is gonna be hard to read and long, so i'll just do it on another line
                                ((self.text_rect[2] + (self.offset * 2)) if self.button_width is None else self.button_width),
                                self.text_rect[3] + (self.offset * 2))

        self.rect.center = self.pos  # i want to center the button on this location

    def draw(self, surface, mouse_pos):  # draw the button on its location
        # calculation part
        button = pg.Surface(self.rect.size)  # create button Surface. APPARENTLY first 2 arguments in the get_rect() tuple are the x,y values, which are equal to 0, but i need width and height, which are 2 last arguments (idx 3 and 4). that's why i use self.rect.size

        self.text_rect.center = (self.rect.width//2, self.rect.height//2)


        # drawing part
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            button.fill(
                self.darker_color)  # dimmer version of the color (I made sure that no button color has a values less than 30, so no error will happen :) )
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
            button.fill(self.color)

        if self.image is None:
            button.blit(self.text, self.text_rect)
        else:
            button.blit(self.image, (0, 0))

        pg.draw.rect(button, BLACK, ((0, 0), button.get_rect()[2:]), 5)

        surface.blit(button, self.rect)

    def action_if_press(self, mouse_pos, mouse_pressed):  # only if mouse is over the button and its pressed.
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and mouse_pressed:
            return 1
        else:
            return 0  # if result is 0, then the variable wont change


class Switch:
    def __init__(self, pos, text1, text2, text_size, color=WHITE, image1=None, image2=None):
        self.pos = pos
        self.text_size = text_size
        self.font = get_font(1, self.text_size)

        self.switch_state = 0  # 0 - off, 1 - on. Basically 0 is the first state, and 1 is the second state -- LOGIC

        self.text1 = self.font.render(text1, True, BLACK)
        self.text2 = self.font.render(text2, True, BLACK)
        self.text1_rect = self.text1.get_rect()
        self.text2_rect = self.text2.get_rect()

        self.offset = 15

        self.cell_rect = max(self.text1_rect, self.text2_rect)  # to make both sides of the switch equally big, so we need the biggest rect
        self.switch_rect = pg.Rect(0, 0, (self.cell_rect.width + self.offset*2)*2, self.cell_rect.height + self.offset*2)

        self.image1 = image1
        self.image2 = image2

        self.color = color
        self.darker_color = (self.color[0] - 50, self.color[1] - 50, self.color[2] - 50)

        self.switch_rect.center = self.pos

        self.pressed_rect = pg.Rect((self.switch_rect.left + self.switch_state*(self.switch_rect.width//2), self.switch_rect.top), (self.switch_rect.width//2, self.switch_rect.height))  # this is the rect of the part of the switch, that is selected, or pressed
        self.unpressed_rect = pg.Rect((self.switch_rect.left + (1 - self.switch_state)*(self.switch_rect.width//2), self.switch_rect.top), (self.switch_rect.width//2, self.switch_rect.height))  # this one is opposite

    def draw(self, surface, mouse_pos):
        switch_surface = pg.Surface(self.switch_rect.size)
        switch_surface.fill(self.color)

        pg.draw.rect(switch_surface, self.darker_color, (self.switch_state*(self.switch_rect.width//2), 0,
                                                         self.switch_rect.width//2, self.switch_rect.height))

        self.text1_rect.center = self.switch_rect.width // 4, self.switch_rect.height // 2
        self.text2_rect.center = (3 * self.switch_rect.width) // 4, self.switch_rect.height // 2

        switch_surface.blit(self.text1, self.text1_rect)
        switch_surface.blit(self.text2, self.text2_rect)

        if self.unpressed_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

        pg.draw.rect(switch_surface, BLACK, pg.Rect((0, 0), self.switch_rect.size), 5)
        pg.draw.line(switch_surface, BLACK, (self.switch_rect.width//2, self.offset), (self.switch_rect.width//2, self.switch_rect.height - self.offset))

        surface.blit(switch_surface, self.switch_rect)  # <- hate this line of code --- long story

    def action_if_press(self, mouse_pos, mouse_pressed):
        """
        works the same as Button class, the only difference is that its only going to change the state, if the mouse
        was pressed over another part of the switch. That's it
        :return: nothing, just change the switch self.state
        """

        if self.unpressed_rect.collidepoint(mouse_pos[0], mouse_pos[1]) and mouse_pressed:
            self.switch_state = 1 - self.switch_state  # 1 - 0 = 1, 1 - 1 = 0, so the state is going to change every time

        self.pressed_rect = pg.Rect((self.switch_rect.left + self.switch_state * (self.switch_rect.width // 2), self.switch_rect.top), (self.switch_rect.width // 2, self.switch_rect.height))  # this is the rect of the part of the switch, that is selected, or pressed
        self.unpressed_rect = pg.Rect((self.switch_rect.left + (1 - self.switch_state) * (self.switch_rect.width // 2), self.switch_rect.top), (self.switch_rect.width // 2, self.switch_rect.height))  # this one is opposite
