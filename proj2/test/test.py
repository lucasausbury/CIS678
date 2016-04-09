import math

documents = []
classes = {}
vocab = {}

f = open('training.txt')
for line in iter(f):
	arr = line.split()
	doc = {}

	for i, w in enumerate(arr):
		if( i == 0 ):
			doc['actual'] = w
			doc['vocab'] = {}

			if w in classes:
				classes[w]['count'] = classes[w]['count'] + 1
			else:
				classes[w] = {}
				classes[w]['count'] = 1
				classes[w]['word_count'] = 0
				classes[w]['vocab'] = {}
		else:
			if w in doc['vocab']:
				doc['vocab'][w] = doc['vocab'][w] + 1
			else:
				doc['vocab'][w] = 1

			if w in classes[doc['actual']]['vocab']:
				classes[doc['actual']]['vocab'][w] = classes[doc['actual']]['vocab'][w] + 1
			else:
				classes[doc['actual']]['vocab'][w] = 1
			classes[doc['actual']]['word_count'] = classes[doc['actual']]['word_count'] + 1

			if w in vocab:
				vocab[w] = vocab[w] + 1
			else:
				vocab[w] = 1

	documents.append(doc)
f.close()

# Constants
V = len(vocab)
D = len(documents)
P = sum(vocab.values())

# Test variables
total = 0
correct = 0

f = open('test.txt')
for line in iter(f):
	arr = line.split()
	actual = ''
	guess = ''
	guesses = {}

	for i, w in enumerate(arr):
		if( i == 0 ):
			actual = w
		else:
			for ci, co in classes.iteritems():
				pC = math.log(co['count']) - math.log(D)
				#pw = math.log(vocab[w]) - math.log(P)
				if w in co['vocab']:
					pwC = math.log(co['vocab'][w] + 1) - math.log(co['word_count'] + V)
				else:
					pwC = 0

				if ci not in guesses:
					guesses[ci] = pC
				else:
					guesses[ci] = guesses[ci] + pwC

	if len(guesses) > 0:
		guess = min(guesses, key=guesses.get)
		total = total + 1
		if guess == actual:
			correct = correct + 1
f.close()

accuracy = 100 * (correct / float(total))
print "ACCURACY: %2f percent (%d / %d)" % (accuracy, correct, total)