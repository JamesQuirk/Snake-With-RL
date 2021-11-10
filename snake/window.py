"""Module for defining the snake game window"""

from tkinter import *

class SnakeWindow(Tk):
	def __init__(self,width=800,height=600,x_offset=300,y_offset=250) -> None:
		super().__init__()
		self.title('Snake')
		self.geometry(f"{width}x{height}+{x_offset}+{y_offset}")	# "widthxheight+XPOS+YPOS"
		# self.configure(bg='#048226')
		
		self.canvas = Canvas(self,width=width,height=height,background='#048226')
		self.canvas.pack(expand=True,fill=BOTH)


	def draw_block(self,x,y,size,colour='red'):
		self.canvas.create_rectangle(x,y,x+size,y+size,fill=colour)
		self.canvas.pack()
		self.canvas.update()


if __name__ == '__main__':
	snake = SnakeWindow()
