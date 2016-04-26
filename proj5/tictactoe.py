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

	def valid_moves(self, board=None):
		if board is None:
			board = self.board

		return [i for i in range(0,9) if board[i] is None]

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
	def connect(self, game, mark):
		self.q = {}
		self.won = False
		self.game = game
		self.mark = mark
		self.last_state = tuple(self.game.board)
		self.last_action = None

	def getValue(self, state, action):
		if self.q.get((state, action)) is None:
			self.q[(state, action)] = 1.0
		return self.q.get((state, action))

	def move(self):
		self.last_state = tuple(self.game.board)
		valid_moves = self.game.valid_moves()
		q_values = []

		for a in valid_moves:
			q_values.append( self.getValue(self.last_state, a) )
			maxq = max(q_values)

			if q_values.count(maxq) > 1:
				tmp = []
				for i,v in enumerate(q_values):
					if v == maxq:
						tmp.append(i)
				i = random.choice(tmp)
			else:
				i = q_values.index(maxq);

		self.game.board[valid_moves[i]] = self.mark
		self.last_action = valid_moves[i]

	def reward(self, reward):
		state = self.last_state
		action = self.last_action
		final_state = tuple(self.game.board)
		prev = self.getValue(state, action)
		maxq = max([self.getValue(final_state, a) for a in self.game.valid_moves(state)])
		self.q[(state, action)] = prev + config.ETA * ((reward + config.GAMMA*maxq) - prev)



#    def reward(self, value, board):
#        if self.last_move:
#            self.learn(self.last_board, self.last_move, value, tuple(board))

#    def learn(self, state, action, reward, result_state):
#        prev = self.getQ(state, action)
#        maxqnew = max([self.getQ(result_state, a) for a in self.available_moves(state)])
#        self.q[(state, action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)