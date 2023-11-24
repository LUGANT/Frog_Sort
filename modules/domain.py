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

    def __init__(self, index) -> None:
        self.index = index

    @abstractmethod
    def __str__(self) -> str:
        return 'Frog'

    def move(self, board:Board, action):
        self._printIndex()
        self._isActionIllegal(action)
        if self.isPosibleToMove(board):
            match action:
                case 1: self._moveOneStep(board)
                case 2: self._moveTwoSteps(board)
        self._printIndex()
    
    def _isActionIllegal(self, action):
        if action not in [1,2]:
            raise Exception('illegal action')

    def _frogOnSpot(self, something: Frog | None):
        if something is not None:
            raise Exception('There is a frog already there')

    def isPosibleToMove(self, board:Board):
        return (self._emptyInOneStep(board) | self._emptyInTwoStep(board)) & (not self.endReached(board))

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
    def _emptyInOneStep(self,board:Board) -> bool:
        raise NotImplementedError
        
    @abstractmethod
    def _emptyInTwoStep(self,board:Board) -> bool:
        raise NotImplementedError

    @abstractmethod
    def endReached(self, board:Board) -> bool:
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

    def _emptyInOneStep(self, board: Board) -> bool:
        try:
            return board.array[self.index-1] == None
        except(IndexError):
            return False

    def _emptyInTwoStep(self, board: Board) -> bool:
        try:
            return board.array[self.index-2] == None
        except(IndexError):
            return False

    def endReached(self, board: Board) -> bool:
        return 0 == self.index

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

    def _emptyInOneStep(self, board: Board) -> bool:
        try:
            return board.array[self.index+1] == None
        except(IndexError):
            return False
    
    def _emptyInTwoStep(self, board: Board) -> bool:
        try:
            return board.array[self.index+2] == None
        except(IndexError):
            return False

    def endReached(self, board: Board) -> bool:
        return len(board.array) == self.index

class Board():
    
    def __init__(self, frogSize: int) -> None:
        if (frogSize % 2) == 0:
            raise Exception('Amount of frogs has to be odd')
        
        half = frogSize/2
        nonePosition = floor(half)
        redFrogPositionStart = ceil(half)

        blueFrogs = [ BlueFrog(index) for index in range(nonePosition) ]
        redFrogs = [ RedFrog(index) for index in range(redFrogPositionStart, frogSize) ]

        self.array:list[Frog | None] = blueFrogs + [None] + redFrogs
        self.frogs = blueFrogs + redFrogs

    def __str__(self) -> str:
        return str([str(frog) if frog is not None else None for frog in self.array])

    def moveFrog(self, index:int, action):
        try:
            self.array[index].move(self,action)
            self._checkGameOver()
        except(AttributeError):
            raise Exception('You are not selecting a frog')

    def _checkGameOver(self):
        gameover = all(frog.isNotPosibleToMove(self) for frog in self.frogs)
        if gameover:
            print("You solved the puzzle!!!")