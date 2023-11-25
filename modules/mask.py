from frogEnv.envs.frogEnv import FrogEnv, boardLen
import numpy as np

#no está bien encarado
#Como existe la posibilidad de usar un NOOP rompe bastante con la logica del juego
def maskedActions(env: FrogEnv) -> np.ndarray:
    action_space =  [ np.zeros(boardLen, dtype=int) for _ in range(boardLen) ]
    frogs = env.board.frogs
    
    for index, frog in enumerate(frogs):
        if index == 0:
            action_space[0][index] = 1 if frog.isPosibleToMove(env.board) else 0
        else:
            action_space[index]
    
    return action_space