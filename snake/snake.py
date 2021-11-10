"""Module for defining the snake itself."""

class SnakeBlock:
	def __init__(self,x,y) -> None:
		self.x = x
		self.y = y


class Snake:

	def __init__(self,x,y,direction,scale=10):
		self.head = SnakeBlock(x,y)
		self.scale = scale

		if direction == 'n':
			self.tail = [SnakeBlock(x,y+scale)]
		elif direction == 's':
			self.tail = [SnakeBlock(x,y-scale)]
		elif direction == 'e':
			self.tail = [SnakeBlock(x-scale,y)]
		elif direction == 'w':
			self.tail = [SnakeBlock(x+scale,y)]

		self.direction = direction

		self.pending_extension = False

	def move(self,direction=None):
		if direction is None or (direction == 'n' and self.direction == 's') or (direction == 's' and self.direction == 'n') or (direction == 'e' and self.direction == 'w') or (direction == 'w' and self.direction == 'e'):
			direction = self.direction
		else:
			self.direction = direction

		self.tail.insert(0,SnakeBlock(self.head.x,self.head.y))	# Insert block behind head
		if not self.pending_extension:
			# If not extending tail then remove last block.
			self.tail.pop(-1)
		else:
			self.pending_extension = False
		
		if direction == 'n':
			self.head.y -= self.scale
		elif direction == 's':
			self.head.y += self.scale
		elif direction == 'e':
			self.head.x += self.scale
		elif direction == 'w':
			self.head.x -= self.scale

	def extend_tail(self):
		self.pending_extension = True

	def body_collision(self) -> bool:
		for block in self.tail:
			if self.head.x == block.x and self.head.y == block.y:
				# print('Collision with body!')
				return True
		return False
