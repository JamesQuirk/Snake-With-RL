"""Play snake as human"""

from snake import SnakeGame
from snake import SnakeEnv
import yaml

with open("params.yaml","r") as file:
	env_params = yaml.safe_load(file)["env"]

env  = SnakeEnv(env_params)
game = SnakeGame(env)

