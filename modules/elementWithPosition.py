from __future__ import annotations

from pygame import Surface
import math

class ElementWithPosition():
    """Class which is inherited by Plane and Location.

        The class has responsabilities related its position on screen and atributes related to pygame.

        Atributes
        ---------
        position_x

        position_y

        image: Surface
            
        id: int
            
        
        Methods
        ---------
        position() -> tuple[int, int]
            Returns a tuple with the element's position
        change_position(x:int, y:int) -> void
            Changes position of the element
        change_id() -> void
            Chages the id of the element
        same_position_as(element: ElementWithPosition) -> bool
            Returns if the elements shares the same position on screen
        calculate_distance(element: ElementWithPosition) -> int
            Returns the raw distance of an element from another element related to the screen
    """

    def __init__(self, position_x, position_y, image, id) -> None:
        self.position_x: int = position_x
        self.position_y: int = position_y
        self.image: Surface = image
        self.id: int = id

    def position(self) -> tuple[int, int]:
        """Returns a tuple with the element's position

        Returns:
            tuple[int, int]
        """
        return (self.position_x, self.position_y)

    def change_position(self,x,y):
        """Changes position of the element

        Args:
            x (int): position_x
            y (int): position_y
        """
        self.position_x = x
        self.position_y = y

    def change_id(self, id):
        """Chages the id of the element

        Args:
            id (int)
        """
        self.id = id

    def same_position_as(self, element: ElementWithPosition) -> bool:
        """Returns if the elements shares the same position on screen

        Args:
            element (ElementWithPosition)

        Returns:
            bool
        """
        return self.position() == element.position() 

    def calculate_distance(self, element:ElementWithPosition) -> int:
        """Returns the raw distance of an element from another element related to the screen

        Args:
            element (ElementWithPosition)

        Returns:
            int
        """
        return int( math.sqrt(math.pow((self.position_x - element.position_x),2) + math.pow((self.position_y - element.position_y),2)) )
