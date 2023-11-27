import gymnasium as gym
from gymnasium.spaces import MultiDiscrete
from frogEnv.envs.frogEnv import FrogEnv
import numpy as np

boardLen = 5

space = MultiDiscrete([boardLen, 2])

# num_ranas = 3
# acciones_por_rana = 2
# espacio_de_accion_expandido = np.arange(num_ranas * acciones_por_rana)
# espacio_de_accion_expandido = espacio_de_accion_expandido.reshape((num_ranas, acciones_por_rana))

# action_space = np.array( [ np.zeros(boardLen), np.ones(2) ], dtype=int )


# print(espacio_de_accion_expandido)
# print(type(espacio_de_accion_expandido))
# print(action_space)
# print(space.sample())
# print(type(space.sample()))

# env = gym.make("frog_env")

# env.reset()

# env.step(np.array([3,0]))
# env.step(np.array([1,1]))
# env.step(np.array([2,0]))
# env.step(np.array([4,1]))
# env.step(np.array([3,0]))

# print()
# env.reset()

# env.step(np.array([3,0]))
# env.step(np.array([1,1]))
# env.step(np.array([0,0]))
# env.step(np.array([2,1]))
# env.step(np.array([4,1]))
# env.step(np.array([3,0]))
# env.step(np.array([1,1]))
# env.step(np.array([2,0]))