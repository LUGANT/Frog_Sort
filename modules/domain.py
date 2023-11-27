from __future__ import annotations
from abc import ABC, abstractmethod
from math import ceil, floor
import numpy as np

class Frog(ABC):
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and 
                callable(subclass.load_data_source) and 
                hasattr(subclass, 'extract_text') and 
                callable(subclass.extract_text) or 
                NotImplemented)

    def __init__(self, index,id) -> None:
        self.index = index
        self.id = id

    @abstractmethod
    def __str__(self) -> str:
        return 'Frog'

    def move(self, board:Board, action):
        self._printIndex()
        self._isActionIllegal(action)
        if self.isPosibleToMove(board):
            try:
                match action:
                    case 1: self._moveOneStep(board)
                    case 2: self._moveTwoSteps(board)
            except: #This happens when you can move, but you have choosen a spot where a frog lies
                return -1 #No Reward
            return 1 #Reward
        else:
            return 0 #No Reward
    
    def goBack(self):
        self.index = self.id

    def _isActionIllegal(self, action):
        if action not in [1,2]:
            raise Exception(f'illegal action: {action} is not posible. Use 0 or 1 ')

    def _frogOnSpot(self, something: Frog | None):
        if something is not None:
            raise Exception('There is already a frog there')

    def isPosibleToMove(self, board:Board):
        return (self.emptyInOneStep(board) | self.emptyInTwoStep(board)) & (not self.endReached(board))

    def isNotPosibleToMove(self, board: Board):
        return not self.isPosibleToMove(board)

    def _changeIndex(self,index):
        self.index = index

    def _printIndex(self):
        print(f'Now my position is {self.index}')

    @abstractmethod
    def _moveOneStep(self, board:Board):
        raise NotImplementedError

    @abstractmethod
    def _moveTwoSteps(self, board:Board):
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
        self._frogOnSpot(board.array[self.index - 1])
        board.array[self.index] = None
        board.array[self.index - 1] = self
        self._changeIndex(self.index - 1)
    
    def _moveTwoSteps(self, board:Board):
        self._frogOnSpot(board.array[self.index - 2])
        board.array[self.index] = None
        board.array[self.index - 2] = self
        self._changeIndex(self.index - 2)

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
        self._frogOnSpot(board.array[self.index + 1])
        board.array[self.index] = None
        board.array[self.index + 1] = self
        self._changeIndex(self.index + 1)
    
    def _moveTwoSteps(self, board:Board):
        self._frogOnSpot(board.array[self.index + 2])
        board.array[self.index] = None
        board.array[self.index + 2] = self
        self._changeIndex(self.index + 2)

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
        return len(board.array) == self.index

    def goalReached(self, board: Board) -> bool:
        return self.index > board.nonePosition

class Board():
    
    def __init__(self, frogSize: int) -> None:
        if (frogSize % 2) == 0:
            raise Exception('Amount of frogs has to be odd')
        
        half = frogSize/2
        self.nonePosition = floor(half)
        redFrogPositionStart = ceil(half)

        self.blueFrogs = [ BlueFrog(index,index) for index in range(self.nonePosition) ]
        self.redFrogs = [ RedFrog(index,index) for index in range(redFrogPositionStart, frogSize) ]
        self.array:list[Frog | None] = self.blueFrogs + [None] + self.redFrogs
        self.frogs = self.blueFrogs + self.redFrogs

        solutionArray = list(range(1, self.nonePosition+1)) + [self.nonePosition] + list(range(self.nonePosition, 0,-1))
        self.totalPunishment = - sum(solutionArray)

    def __str__(self) -> str:
        return str([str(frog) if frog is not None else None for frog in self.array])

    def reversed__str__(self) -> str:
        return str([str(frog) if frog is not None else None for frog in reversed(self.array)])

    def moveFrog(self, index:int, action):
        try:
            isActionCompleted = self.array[index].move(self,action)
            self._checkGameOver()

            if isActionCompleted == -1:
                isActionCompleted = self.totalPunishment

            return self.getArrayInfo(), isActionCompleted
        except(AttributeError):
            raise Exception('You are not selecting a frog')

    def getFrog(self, index:int) -> Frog:
        if self.array[index] == None:
            raise Exception("There's no frog here")
        return self.array[index]

    def getArrayInfo(self):
        array = np.full(shape= len(self.array), fill_value=-1, dtype=int)
        for frog in self.frogs:
            if frog.emptyInOneStep(self):
                array[frog.index] = 1
            if frog.emptyInTwoStep(self):
                array[frog.index] = 2
            if frog.isNotPosibleToMove(self):
                array[frog.index] = 0
        return array

    def _checkGameOver(self):

        if self.noPosibleMoves():

            if self.puzzleSolved():
                print("You solved the puzzle!!!")
                
            else:
                print("You lost :C")

    def reset(self):
        
        for frog in self.blueFrogs:
            frog.goBack()

        for frog in self.redFrogs:
            frog.goBack()

        self.array = self.blueFrogs + [None] + self.redFrogs
        self.steps = []
        self.sameStep = 3

    def gameStruncated(self):
        return self.noPosibleMoves() & (not self.puzzleSolved())

    def noPosibleMoves(self):
        return all(frog.isNotPosibleToMove(self) for frog in self.frogs)
    
    def puzzleSolved(self):
        return all(frog.goalReached(self) for frog in self.frogs)