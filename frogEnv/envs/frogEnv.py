from typing import Any, SupportsFloat
from modules.domain import Board
import gymnasium as gym
from gymnasium.spaces import MultiDiscrete, Box
import numpy as np

boardLen = 5
def getActionSpace():
    action_space = [boardLen]
    for _ in range(boardLen-1): # -1 because there a none in board
        action_space.append(2)
    return action_space 

class FrogEnv(gym.Env):

    metadata = { 'render_modes': ['human'] }

    def __init__(self) -> None:
        self.render_mode = 'human'
        self.board:Board = None
        self.observation_space = Box(low=-1, high=2, shape=(boardLen,), dtype=int)
        self.action_space = MultiDiscrete(getActionSpace())
        self.steps = None
        self.stepsTaken: list = None

    def step(self, action: np.ndarray):

        boardIndex = action[0]
        frogAction = action[boardIndex+1]

        self.stepsTaken.append(action)

        observation, reward = self.board.moveFrog(boardIndex, frogAction)
        print(self.board)

        terminated = self.board.puzzleSolved()
        truncated = self.board.gameStruncated()
        info = {}

        if terminated:
            print(f'The solution was {self.stepsTaken}')

        return observation, reward, terminated, truncated, info
    
    def reset(self, *, seed=None, options= None) -> tuple[Any, dict[str, Any]]:
        self.board = Board(boardLen)
        self.steps = 0
        self.initialReward = 1
        self.stepsTaken = []
        info = {}
        observation = self.board.getArrayInfo()        
        return observation, info
