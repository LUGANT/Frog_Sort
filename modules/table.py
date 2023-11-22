class Frog():
    def __init__(self, direction: bool) -> None:
        self.forward = direction
            #true -> forward
            #false -> backwards

class Table():
    
    def __init__(self, blueFrogs:list, redFrogs:list) -> None:
        self.array:list[Frog | None] = blueFrogs + [None] + redFrogs

    def move(self, frogId, action):
        forward = self.array[frogId].forward
        if forward:
            pass

    def _changePreviousPosition(self):
        pass
        
    def gameOver(self):
        return Exception("The game has ended")