from __future__ import annotations
from abc import ABC, abstractmethod
from math import ceil, floor

class Frog(ABC):
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and 
                callable(subclass.load_data_source) and 
                hasattr(subclass, 'extract_text') and 
                callable(subclass.extract_text) or 
                NotImplemented)

    def __init__(self, index, id) -> None:
        self.index = index
        self.id = id

    @abstractmethod
    def __str__(self) -> str:
        return 'Frog'

    def move(self, board:Board, action) -> bool:
        # self._printIndex()
        self._isActionIllegal(action)
        if self.isPosibleToMove(board):
            match action:
                case 1: return self._moveOneStep(board)
                case 2: return self._moveTwoSteps(board)
        # self._printIndex()
    
    def _isActionIllegal(self, action):
        if action not in [1,2]:
            raise Exception('illegal action')

    def _frogOnSpot(self, something: Frog | None):
        return something is not None

    def isPosibleToMove(self, board:Board):
        return self.isPosibleToDoSomething(board) and not self.endReached(board)

    def isPosibleToDoSomething(self, board):
        return self.emptyInOneStep(board) | self.emptyInTwoStep(board)

    def isNotPosibleToMove(self, board: Board):
        return not self.isPosibleToMove(board)

    def changeIndex(self,index):
        self.index = index

    def goBack(self):
        self.index = self.id

    def _printIndex(self):
        print(f'{str(self)}_{self.id} = estoy en indice {self.index}')

    @abstractmethod
    def _moveOneStep(self, board:Board) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _moveTwoSteps(self, board:Board) -> bool:
        raise NotImplementedError

    @abstractmethod
    def emptyInOneStep(self,board:Board) -> bool:
        raise NotImplementedError
        
    @abstractmethod
    def emptyInTwoStep(self,board:Board) -> bool:
        raise NotImplementedError

    @abstractmethod
    def endReached(self, board:Board) -> bool:
        raise NotImplementedError

    @abstractmethod
    def goalReached(self, board:Board) -> bool:
        raise NotImplementedError 

class RedFrog(Frog):

    def __str__(self):
        return 'RedFrog'

    def _moveOneStep(self, board:Board):
        try:
            if not self._frogOnSpot(board.array[self.index - 1]):
                board.array[self.index] = None
                board.array[self.index - 1] = self
                self.changeIndex(self.index - 1)
                return True
            else:
                return False
        except:
            return False
    
    def _moveTwoSteps(self, board:Board):
        try:
            if not self._frogOnSpot(board.array[self.index - 2]):
                board.array[self.index] = None
                board.array[self.index - 2] = self
                self.changeIndex(self.index - 2)
                return True
            else:
                return False
        except:
            return False

    def emptyInOneStep(self, board: Board) -> bool:
        try:
            return board.array[self.index-1] == None
        except(IndexError):
            return False

    def emptyInTwoStep(self, board: Board) -> bool:
        try:
            return board.array[self.index-2] == None
        except(IndexError):
            return False

    def endReached(self, board: Board) -> bool:
        return 0 == self.index

    def goalReached(self, board: Board) -> bool:
        return self.index < board.nonePosition

class BlueFrog(Frog):

    def __str__(self):
        return 'BlueFrog'

    def _moveOneStep(self, board:Board):
        try:
            if not self._frogOnSpot(board.array[self.index + 1]):
                board.array[self.index] = None
                board.array[self.index + 1] = self
                self.changeIndex(self.index + 1)
                return True
            else:
                return False
        except:
            return False
    
    def _moveTwoSteps(self, board:Board):
        try:
            if not self._frogOnSpot(board.array[self.index + 2]):
                board.array[self.index] = None
                board.array[self.index + 2] = self
                self.changeIndex(self.index + 2)
                return True
            else:
                return False
        except:
            return False

    def emptyInOneStep(self, board: Board) -> bool:
        try:
            return board.array[self.index+1] == None
        except(IndexError):
            return False
    
    def emptyInTwoStep(self, board: Board) -> bool:
        try:
            return board.array[self.index+2] == None
        except(IndexError):
            return False

    def endReached(self, board: Board) -> bool:
        return len(board.array)-1 == self.index

    def goalReached(self, board: Board) -> bool:
        return self.index > board.nonePosition

class Board():
    
    def __init__(self, frogSize: int) -> None:
        if (frogSize % 2) == 0:
            raise Exception('Amount of frogs has to be odd')
        
        self.frogSize = frogSize
        half = frogSize/2
        self.nonePosition = floor(half)
        self.redFrogPositionStart = ceil(half)

        self.blueFrogs = [ BlueFrog(index, index) for index in range(self.nonePosition) ]
        self.redFrogs = [ RedFrog(index, index) for index in range(self.redFrogPositionStart, self.frogSize) ]
        self.frogLen = len(self.blueFrogs)
        self.sameStep = 3

        self.array:list[Frog | None] = self.blueFrogs + [None] + self.redFrogs
        self.frogs = self.blueFrogs + self.redFrogs
        self.steps = []

    def __str__(self) -> str:
        return str([str(frog) if frog is not None else None for frog in self.array])

    def moveFrog(self, index:int, action):
        try:
            successfulAction = self.array[index].move(self,action)
            # print(self)
            # input()
            if successfulAction:
                self.steps.append( (index, action) )
            self._checkGameOver()
            return successfulAction
        except(AttributeError):
            raise Exception('You are not selecting a frog')

    def _checkGameOver(self):

        if self.noPosibleMoves() and not self.puzzleSolved():
            print("You lost :C")
            print(str(self))
            print(self.steps)
            self.reset()
            raise Exception('You lost! Now reset')

    def reset(self):
        
        for frog in self.blueFrogs:
            frog.goBack()

        for frog in self.redFrogs:
            frog.goBack()

        self.array = self.blueFrogs + [None] + self.redFrogs
        self.steps = []
        self.sameStep = 3

    def noPosibleMoves(self):
        return all(frog.isNotPosibleToMove(self) for frog in self.frogs)
    
    def posibleToMove(self):
        return [frog.isPosibleToMove(self) for frog in self.frogs]

    def puzzleSolved(self):
        return all(frog.goalReached(self) for frog in self.frogs)
    
class BoardThread(Board):
    
    def __init__(self, frogSize: int) -> None:
        super().__init__(frogSize)

        self.step = 0
        self.solutionArray = list(range(1, self.nonePosition+1)) + [self.nonePosition] + list(range(self.nonePosition, 0,-1))
        print(f'esta es la solucion array: {self.solutionArray}')

    def amountOfSteps(self):
        print(f'el valor de step es {self.step}')
        number = self.solutionArray[self.step]
        print(f'El numero de raanas es {number}')
        return number
        
    def doAStep(self):
        self.step += 1

    def reset(self):
        self.step = 0
        super().reset()