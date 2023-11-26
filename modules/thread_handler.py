# importing the modules 
from collections.abc import Callable, Iterable, Mapping
import threading
from threading import Semaphore
from typing import Any
from modules.domain import Board, RedFrog, BlueFrog, BoardThread
import random

class PuzzleSolverThread(threading.Thread):
    
    def __init__(self, board, frog, id, semaphore):
        super().__init__()
        self.board: Board = board
        self.frog: RedFrog | BlueFrog = frog
        self.threadId = id
        self.semaphore: Semaphore = semaphore

    def run(self):
        max_attempts = 10  # Número máximo de intentos
        current_attempt = 0

        while not self.board.puzzleSolved() and not self.board.noPosibleMoves():
            self.semaphore.acquire()
            action = random.choice([1,2])
            
            while current_attempt < max_attempts:
                try:
                    if self.board.moveFrog(self.frog.index, action):
                        input()
                        # El movimiento fue exitoso, salir del bucle de intentos
                        break
                    current_attempt += 1
                except Exception as e:
                    input()
                    current_attempt += 1
                    print(f"Error in thread {self.threadId}: {e}")
                    self.board.reset()
                    # print(f'board:{str(self.board)}\nposibleToMove: {self.board.posibleToMove()}\nfrog_{self.frog.id}_pos: {self.frog.index}\nthread:{self.threadId}\ntype:{str(self.frog)}\naction: {action}')
                finally:
                    self.semaphore.release()

            # Si llegamos a este punto, hemos agotado los intentos
            current_attempt = 0

        print(self.board.steps)

        # while not self.board.puzzleSolved() and not self.board.noPosibleMoves():
        #     action = random.choice([1,2])
        #     try:
        #         # self.semaphore.acquire()
        #         self.board.moveFrog(self.frog.index, action)
        #         print(f'board:{str(self.board)}\nposibleToMove: {self.board.posibleToMove()}\nfrog_{self.frog.id}_pos: {self.frog.index}\nthread:{self.threadId}\ntype:{str(self.frog)}\naction: {action}')
        #         input()
        #         # self.semaphore.release()
        #     except Exception as e:
        #         print(f"Error in thread {self.threadId}: {e}")
        #         # self.semaphore.release()

class RedFrogThread(threading.Thread):

    def __init__(self, board: BoardThread, semaphore: Semaphore):
        super().__init__()
        self.board = board
        self.semaphore = semaphore
        self.frogs = board.redFrogs
        self.maxSteps = len(board.frogs)

    def run(self) -> None:
        return super().run()
    
class BlueFrogThread(threading.Thread):

    def __init__(self, board: BoardThread, semaphore: Semaphore):
        super().__init__()
        self.board = board
        self.semaphore = semaphore
        self.frogs = board.blueFrogs
        self.frogLen = len(self.frogs)

    def run(self) -> None:
        while True:
            return super().run()
    
class FrogHandler():

    def __init__(self, size) -> None:
        self.board = BoardThread(size)
        self.semaphore = Semaphore(1)
        self.redFrogThread = RedFrogThread(self.board, self.semaphore)
        self.blueFrogThread = BlueFrogThread(self.board, self.semaphore)

    def start(self):
        self.redFrogThread.start()
        self.blueFrogThread.start()
