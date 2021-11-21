"""Apply random actions"""
import numpy as np

class RandomAgent:
	def __init__(self,env) -> None:
		self.env = env

	def act(self,_):
		action = self.env.action_space.sample()

		_, _, done, _ = self.env.step(action)
		return done

