import MySQLdb
import Levenshtein

db = MySQLdb.connect("localhost","root","","Proj2");
cursor = db.cursor()

# Clear tables if they exist and (re)build them
cursor.execute("DROP TABLE IF EXISTS Vocab_fuzzed")
cursor.execute("DROP TABLE IF EXISTS Classes_fuzzed")
cursor.execute("DROP TABLE IF EXISTS Words_fuzzed")
vocab_sql = """CREATE TABLE Vocab_fuzzed (
		word     VARCHAR(128) NOT NULL,
		count    INT DEFAULT 1,
    PRIMARY KEY(word)
	)"""
categories_sql = """CREATE TABLE Classes_fuzzed (
		class    VARCHAR(128) NOT NULL,
		docs     INT DEFAULT 1,
		PRIMARY KEY(class)
	)"""
words_sql = """CREATE TABLE Words_fuzzed (
		class    VARCHAR(128) NOT NULL,
		word     VARCHAR(128) NOT NULL,
		count    INT DEFAULT 1,
		p_C      DECIMAL(32,30) DEFAULT 0,
		p_w      DECIMAL(32,30) DEFAULT 0,
		p_wC     DECIMAL(32,30) DEFAULT 0,
		PRIMARY KEY(class, word)
	)"""
data = cursor.execute(vocab_sql)
data = cursor.execute(categories_sql)
data = cursor.execute(words_sql)

# Read training data line-by-line, break it down into
#     meaningful metrics and insert them into database
words = []
f = open('training.txt')
for line in iter(f):
	arr = line.split()
	c = ''
	for i, w in enumerate(arr):
		if( i == 0 ):
			c = w
			sql = "INSERT INTO Classes_fuzzed (class) VALUES('%s') ON DUPLICATE KEY UPDATE docs=docs+1" % w
			cursor.execute(sql)
			db.commit()
		else:
			closest = w
			leven = .6

			if w not in words:
				for k in words:
					l = Levenshtein.ratio(w, k)
					if l > leven:
						closest = k
						leven = l
				words.append( closest )

			if len(closest) > 3:
				sql1 = "INSERT INTO Vocab_fuzzed (word) VALUES('%s') ON DUPLICATE KEY UPDATE count=count+1" % closest
				cursor.execute(sql1)
				db.commit()
				sql2 = "INSERT INTO Words_fuzzed (class, word) VALUES('%s', '%s') ON DUPLICATE KEY UPDATE count=count+1" % (c, closest)
				cursor.execute(sql2)
				db.commit()
			
f.close()
db.close()
