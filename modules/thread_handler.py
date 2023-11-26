# importing the modules 
import threading
from threading import Semaphore
from modules.domain import Board, RedFrog, BlueFrog
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
            action = random.choice([1,2])
            
            while current_attempt < max_attempts:
                
                try:
                    self.semaphore.acquire()
                    if self.board.moveFrog(self.frog.index, action):
                        # El movimiento fue exitoso, salir del bucle de intentos
                        break
                    current_attempt += 1

                except Exception as e:
                    print(f"Error in thread {self.threadId}: {e}")
                    current_attempt += 1

                finally:
                    self.semaphore.release()

            # Si llegamos a este punto, hemos agotado los intentos
            current_attempt = 0