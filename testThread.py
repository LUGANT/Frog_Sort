from modules.domain import Board
from modules.thread_handler import PuzzleSolverThread
from threading import Semaphore

# Crear una instancia de la clase Board
board = Board(frogSize=5)

# Crear threads para cada posible movimiento
threads = []


for index, frog in enumerate(board.array):
    if frog is not None:
        thread = PuzzleSolverThread(board, frog, index)
        threads.append(thread)

# Iniciar los threads
for thread in threads:
    thread.start()

# Esperar a que todos los threads terminen
for thread in threads:
    thread.join()

print("Todos los threads han terminado.")

