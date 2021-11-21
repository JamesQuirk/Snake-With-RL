"""Human interface module to allow interaction with the environment using keys.
"""

from .window import SnakeWindow
from .snake import Snake
import random
import numpy as np

class SnakeGame:

	SPEEDS = {
		"slow": 100,
		"medium": 75,
		"fast": 50
	}

	def __init__(self,env,speed="fast") -> None:
		self.score = 0
		self._env = env
		self._env_key = env.key()
		self._next_action = "e"
		self.SPEED = SnakeGame.SPEEDS[speed]
		self._frames_since_step = 0

		self.window = SnakeWindow(self._env.PARAMS["grid_shape"])

		# Bind keys
		self.window.bind('<Key>',self._key_handler)

		# Queue controller function
		self.window.after(0,self._frame_zero)

		# Start render
		self.window.mainloop()

	def _frame_zero(self):
		"""Called once, when game first starts up."""
		state  = self._env.reset()
		self.window.show(state,self._env_key)
		self.window.after(self.SPEED,self._game_step)

	def _game_step(self):
		"""Take step in game"""
		state, reward, done, _ = self._env.step(self._next_action)
		self.score += reward
		if done:
			self._game_over()
		self.window.show(state,self._env_key)
		self.schedule_id = self.window.after(self.SPEED,self._game_step)

	def _game_over(self):
		#TODO: display "Game Over" on game window
		print("Game Over!")
		print("Final Score:",self.score)
		self.window.after_cancel(self.schedule_id)
		self.window.quit()
 
	def _key_handler(self,event):
		# print(event)
		if event.keysym in ('Up','w'):
			self._next_action = "n"
		elif event.keysym in ('Right','d'):
			self._next_action = "e"
		elif event.keysym in ('Down','s'):
			self._next_action = "s"
		elif event.keysym in ('Left','a'):
			self._next_action = "w"
		elif event.keysym == "Escape":
			self.window.after_cancel(self.schedule_id)
			self.window.quit()


if __name__ == '__main__':
	game = SnakeGame()

