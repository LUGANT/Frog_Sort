from frogEnv.envs.frogEnv import FrogEnv, boardLen
import numpy as np

#no está bien encarado
#Como existe la posibilidad de usar un NOOP rompe bastante con la logica del juego
def maskedActions(env: FrogEnv) -> np.ndarray:
    action_space = np.zeros((2,boardLen), dtype=int)
    frogs = env.board.frogs

    for index in range(len(env.board.array)):
        if env.board.array[index] == None:
            action_space[0][index] = 0
        else:
            action_space[0][index] = 1 if env.board.array[index].isPosibleToMove(env.board) else 0

    action_space[1][0] = 1
    action_space[1][1] = 1

    return action_space