"""Snake environment.
Handles all game logic internally."""

from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
from .snake import Snake
from .cherry import Cherry

class SnakeEnv(Env):
	'''
	--- MDP ---

	Env: Snake game. 
	State: The game grid containing integers encoding what each grid square contains: empty (0), snake body/tail (1), snake head (2) or cherry (3)
	Actions: Up, Down, Left, Right, Nothing (technically choosing the same action twice is equal to choosing the first action and then choosing 'Nothing')
	Reward: Score (number of cherries eaten)
	Observation: The game grid containing integers encoding what each grid square contains: empty (0), snake body/tail (1), snake head (2) or cherry (3)
	'''
	NOTHING = 0
	SNAKE_HEAD = 2
	SNAKE_BODY = 1
	CHERRY = 3

	def __init__(self,params: dict):
		self.PARAMS = params

		if "seed" in params:
			print("Seeding RNG")
			np.random.seed(params["seed"])

		self.previous_proximity = None
		self.previous_action = None

		# Actions: Up, Down, Left, Right, Nothing
		self._actions_char2ind = {
			'n':0,
			's':1,
			'e':2,
			'w':3,
			# None:4
		}
		self._actions_ind2char = {
			0:'n',
			1:'s',
			2:'e',
			3:'w',
			# 4:None
		}
		self.action_space = Discrete(len(self._actions_ind2char))

		# Observation space contains the range of possible values for the observation array.
		self.observation_space = Box(low=np.zeros(shape=self.PARAMS["grid_shape"]),high=np.zeros(shape=self.PARAMS["grid_shape"])+3)

	def reset(self) -> np.ndarray:
		self.total_reward = 0

		# Initialise the grid as empty
		self.state = np.zeros(shape=self.PARAMS["grid_shape"])

		# Initialise snake
		self.snake = Snake(self.PARAMS["grid_shape"][1]//2,self.PARAMS["grid_shape"][0]//2,direction='e')
		self._update_state_snake()

		# Place cherry
		self._place_cherry(initialise=True)
		self._update_state_cherry()

		return self.state

	def _place_cherry(self,initialise=False):
		""" Recursively places cherry until finds a valid position (if one exists). """
		if initialise:
			self.cherry = Cherry()
		if self.state[self.state == 0].size > 0:
			# There is at least 1 empty position in grid
			self.cherry.x = np.random.randint(0,self.PARAMS["grid_shape"][1])
			self.cherry.y = np.random.randint(0,self.PARAMS["grid_shape"][0])
			if self.state[self.cherry.y,self.cherry.x] != 0:
				# If new cherry position conflicts with other object in the environment, replace.
				self._place_cherry()
		else:
			# No positions available
			self.cherry = None
		self._update_state_cherry()

	def _update_state(self):
		self._update_state_snake()
		self._update_state_cherry()

	def _update_state_snake(self):
		if self.state[self.state == self.SNAKE_HEAD].size == 0:
			# Snake has not been placed yet.
			self.state[self.snake.head.y,self.snake.head.x] = self.SNAKE_HEAD
			for part in self.snake.tail:
				self.state[part.y,part.x] = self.SNAKE_BODY
		else:
			# Just need to move head and remove previous position of last part in tail.
			if self._object_oob(self.snake.head):
				print("Snake head out-of-bounds")
				return False
			else:
				self.state[self.snake.head.y,self.snake.head.x] = self.SNAKE_HEAD
			self.state[self.snake.tail[0].y,self.snake.tail[0].x] = self.SNAKE_BODY
			if self.snake.removed_block is not None:
				# If the tail has not been extended, there will be a block removed that is temporarily stored
				# in 'removed_block'.
				self.state[self.snake.removed_block.y,self.snake.removed_block.x] = self.NOTHING
	
	def _update_state_cherry(self):
		if self.cherry is not None:
			self.state[self.cherry.y,self.cherry.x] = self.CHERRY

	def _object_oob(self,obj) -> bool:
		"""Check if object is out-of-bounds"""
		if obj.x < 0 or obj.x >= self.state.shape[1] or obj.y < 0 or obj.y >= self.state.shape[0]:
			return True
		else:
			return False

	def _apply_action(self,action):
		"""
		:: action: (char) action character
		"""
		body_collision = self.snake.move(direction=action,callback=self._update_state_snake)
		if self.snake.head.x == self.cherry.x and self.snake.head.y == self.cherry.y:
			cherry_eaten = True
			print("Cherry eaten, replacing")
			self._place_cherry()
			self.snake.extend_tail()
		else:
			cherry_eaten = False
		
		if body_collision \
			or (self.snake.head.x < 0 \
			or self.snake.head.x >= self.state.shape[1] \
			or self.snake.head.y < 0 \
			or self.snake.head.y >= self.state.shape[0]) \
			or self.cherry is None:
			# Body, wall collision or no available position for cherry (env full)
			done = True
		else:
			done = False

		return done, cherry_eaten

	def _evaluate_reward(self,done,cherry_eaten):
		reward = 0

		if done:
			reward += self.PARAMS["reward"].get("game_over",0)

		if cherry_eaten:
			reward += self.PARAMS["reward"].get("cherry",0)

		if self.cherry is not None:
			proximity = self.snake.distance_from(self.cherry)
			if self.previous_proximity is None or (self.previous_proximity is not None and proximity < self.previous_proximity):
				reward += self.PARAMS["reward"].get("proximity_gain",0)
			else:
				reward += self.PARAMS["reward"].get("proximity_loss",0)
			self.previous_proximity = proximity
		else:
			reward += self.PARAMS["reward"].get("completed",0)
		return reward

	def step(self,action):
		""":: action: (int | str) 0 to 3 inclusive or character (n, s, e, w) representing direction to go"""
		if isinstance(action,str):
			assert action in self._actions_char2ind, "Invalid action: " + action
			direction = action
		elif isinstance(action,int):
			assert action in self._actions_ind2char.keys(), 'Invalid action: ' + str(action)
			direction = self._actions_ind2char[action]
		
		done, cherry_eaten = self._apply_action(direction)
		reward = self._evaluate_reward(done,cherry_eaten)
		self.total_reward += reward
		
		info = {
			"cherry_eaten":cherry_eaten, # If done and cherry_eaten -> completed!
			"total_reward":self.total_reward
			}
		return self.state, reward, done, info

	def key(self):
		return {
			"NOTHING": 0,
			"SNAKE_HEAD": 2,
			"SNAKE_BODY": 1,
			"CHERRY": 3,
		}

	def render(self,mode):
		# TODO
		pass
