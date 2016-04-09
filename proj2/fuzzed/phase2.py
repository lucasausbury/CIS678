import MySQLdb
import math
import numpy as np

db = MySQLdb.connect("localhost","root","","Proj2");
cursor = db.cursor()

# Get constant data
cursor.execute("SELECT COUNT(word) FROM Vocab_stemmed")
row = cursor.fetchone()
Vocabulary = row[0]

cursor.execute("SELECT SUM(docs) FROM Classes_stemmed")
row = cursor.fetchone()
Documents = row[0]

cursor.execute("SELECT SUM(count) FROM Vocab_stemmed")
row = cursor.fetchone()
Positions = row[0]

# Get number of documents per class and cache it
Documents_j = {}
cursor.execute("SELECT class, docs FROM Classes_stemmed")
rows = cursor.fetchall()
for row1 in rows:
	Documents_j[row1[0]] = row1[1]

# Get word counts and cache them
word_counts = {}
cursor.execute("SELECT word, count FROM Vocab_stemmed")
rows = cursor.fetchall()
for row in rows:
	word_counts[row[0]] = row[1]

# For every class/word combination, calculate P(C|w)
sql = "SELECT class, word, count FROM Words_stemmed"
cursor.execute(sql)

rows = cursor.fetchall()
for row in rows:
	c = row[0]
	w = row[1]
	n_k = row[2]

	p_C  = np.divide(Documents_j[c], float(Documents))
	p_w  = np.divide(word_counts[w], float(Positions))
	p_wC = np.divide((n_k + 1), float(Positions + Vocabulary))

	sql = "UPDATE Words_stemmed SET p_C=%f, p_w=%f, p_wC=%f WHERE class='%s' AND word='%s'" % (p_C, p_w, p_wC, c, w)
	cursor.execute(sql)
	db.commit()

db.close()
