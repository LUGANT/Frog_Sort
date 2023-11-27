from typing import Any, SupportsFloat
from modules.domain import Board
import gymnasium as gym
from gymnasium.spaces import MultiDiscrete, Box
import numpy as np

boardLen = 5

class FrogEnv(gym.Env):

    metadata = { 'render_modes': ['human'] }

    def __init__(self) -> None:
        self.render_mode = 'human'
        self.board:Board = Board(boardLen)
        self.observation_space = Box(low=-1, high=2, shape=(boardLen,), dtype=int)
        self.action_space = MultiDiscrete([boardLen,boardLen])
        self.steps = None
        self.accumulatedReward = None
        self.stepsTaken: list = None

    def step(self, action: np.ndarray):

        boardIndex = action[0]
        frogAction = action[1]

        self.stepsTaken.append(action)

        observation, reward = self.board.moveFrog(boardIndex, frogAction)
        print(self.board)

        if reward < 0:
            self.accumulatedReward = reward
        else:
            self.accumulatedReward += reward

        if self.board.puzzleSolved():
            self.accumulatedReward += 100

        terminated = self.board.puzzleSolved()
        truncated = self.board.gameStruncated()
        info = {}

        if terminated:
            print(f'The solution was {self.stepsTaken}')

        return observation, self.accumulatedReward, terminated, truncated, info
    
    def reset(self, *, seed=None, options= None) -> tuple[Any, dict[str, Any]]:
        self.board.reset()
        self.steps = 0
        self.initialReward = 1
        self.stepsTaken = []
        self.accumulatedReward = 0
        info = {}
        observation = self.board.getArrayInfo()        
        return observation, info
