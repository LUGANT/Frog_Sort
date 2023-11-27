from modules.thread_handler import FrogHandler
from modules.domain import Board
from modules.write import readAnswer

froglen = 501

frogHandler = FrogHandler(froglen)

frogHandler.start()
frogHandler.finish()

board = Board(froglen)

print(str(board))
answer = readAnswer()
print(f'el resultado es {answer}')

for action in answer:
    board.moveFrog(action[0], action[1])

print(str(board))