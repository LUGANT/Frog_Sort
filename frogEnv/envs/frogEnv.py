from typing import Any, SupportsFloat
from modules.domain import Board
import gymnasium as gym
from gymnasium.spaces import MultiDiscrete

boardLen = 5

class FrogEnv(gym.Env):

    def __init__(self) -> None:
        self.board:Board = None
        self.action_space = MultiDiscrete([boardLen+1, 3])

    def step(self, action: Any) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        return super().step(action)
    
    def reset(self) -> tuple[Any, dict[str, Any]]:
        self.board = Board(boardLen)