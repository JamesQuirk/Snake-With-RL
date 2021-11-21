import yaml
from snake import SnakeEnv
from agents import *

with open("params.yaml","r") as p:
	params = yaml.safe_load(p)

env = SnakeEnv(params["env"])

if params["train"]["agent"] == "random":
	agent = RandomAgent(env)

obs = env.reset()

for step in range(params["train"]["steps"]):
	print("Step:",step)
	print(obs)
	done = agent.act(obs)
	print("Episode done:",done)
	if done or (step % 50 == 0 and step != 0):
		print("Done, or timed out")
		obs = env.reset()

