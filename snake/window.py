"""Module for defining the snake game window.
Renders the environment state."""

from tkinter import *

import numpy as np


class SnakeWindow(Tk):
	BLACK = "#000000"
	GREEN = "#048226"
	RED = "red"
	BLUE = "blue"

	def __init__(self,grid_shape,scale=10,x_offset=300,y_offset=250) -> None:
		"""
		:: grid_shape: defines size of environment grid.
		:: scale: used to scale up from env grid size
		:: <offset>: location of window on screen"""
		super().__init__()
		self.frame_count = 0
		self.scale = scale

		self.title('Snake')
		width = (grid_shape[1] + 2) * scale	# '+2' accounts for boarder
		height = (grid_shape[0] + 2) * scale	# '+2' accounts for boarder
		self.geometry(f"{width}x{height}+{x_offset}+{y_offset}")	# "widthxheight+XPOS+YPOS"
		self.configure(bg=SnakeWindow.GREEN)
		
		self.canvas = Canvas(self,width=width,height=height,background=SnakeWindow.GREEN)
		self.canvas.create_rectangle(0,0,width,height,outline=SnakeWindow.BLACK)
		self.canvas.pack(expand=True,fill=BOTH)
		# self.update()

	def _draw_block(self,x,y,colour='red'):
		win_x = x * self.scale
		win_y = y * self.scale
		self.canvas.create_rectangle(
			win_x,
			win_y,
			win_x + self.scale,
			win_y + self.scale,
			fill=colour
		)
		self.canvas.pack()
		self.canvas.update()

	def show(self,state,object_key):
		self.frame_count += 1

		self._draw_state(state,object_key)

	def _draw_state(self,state,key):
		"""Draws SnakeEnv provided state array"""
		self.canvas.delete('all')

		# Insert state into grid with margin to ensure no objects are over edge of screen
		grid = np.zeros((state.shape[0]+2,state.shape[1]+2))
		grid[1:-1,1:-1] = state

		# Draw boarder
		self.canvas.create_rectangle(
			0, 0, grid.shape[1]*self.scale, grid.shape[0]*self.scale, outline=SnakeWindow.BLACK, width=self.scale*2
		)
		self.canvas.pack()
		self.canvas.update()

		# Draw snake
		head_ys, head_xs = np.where(grid  == key["SNAKE_HEAD"])
		print(head_xs[0],head_ys[0])
		self._draw_block(head_xs[0],head_ys[0],colour=SnakeWindow.BLUE)
		for body_y, body_x in np.vstack(np.where( grid == key["SNAKE_BODY"] )).T:
			self._draw_block(body_x,body_y,colour=SnakeWindow.BLACK)

		# Draw cherry
		cherries = np.vstack(np.where( grid == key["CHERRY"] )).T
		if cherries.size > 0:
			for cherry_y, cherry_x in cherries:
				self._draw_block(cherry_x,cherry_y,colour=SnakeWindow.RED)


if __name__ == '__main__':
	snake = SnakeWindow()
