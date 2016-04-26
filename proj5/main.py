import random
import config
import tictactoe as ttt


player1 = ttt.RandomPlayer();
player2 = ttt.RandomPlayer();
wins = {'P1':0, 'P2':0, 'D':0}

for i in range(1000):
	game = ttt.TicTacToe(player1, player2);
	game.play()

	if player1.won:
		wins['P1'] += 1
	elif player2.won:
		wins['P2'] += 1
	else:
		wins['D'] += 1

print "P1: %d, P2: %d, D: %d" % (wins['P1'], wins['P2'], wins['D'])