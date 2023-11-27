from modules.thread_handler import FrogHandler
from modules.domain import Board
from modules.write import readAnswer

frogHandler = FrogHandler(1001)

frogHandler.start()
frogHandler.finish()

board = Board(1001)
answer = readAnswer()
print(f'el resultado es {answer}')

for action in answer:
    board.moveFrog(action[0], action[1])