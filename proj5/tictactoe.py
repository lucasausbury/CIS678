import random

class Board(object):
	def __init__(self):
		self.grid = []
		self.x_count = 0
		self.o_count = 0
		self.draw_count = 0

		self.reset()

	def reset(self):
		self.grid[:] = []
		self.grid = [[None for i in range(3)] for j in range(3)]

	def play_random(self, mark):
		while True:
			x = random.randint(0,2)
			y = random.randint(0,2)

			if self.grid[y][x] is None:
				break

		self.grid[y][x] = mark

	def game_won(self, mark):
		for y,row in enumerate(self.grid):
			for x,col in enumerate(row):
				if self.grid[x][0] == self.grid[x][1] == self.grid[x][2] == mark:
					return True
				if self.grid[0][y] == self.grid[1][y] == self.grid[2][y] == mark:
					return True
		if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == mark:
			return True
		if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == mark:
			return True
		return False

	def __str__(self):
		out = ''

		for y,row in enumerate(self.grid):
			for x,col in enumerate(row):
				out = out + (" - " if col is None else " %s " % col)
			out = out + "\n"

		return out