import MySQLdb
import math
import numpy as np

db = MySQLdb.connect("localhost","root","","Proj2");
cursor = db.cursor()

# Clear table if exists and (re)build it
cursor.execute("DROP TABLE IF EXISTS Tests_stemmed")
cursor.execute("CREATE TABLE Tests_stemmed ( \
		document    INT AUTO_INCREMENT, \
		word        VARCHAR(128) NOT NULL, \
		class       VARCHAR(32) NOT NULL, \
		count       INT DEFAULT 1, \
    	PRIMARY KEY(document, word) \
	)")

# Read test data line-by-line, break it down into
#     meaningful metrics and insert them into database
document = 0
f = open('test.txt')
for line in iter(f):
	arr = line.split()
	document = document + 1
	actual = ''

	for i, w in enumerate(arr):
		if( i == 0 ):
			actual = w
		else:
			sql = "INSERT INTO Tests_stemmed(document, word, class) VALUES (%d, '%s', '%s') ON DUPLICATE KEY UPDATE count=count+1" % (document, w, actual)
			cursor.execute(sql)
			db.commit()
f.close()
db.close()