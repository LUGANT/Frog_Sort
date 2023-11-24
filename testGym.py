from gymnasium.spaces import MultiDiscrete

space = MultiDiscrete([6, 3])
print(space.sample())