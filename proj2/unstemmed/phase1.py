import MySQLdb

db = MySQLdb.connect("localhost","root","","Proj2");
cursor = db.cursor()

# Clear tables if they exist and (re)build them 
cursor.execute("DROP TABLE IF EXISTS Vocab_unstemmed")
cursor.execute("DROP TABLE IF EXISTS Classes_unstemmed")
cursor.execute("DROP TABLE IF EXISTS Words_unstemmed")
vocab_sql = """CREATE TABLE Vocab_unstemmed (
		word     VARCHAR(128) NOT NULL,
		count    INT DEFAULT 1,
    PRIMARY KEY(word)
	)"""
categories_sql = """CREATE TABLE Classes_unstemmed (
		class    VARCHAR(128) NOT NULL,
		docs     INT DEFAULT 1,
		PRIMARY KEY(class)
	)"""
words_sql = """CREATE TABLE Words_unstemmed (
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
f = open('training.txt')
for line in iter(f):
	arr = line.split()
	c = ''
	for i, w in enumerate(arr):
		if( i == 0 ):
			c = w
			sql = "INSERT INTO Classes_unstemmed (class) VALUES('%s') ON DUPLICATE KEY UPDATE docs=docs+1" % w
			cursor.execute(sql)
			db.commit()
		else:
			sql1 = "INSERT INTO Vocab_unstemmed (word) VALUES('%s') ON DUPLICATE KEY UPDATE count=count+1" % w
			cursor.execute(sql1)
			db.commit()
			sql2 = "INSERT INTO Words_unstemmed (class, word) VALUES('%s', '%s') ON DUPLICATE KEY UPDATE count=count+1" % (c, w)
			cursor.execute(sql2)
			db.commit()
			
f.close()
db.close()
