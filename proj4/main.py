import sys
import config
import parse
import nn

if len(sys.argv) < 2:
	sys.exit('Usage: %s directory-name' % sys.argv[0])

d = sys.argv[1]
#try:
translate = parse.buildTranslate(d)
data = parse.getData(d, "training", True)

data['translate'] = translate
print data
#nn = nn.neuralNetwork( data )
#print nn

#data = parse.getData(d, "test")

#for row in data['inputs']:
#	print nn.predict( row )
#except Exception as error:
#	print error
