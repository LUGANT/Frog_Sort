from gymnasium.envs.registration import register

register(
    id='frog_env',
    entry_point='frogEnv.envs:FrogEnv',
)