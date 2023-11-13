from __future__ import annotations

import pygame
import numpy as np
from elementWithPosition import ElementWithPosition


WHITE = (255, 255, 255)
FRAMESIZE_X = 800
FRAMESIZE_Y = 600  

class GameHandler():
    """GameHandler Class. Manages events, drawing and pygame elements

        Atributes
        ---------
        game_window: Surface
            Defines the window display, allows to use the blit method to load elements
        game_background: Surface
            Defines the background window
        game_display: Module
            Defines the display, it allows to use the flip method to update elements
        game_lines: list[Line]
            Stores the lines used in the game to draw the plane's trajectory 
    """

    def __init__(self) -> None:
        self.game_window = pygame.display.set_mode((FRAMESIZE_X, FRAMESIZE_Y))
        self.game_background = pygame.transform.scale(pygame.image.load('assets/background.jpg').convert(), (FRAMESIZE_X, FRAMESIZE_Y))
        self.game_display = pygame.display

    def load_background(self):
        self.game_window.blit(self.game_background,  (0,0))

    def display_score(self, score, color=WHITE, font="times", size=20):
        '''
        Loads the score in the top left corner of the screen
        '''
        pygame.font.init()
        score_font = pygame.font.SysFont(font, size, bold=True)
        score_surface = score_font.render('Score : ' + str(np.round(score,2)), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (FRAMESIZE_X/8, 15)
        self.game_window.blit(score_surface, score_rect)
        self.game_display.flip()

    def handle_events(self):
        """Manages pygame event"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def wait_for_keypress(self):
        """Waits until enter is pressed. 

        Only for debugging
        """
        waiting = True
        while waiting:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

    # shield_position realmente debería de ser parte de pala, pero por ahora se mantendra como una lista
    def draw_elements(self, elements: list[ElementWithPosition], aditional_space:int) -> None:
        """draws elements on the screen

        Arguments
        -----
        elements: list[ElementWithPosition]
        aditional_space: int
            Is the space added to the last element in list of elements. it is added to the position_x
        """
        for element in elements:
            self.draw_element(element)

        self.game_display.flip()

    def draw_element(self, element:ElementWithPosition, aditional_space_x:int=0, aditional_space_y:int=0) -> None:
        """Draws the element on screen

        Args:
            element (ElementWithPosition)
            aditional_space_x (int, optional): added space to position_x
            aditional_space_y (int, optional): added space to position_y
        """
        self.game_window.blit(element.image, (element.position_x+aditional_space_x, element.position_y+aditional_space_y))

    def flip(self):
        self.game_display.flip()