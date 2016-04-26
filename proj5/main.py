import random
import config
import tictactoe

board = tictactoe.Board();
playerX = tictactoe.LearningPlayer("X", board);
playerO = tictactoe.RandomPlayer("O", board);

wins = {'X':0, 'O':0, 'D':0}

for i in range(10000):
	board.reset()
	playerX.reset()
	playerO.reset()

	# randomize who goes first
	if config.RANDOMIZE_START:
		coinflip = random.randint(1,2)
	else:
		coinflip = 1

	if coinflip == 1:
		p1 = playerX
		p2 = playerO
	else:
		p1 = playerO
		p2 = playerX

	while board.game_over() == 0:
		if board.num_moves % 2 == 0:
			p1.move()
		else:
			p2.move()

	if playerX.won:
		playerX.reward(1)
		playerO.reward(-1)
		wins['X'] += 1
	elif playerO.won:
		playerX.reward(-1)
		playerO.reward(1)
		wins['O'] += 1
	else:
		wins['D'] += 1

print "P1: %d, P2: %d, D: %d" % (wins['X'], wins['O'], wins['D'])