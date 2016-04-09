from fuzzywuzzy import fuzz
from fuzzywuzzy import process

classes = {}
f = open('training.txt')
for line in iter(f):
	arr = line.split()
	c = ''
	for i, w in enumerate(arr):
		if( i == 0 ):
			c = w
			classes[c] = ""
		else:
			classes[c] = classes[c] + " " + w
f.close()

docs = 0
correct = 0 
incorrect = 0
f = open('test.txt')
for line in iter(f):
	arr = line.split()
	c = ''
	t = ''

	for i, w in enumerate(arr):
		if i == 0:
			c = w
		else:
			t = t + " " + w

	guess = ''
	conf = 0
	for cls, st in classes:
		f = fuzz.token_set_ratio(st, t)
		if f > conf:
			guess = cls

	if( guess == c ):
		correct = correct + 1
	else:
		incorrect = incorrect + 1
	documents = documents + 1

accuracy = correct / float(documents)
print "%d / %d = %f" % (correct, documents, accuracy)
