import MySQLdb
import math
import numpy as np

db = MySQLdb.connect("localhost","root","","Proj2");
cursor = db.cursor()

num_docs = 0
correct = 0
incorrect = 0

# For every class, load P(C) and cache it
p_C = {}
cursor.execute("SELECT class, p_C FROM Words_unstemmed GROUP BY class, p_C")
classes = cursor.fetchall()
for c in classes:
	p_C[c[0]] = math.log(c[1])

# Iterate through each document
cursor.execute("SELECT DISTINCT document FROM Tests_unstemmed")
docs = cursor.fetchall()
for doc in docs:
	actual = ''
	probs = {}

	# Pull every word in this document, along with the number of times
	#   it appears in this document, and p(w|C) for each class.
	#   We are also pulling the actual class for this document and 
	#   storing it for verification.
	sql = "SELECT a.class as actual, b.class, a.count, b.p_wC \
			FROM Tests_unstemmed a, Words_unstemmed b \
			WHERE a.document=%d AND a.word=b.word" % doc
	cursor.execute(sql)
	rows = cursor.fetchall()
	for row in rows:
		actual = row[0]
		probs[row[1]] = probs.get(row[1], p_C[row[1]]) + (row[2] * math.log(row[3]))

	guess = min(probs, key=probs.get)
	num_docs = num_docs + 1
	if guess == actual:
		correct = correct + 1
	else:
		incorrect = incorrect + 1

# Display total accuracy
perc = correct / float(num_docs)
print "ACCURACY: %.4f (%d / %d)" % (perc, correct, num_docs)
db.close()