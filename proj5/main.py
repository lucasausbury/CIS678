import sys
import tictactoe
import analytics

board = tictactoe.Board()
x_wins = 0
o_wins = 0
draws = 0

if len(sys.argv) < 2:
	games = 1
	verbose = True
else:
	verbose = False
	games = int(sys.argv[1])

for i in range(games):
	board.reset()
	moves = 0
	done = False

	while not done and moves < 9:
		moves += 1

		if moves % 2:
			mark = 'X'
		else:
			mark = 'O'

		board.play_random(mark)

		if verbose:
			print board

		if board.game_won(mark):
			if verbose:
				print "Game over. %s wins!" % mark

			done = True
			if mark == 'X':
				x_wins += 1
			elif mark == 'O':
				o_wins += 1

	if moves == 9 and not done:
		if verbose:
			print "Draw."
		draws += 1

if not verbose:
	print "X: %d\tO: %d\tDraw: %d" % (x_wins, o_wins, draws)