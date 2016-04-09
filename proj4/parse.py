import os
import csv

inputs=[]
outputs=[]
classes={}

def buildClasses(d):
	f1 = d+"/training.csv"
	f2 = d+"/test.csv"
	del inputs[:]
	del outputs[:]
	classes.clear()

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
				if i not in classes:
					classes[i]=[]
				if v.isdigit():
					classes[i]=['numeric']
				else:
					if v not in classes[i]:
						classes[i].append(v)

	with open(f2,'rb') as test:
		reader=csv.reader(test)
		for row in reader:
			for (i,v) in enumerate(row):
				if i not in classes:
					classes[i]=[]
				if v.isdigit():
					classes[i]=['numeric']
				else:
					if v not in classes[i] and len(v) > 0:
						classes[i].append(v)
	return classes

def getData(d, f):
	del inputs[:]
	del outputs[:]
	with open(d+"/"+f+".csv",'rb') as train:
		reader=csv.reader(train)
		for row in reader:
			inp = []
			out = []

			for (i,v) in enumerate(row):
				if len(v) > 0:
					if len(classes[i]) == 1:
						if (i+1) == len(row):
							out.append(float(v))
						else:
							inp.append(float(v))
					elif len(classes[i]) == 2:
						if (i+1) == len(row):
							out.append(float(classes[i].index(v)))
						else:
							inp.append(float(classes[i].index(v)))
					else:
						for c in classes[i]:
							if (i+1) == len(row):
								if c == v:
									out.append(1.0)
								else:
									out.append(0.0)
							else:
								if c == v:
									inp.append(1.0)
								else:
									inp.append(0.0)
			inputs.append(inp)
			outputs.append(out)

	return {'inputs':inputs, 'outputs':outputs}