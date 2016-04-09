import sys
import config
import parse
import mlp

if len(sys.argv) < 2:
	sys.exit('Usage: %s directory-name' % sys.argv[0])

d = sys.argv[1]
try:
	classes = parse.buildClasses(d)
	data = parse.getData(d, "training")
	data['classes'] = classes
	nn = mlp.neuralNetwork( data )

	data = parse.getData(d, "test")

	for row in data['inputs']:
		print nn.predict( row )
except Exception as error:
	print error
