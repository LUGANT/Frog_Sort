# importing the modules 
from collections.abc import Callable, Iterable, Mapping
import threading
from threading import Lock
from typing import Any
from modules.domain import Board, RedFrog, BlueFrog, BoardThread, Frog
import random

class PuzzleSolverThread(threading.Thread):
    
    def __init__(self, board, frog, id):
        super().__init__()
        self.board: Board = board
        self.frog: RedFrog | BlueFrog = frog
        self.threadId = id
        self.semaphore: Lock = Lock()

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

class FrogThread(threading.Thread):

    def __init__(self, board: BoardThread, semaphore: Lock):
        super().__init__()
        self.board = board
        self.semaphore = semaphore
        self.maxSteps = len(board.frogs)
        self.frogs: list[Frog] = None

    def run(self) -> None:

        while not self.board.puzzleSolved() and not self.board.noPosibleMoves():
            
            self.semaphore.acquire()
            print(f'agarre el semaforo, soy {str(self)}')
            print(str(self.board))
            print()

            try:
                for index in range( self.board.amountOfSteps() ):

                    frog: Frog = self.frogs[index]
                    
                    if frog.emptyInOneStep(self.board):

                        self.board.moveFrog(frog.index, 1)

                        print(f'di un paso, soy {str(self)}')
                        print(str(self.board))
                        print()

                        self.semaphore.release()

                    if frog.emptyInTwoStep(self.board):

                        self.board.moveFrog(frog.index, 2)
                        
                        print(f'di dos pasos, soy {str(self)}')
                        print(str(self.board))
                        print()

                        self.semaphore.release()
                        

            except Exception as e:
                print(f'algo pasó: {e}')
                print(self.board.steps)
                print(str(self.board))
                input()

            # self.semaphore.release()

        print(str(self.board))
        print(self.board.steps)

class RedFrogThread(FrogThread):

    def __init__(self, board: BoardThread, semaphore: Lock):
        super().__init__(board, Lock())
        self.frogs: list[Frog] = self.board.redFrogs

class BlueFrogThread(FrogThread):

    def __init__(self, board: BoardThread, semaphore: Lock):
        super().__init__(board, Lock())
        self.frogs: list[Frog] = self.board.blueFrogs
        self.frogs.reverse()

class FrogHandler():

    def __init__(self, size) -> None:
        self.board = BoardThread(size)
        print(str(self.board))
        self.semaphore = Lock()
        self.redFrogThread = RedFrogThread(self.board, self.semaphore)
        self.blueFrogThread = BlueFrogThread(self.board, self.semaphore)

    def start(self):
        self.blueFrogThread.start()
        self.redFrogThread.start()

    def finish(self):
        self.blueFrogThread.join()
        self.redFrogThread.join()