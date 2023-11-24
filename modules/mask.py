from frogEnv.envs.frogEnv import FrogEnv, boardLen
import numpy as np

#no está bien encarado
#Como existe la posibilidad de usar un NOOP rompe bastante con la logica del juego
def maskedActions(env: FrogEnv) -> np.ndarray:
    action_space = np.zeros((boardLen,3), dtype=int)
    frogs = env.board.frogs
    for frog, index in zip(frogs, range(len(frogs))):
        if frog.isPosibleToMove():
            action_space[frog.index] = 1
    pass