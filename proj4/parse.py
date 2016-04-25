import os
import math
import statistics
import csv
from random import shuffle

inputs=[]
outputs=[]
translate={}

def buildTranslate(d):
	f1 = d+"/training.csv"
	f2 = d+"/test.csv"
	translate.clear()

	if not os.path.isdir(d):
		raise Exception('Directory doesn\'t exist')
	if not os.path.exists(f1):
		raise Exception('Training data doesn\'t exists or is improperly named')
	if not os.path.exists(f2):
		raise Exception('Test data doesn\'t exists or is improperly named')

	with open(f1,'rb') as train:
		reader=csv.reader(train)
		for row in reader:
			for (i,v) in enumerate(row):
				if i not in translate:
					translate[i]={'values':[], 'translations':[], 'type':'classed', 'is_output':False}

				if i == len(row)-1:
					translate[i]['is_output'] = True
				if v not in translate[i]['values']:
					translate[i]['values'].append(v)

	with open(f2,'rb') as test:
		reader=csv.reader(test)
		for row in reader:
			for (i,v) in enumerate(row):
				if i not in translate:
					translate[i]={'values':[], 'translations':[], 'type':'classed'}

				if v not in translate[i]['values']:
					translate[i]['values'].append(v)

	for key, attribute in translate.iteritems():
		all_numeric = True

		for value in attribute['values']:
			all_numeric = all_numeric and unicode(value, 'utf-8').isnumeric()

		# normalize numeric values
		if all_numeric:
			attribute['type'] = 'numeric'
			tmp = [float(i) for i in attribute['values']]
			attribute['mean'] = statistics.mean(tmp)
			attribute['stdev'] = statistics.stdev(tmp)

			for value in attribute['values']:
				if not attribute['is_output']:
					normal = (float(value) - attribute['mean']) / attribute['stdev']
					attribute['translations'].append(normal)
				else:
					attribute['translations'].append(float(value))

		# encode binary attributes
		elif len(attribute['values']) == 2:
			attribute['type'] = 'binary'

			if attribute['is_output']:
				attribute['translations'].extend((0.0, 1.0))
			else:
				attribute['translations'].extend((-1.0, 1.0))
		# binary encode classed attributes
		else:
			num_values = len(attribute['values'])

			for (i,v) in enumerate(attribute['values']):
				if i == num_values-1 and not attribute['is_output']:
					lst = [-1.0] * num_values
				else:
					lst = [0.0] * num_values
					lst[num_values-i-1] = 1.0
				attribute['translations'].append(lst)

	return translate

def getData(directory, file, has_output):
	inputs = []
	outputs = []
	tmp = []

	with open(directory+"/"+file+".csv",'rb') as f:
		reader=csv.reader(f)
		for row in reader:
			tmp.append(row)

	shuffle(tmp)
	for row in tmp:
		inp = []
		out = []

		for (i,v) in enumerate(row):
			value_index = translate[i]['values'].index(v)

			if has_output and i == len(row)-1:
				if isinstance(translate[i]['translations'][value_index], list):
					out += translate[i]['translations'][value_index]
				else:
					out.append(translate[i]['translations'][value_index])
			else:
				if isinstance(translate[i]['translations'][value_index], list):
					inp += translate[i]['translations'][value_index]
				else:
					inp.append(translate[i]['translations'][value_index])
		inputs.append(inp)
		outputs.append(out)

	return {'inputs':inputs, 'outputs':outputs}