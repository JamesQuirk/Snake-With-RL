"""Module for defining the snake game."""

from .window import SnakeWindow
from .snake import Snake
import random
import numpy as np

class SnakeGame:

	def __init__(self,mode='keys') -> None:
		self.WIN_WIDTH = 800
		self.WIN_HEIGHT = 600

		self.GAME_MODE = mode	# Choice of "keys" or "code". 'Code' requires a function to be called at each frame and return the chosen direction
		self.scale = 10
		self.frame_count = 0
		self.score = 0

		self.rand_seed = 42

		# The 'grid' will define the dimensions of the grid that can contain blocks
		self.GRID_WIDTH = self.WIN_WIDTH // self.scale
		self.GRID_HEIGHT = self.WIN_HEIGHT // self.scale
		self.grid_shape = (self.GRID_HEIGHT,self.GRID_WIDTH)	# (rows,cols)

		self.snake = Snake(self.WIN_WIDTH//2,self.WIN_HEIGHT//2,'e',self.scale)
		self.cherry = None

		self.window = SnakeWindow(self.WIN_WIDTH,self.WIN_HEIGHT)
		if mode == 'keys':
			self.window.bind('<Key>',self.key_handler)
			self.window.after(0,self.render_frame)
			self.window.mainloop()

	def show(self):
		self.window.canvas.delete('all')

		self.draw_snake()
		self.draw_cherry()

	def render_frame(self):
		self.frame_count += 1

		self.window.canvas.delete('all')	# Clear the canvas

		self.draw_snake()
		self.draw_cherry()

		self.window.draw_block(0,0,self.scale,'black')
		self.window.draw_block(0,self.WIN_HEIGHT-self.scale,self.scale,'black')
		self.window.draw_block(self.WIN_WIDTH-self.scale,0,self.scale,'black')
		self.window.draw_block(self.WIN_WIDTH-self.scale,self.WIN_HEIGHT-self.scale,self.scale,'black')

		game_over, _ = self.advance_timestep()

		if game_over:
			print('GAME OVER')
			print('Score:',self.score)
			self.window.after_cancel(self.schedule_id)
			self.window.quit()
		else:
			self.schedule_id = self.window.after(50,self.render_frame)

	def snake_crashed(self) -> bool:
		return self.snake.head.x <= 0 or self.snake.head.x >= self.WIN_WIDTH - self.scale or self.snake.head.y <= 0 or self.snake.head.y >= self.WIN_HEIGHT - self.scale or self.snake.body_collision()

	def cherry_eaten(self) -> bool:
		return self.snake.head.x == self.cherry['x'] and self.snake.head.y == self.cherry['y']

	def place_cherry(self):
		if self.cherry is None:
			random.seed(self.rand_seed)
			self.rand_seed += 1
			x = random.randint(0,self.GRID_WIDTH-2) * self.scale
			y = random.randint(0,self.GRID_HEIGHT-2) * self.scale

			self.cherry = {'x':x,'y':y}

	def draw_cherry(self):
		self.place_cherry()

		self.window.draw_block(self.cherry['x'],self.cherry['y'],self.scale,'red')

	def draw_snake(self):
		self.window.draw_block(self.snake.head.x,self.snake.head.y,self.scale,'blue')
		for block in self.snake.tail:
			self.window.draw_block(block.x,block.y,self.scale,'black')

	def key_handler(self,event):
		# print(event)
		if event.keysym in ('Up','w'):
			self.snake.direction = 'n'
		elif event.keysym in ('Right','d'):
			self.snake.direction = 'e'
		elif event.keysym in ('Down','s'):
			self.snake.direction = 's'
		elif event.keysym in ('Left','a'):
			self.snake.direction = 'w'

	def get_grid_state(self):
		''' Returns the grid with encoded cells showing what is contained. 
		Encodings are as follows:
		- empty = 0
		- snake body/tail = 1
		- snake head = 2
		- cherry = 3
		'''

		grid = np.zeros(shape=self.grid_shape)

		# Add snake's head
		grid[self.snake.head.y//self.scale,self.snake.head.x//self.scale] = 2

		# Add snake's tail
		for block in self.snake.tail:
			grid[block.y//self.scale,block.x//self.scale] = 1
		
		# Add cherry
		grid[self.cherry['y']//self.scale,self.cherry['x']//self.scale] = 3

		return grid

	def advance_timestep(self,action=None):
		''' Method to take a timestep in the game - aimed at code interactions where the gui is not relevant.
		'action': choice of direction to move in or None. 
		'''
		self.place_cherry()
		# print(self.distance_from_cherry())
		self.snake.move(direction=action)

		cherry_eaten = self.cherry_eaten()
		if cherry_eaten:
			self.cherry = None
			self.score += 1
			self.snake.extend_tail()
			self.place_cherry()

		game_over = self.snake_crashed()

		return game_over, cherry_eaten

	def distance_from_cherry(self):
		return np.sqrt( (self.snake.head.x - self.cherry['x'])**2 + (self.snake.head.y - self.cherry['y'])**2 )

if __name__ == '__main__':
	game = SnakeGame()

