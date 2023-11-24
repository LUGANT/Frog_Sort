from modules.domain import Board

# Example with 3 frogs
# board = Board(2) # Raises exception - only odd numbers
board = Board(3)
print(str(board))

# board.moveFrog(0,2) # Raises exception - there is already a frog there
# print(str(board))

board.moveFrog(0,1)
print(str(board))

# board.moveFrog(0,1) # Raises exception - you are picking a None, not a Frog
# print(str(board))

board.moveFrog(2,2)
print(str(board))

board.moveFrog(1,1)
print(str(board))

# Example with 5 frogs
board = Board(5)
print(str(board))

board.moveFrog(3,1)
print(str(board))

board.moveFrog(1,2)
print(str(board))

board.moveFrog(0,1)
print(str(board))

board.moveFrog(2,2)
print(str(board))

board.moveFrog(4,2)
print(str(board))

board.moveFrog(3,1)
print(str(board))

board.moveFrog(1,2)
print(str(board))

board.moveFrog(2,1)
print(str(board))