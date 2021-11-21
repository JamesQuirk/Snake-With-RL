"""Module for defining the snake itself."""
import numpy as np

class SnakeBlock:
	def __init__(self,x,y) -> None:
		self.x = x
		self.y = y

	def __str__(self) -> str:
		return f"SnakeBlock({self.x},{self.y})"

class Snake:

	def __init__(self,x,y,direction):
		self.head = SnakeBlock(x,y)

		if direction == 'n':
			self.tail = [SnakeBlock(x,y+1)]
		elif direction == 's':
			self.tail = [SnakeBlock(x,y-1)]
		elif direction == 'e':
			self.tail = [SnakeBlock(x-1,y)]
		elif direction == 'w':
			self.tail = [SnakeBlock(x+1,y)]

		self.direction = direction

		self.pending_extension = False

	def __str__(self) -> str:
		return str([str(b) for b in self.tail]) + " " + str(self.head)

	def move(self,direction=None,callback=None):
		if direction is None or (direction == 'n' and self.direction == 's') or (direction == 's' and self.direction == 'n') or (direction == 'e' and self.direction == 'w') or (direction == 'w' and self.direction == 'e'):
			direction = self.direction
		else:
			self.direction = direction

		# print(f"Snake moving {direction}")

		self.tail.insert(0,SnakeBlock(self.head.x,self.head.y))	# Insert block behind head
		if not self.pending_extension:
			# If not extending tail then remove last block.
			self.removed_block = self.tail.pop(-1)
		else:
			self.removed_block = None
			self.pending_extension = False
		
		if direction == 'n':
			self.head.y -= 1
		elif direction == 's':
			self.head.y += 1
		elif direction == 'e':
			self.head.x += 1
		elif direction == 'w':
			self.head.x -= 1

		if callback is not None:
			callback()
		return self.body_collision()

	def extend_tail(self):
		self.pending_extension = True

	def body_collision(self) -> bool:
		for block in self.tail:
			if self.head.x == block.x and self.head.y == block.y:
				# print('Collision with body!')
				return True
		return False

	def distance_from(self,item):
		return np.sqrt( (self.head.x - item.x)**2 + (self.head.y - item.y)**2 )

