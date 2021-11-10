from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
from .game import SnakeGame

class SnakeEnv(Env):
	'''
	--- MDP ---

	Env: Snake game. 
	State: The game grid containing integers encoding what each grid square contains: empty (0), snake body/tail (1), snake head (2) or cherry (3)
	Actions: Up, Down, Left, Right, Nothing (technically choosing the same action twice is equal to choosing the first action and then choosing 'Nothing')
	Reward: Score (number of cherries eaten)
	Observation: The game grid containing integers encoding what each grid square contains: empty (0), snake body/tail (1), snake head (2) or cherry (3)
	'''
	def __init__(self):
		self.CHERRY_REWARD = 100
		self.REWARD_PROXIMITY = True

		self.previous_proximity = None
		self.previous_action = None

		# Actions: Up, Down, Left, Right, Nothing
		self.actions_code2ind = {
			'n':0,
			's':1,
			'e':2,
			'w':3,
			# None:4
		}
		self.actions_ind2code = {
			0:'n',
			1:'s',
			2:'e',
			3:'w',
			# 4:None
		}
		self.action_space = Discrete(len(self.actions_ind2code))
		# Setup game objects
		self.game = SnakeGame(mode='code')

		# Observation space contains the range of possible values for the observation array.
		self.observation_space = Box(low=np.zeros(shape=self.game.grid_shape),high=np.zeros(shape=self.game.grid_shape)+3)
		self.state = np.zeros(shape=self.game.grid_shape)	# Initialise the grid as empty


	def step(self,action):
		# Action will be the direction for the snake to move, encoded as integers 0 to 4.
		assert action in self.actions_ind2code.keys(), 'Invalid action: ' + str(action)
		direction = self.actions_ind2code[action]
		
		game_over, cherry_eaten = self.game.advance_timestep(direction)

		if game_over:
			reward = -100
		else:
			if cherry_eaten:
				reward = self.CHERRY_REWARD
			else:
				reward = 0

			if self.REWARD_PROXIMITY:
				proximity = self.game.distance_from_cherry()
				if self.previous_proximity is None or (self.previous_proximity is not None and proximity > self.previous_proximity):
					prox_reward = -10
				else:
					prox_reward = 10
				self.previous_proximity = proximity
				reward += prox_reward

		self.state = self.game.get_grid_state()
		
		info = {}
		return self.state, reward, game_over, info

	def render(self,mode):
		self.game.show()

	def reset(self):
		self.game.window.destroy()
		del self.game, self.state
		self.game = SnakeGame(mode='code')
		self.state = np.zeros(shape=self.game.grid_shape)
		return self.state
