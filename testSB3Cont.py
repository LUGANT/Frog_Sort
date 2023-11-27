from stable_baselines3.common.callbacks import BaseCallback
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker
from modules.mask import maskedActions
import gymnasium as gym
from gymnasium.spaces import MultiDiscrete
from frogEnv.envs.frogEnv import FrogEnv
import os
import tensorflow as tf

env = gym.make("frog_env")

env = ActionMasker(env, maskedActions)

models_dir = "models/PPO"
logdir = "logs"

Writer = tf.summary.create_file_writer(logdir)

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

TIMESTEPS = 200_000

# crear tu propia red neuronal para el entrenamiento 
policy_kwargs = dict(
    net_arch=dict(pi=[512,512], vf=[512,512])
)

class ExplorationDecayCallback(BaseCallback):
    def __init__(self, exploration_start: float, exploration_end: float, total_timesteps: int, verbose=0):
        super(ExplorationDecayCallback, self).__init__(verbose)
        self.exploration_start = exploration_start
        self.exploration_end = exploration_end
        self.total_timesteps = total_timesteps

    def _on_step(self) -> bool:
        current_step = self.num_timesteps
        frac_remaining = 1 - (current_step / self.total_timesteps)
        new_exploration = self.exploration_start * frac_remaining + self.exploration_end * (1 - frac_remaining)
        self.model.exploration_rate = new_exploration
        return True

exploration_start = 0.4
exploration_end = 0.05
total_timesteps = 1_000_000

callback = ExplorationDecayCallback(exploration_start, exploration_end, total_timesteps)

model = MaskablePPO("MlpPolicy", env, verbose=1, learning_rate=2.5e-4, 
            tensorboard_log= logdir)

TIMESTEPS = 200_000

for i in range(5):
    model.learn(total_timesteps=TIMESTEPS, progress_bar=True, 
                reset_num_timesteps=False, 
                 tb_log_name="frog_puzzle_V_0.3")

    model.save(f"{models_dir}/{TIMESTEPS*i}")