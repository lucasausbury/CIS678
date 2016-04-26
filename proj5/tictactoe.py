import random
import config

class Board(object):
	def __init__(self):
		self.wins = [
			(0,1,2), (3,4,5), (6,7,8),
			(0,3,6), (1,4,7), (2,5,8),
			(0,4,8), (2,4,6)
		]
		self.grid = []
		self.reset()

	def reset(self):
		self.grid[:] = []
		self.grid = [None for i in range(9)]
		self.num_moves = 0
		self.states = []

	def play(self, player, index):
		if self.grid[index] is None:
			self.grid[index] = player.mark
			self.num_moves += 1

			self.states.append(self.valid_moves())

			if self.game_over() == 2:
				player.won = True
			else:
				player.reward(0)

	def game_over(self):
		for i,j,k in self.wins:
			if self.grid[i] is not None and self.grid[i]==self.grid[j]==self.grid[k]:
				return 2 # won
		if self.num_moves >= 9:
			return 1 # draw
		else:
			return 0 # still playing

	def valid_moves(self):
		return [i for i in range(0,9) if self.grid[i] is None]

	def get_state(self, offset=None):
		if offset is None:
			return tuple(self.grid)
		else:
			return tuple(self.states[offset])

	def __str__(self):
		out = ''

		for k,v in enumerate(self.grid):
			if k % 3 == 0 and k is not 0:
				out = out + "\n"
			out = out + (" - " if v is None else " %s " % v)

		return out

class RandomPlayer(object):
	def __init__(self, mark, board):
		self.mark = mark
		self.board = board
		self.reset()

	def reset(self):
		self.won = False

	def move(self):
		i = random.choice( self.board.valid_moves() )
		self.board.play(self, i)

	def reward(self, reward):
		return

class LearningPlayer(object):
	def __init__(self, mark, board):
		self.mark = mark
		self.board = board
		self.q = {}
		self.reset()

	def reset(self):
		self.won = False
		self.last_action = None

	def getValue(self, state, action):
		if self.q.get((state, action)) is None:
			self.q[(state, action)] = 1.0
		return self.q.get((state, action))

	def move(self):
		valid_moves = self.board.valid_moves()
		state = self.board.get_state()

		if random.random() < config.EPSILON:
			i = random.choice( valid_moves )
		else:
			values = []

			for a in valid_moves:
				values.append( self.getValue(state, a) )
				maxq = max(values)

				if values.count(maxq) > 1:
					tmp = []
					for i,v in enumerate(values):
						if v == maxq:
							tmp.append(i)
					i = random.choice(tmp)
				else:
					i = values.index(maxq);

		self.board.play(self, i)
		self.last_action = i

	def reward(self, reward):
		final_state = self.board.get_state()
		last_state = self.board.get_state(-1)
		last_value = self.getValue(last_state, self.last_action)

		tmp = []
		for a in list(last_state):
			tmp.append(self.getValue(final_state, a))

		if len(tmp) > 0:
			maxq = max(tmp)
			self.q[(last_state, self.last_action)] = last_value + config.ETA*((reward + config.GAMMA*maxq) - last_value)