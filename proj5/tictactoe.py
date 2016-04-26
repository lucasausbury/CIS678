import random
import config

class TicTacToe(object):
	def __init__(self, player1, player2):
		self.wins = [
			(0,1,2), (3,4,5), (6,7,8),
			(0,3,6), (1,4,7), (2,5,8),
			(0,4,8), (2,4,6)
		]
		self.board = [None for i in range(9)]
		self.num_moves = 0
		self.states = []

		# randomize who goes first
		if config.RANDOMIZE_START:
			coinflip = random.randint(1,2)
		else:
			coinflip = 1

		if coinflip == 1:
			self.pX = player1
			self.pO = player2
		else:
			self.pX = player2
			self.pO = player1

		self.pX.connect(self, 'X')
		self.pO.connect(self, 'O')

	def play(self):
		cont = True
		num_moves = 0

		while cont and num_moves < 9:
			if num_moves % 2 == 0:
				player = self.pX
				opponent = self.pO
			else:
				player = self.pO
				opponent = self.pX

			player.move()
			result = self.game_over()
			if result == 2:
				player.won = True
				player.reward(1)
				opponent.reward(-1)
				cont = False
			elif result == 1:
				player.reward(.5)
				opponent.reward(.5)
				cont = False
			else:
				opponent.reward(0)
			num_moves += 1

	def game_over(self):
		for i,j,k in self.wins:
			if self.board[i] is not None and self.board[i]==self.board[j]==self.board[k]:
				return 2 # won
		if self.num_moves >= 9:
			return 1 # draw
		else:
			return 0 # still playing

	def valid_moves(self):
		return [i for i in range(0,9) if self.board[i] is None]

	def __str__(self):
		out = ''

		for k,v in enumerate(self.board):
			if k % 3 == 0 and k is not 0:
				out = out + "\n"
			out = out + (" - " if v is None else " %s " % v)

		return out

class RandomPlayer(object):
	def connect(self, game, mark):
		self.won = False
		self.game = game
		self.mark = mark

	def move(self):
		i = random.choice( self.game.valid_moves() )
		self.game.board[i] = self.mark

	def reward(self, reward):
		return

class LearningPlayer(object):
	def __init__(self):
		self.q = {}

	def connect(self, game, mark):
		self.won = False
		self.game = game
		self.mark = mark
		self.last_action = None

	def getValue(self, state, action):
		if self.q.get((state, action)) is None:
			self.q[(state, action)] = 1.0
		return self.q.get((state, action))

	def move(self):
		valid_moves = self.game.valid_moves()
		state = self.game.get_state()

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
		final_state = self.game.board.get_state()
		last_state = self.game.board.get_state(-1)
		last_value = self.getValue(last_state, self.last_action)

		tmp = []
		for a in list(last_state):
			tmp.append(self.getValue(final_state, a))

		if len(tmp) > 0:
			maxq = max(tmp)
			self.q[(last_state, self.last_action)] = last_value + config.ETA*((reward + config.GAMMA*maxq) - last_value)