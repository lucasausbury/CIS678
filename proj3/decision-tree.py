import math
import operator
from pprint import pprint

class decisionTree(object):
	class decisionTreeNode(object):
		def __init__(self, attribute, type='discrete'):
			self.attribute = attribute
			self.type = type
			self.values = []

		def addValue(self, node, a, b=None, c=None):
			v = {}
			v['node'] = node
			v['class'] = c

			if self.type == 'discrete':
				v['value'] = a
			else:
				v['min'] = a
				v['max'] = b

			self.values.append(v)

		def predict(self, data):
			a = data[self.attribute]

			for v in self.values:
				if a == v['value']:
					if v['node'] is not None:
						if len(v['node'].values) == 1:
							return "A: " + v['node'].values[0]['class']
						elif len(v['node'].values) == 0:
							return "B: " + v['class']
						else:				
							return v['node'].predict(data)
					else:
						if v['class'] is not None:
							return v['class']
					
			return "NO DATA AVAILABLE"

		def __repr__(self, level=0):
			pre = "\t"*(level)
			ret = ""
			for v in self.values:
				ret = ret + pre + "IF %s EQUALS %s:\n" % (self.attribute, v['value'])

				if v['node'] is not None:
					if len(v['node'].values) == 1:
						ret = ret + pre + "\tRETURN %s\n" % v['node'].values[0]['class']
					elif len(v['node'].values) == 0:
						ret = ret + pre + "\tRETURN %s\n" % v['class']
					else:
						ret = ret + v['node'].__repr__(level+1)
				else:
					if v['class'] is not None:
						ret = ret + pre + "\tRETURN %s\n" % v['class']
					else:
						print v
						ret = ret + pre + "\tNO DATA AVAILABLE\n"
			return ret

	def __init__(self, data, classes, attributes):
		self.data = data
		self.classes = classes
		self.attributes = attributes
		self.root = None

	# Calculates entropy of given dataset
	def entropy(self, data=None):
		counts={}
		total = 0

		if data is None:
			data = self.data

		for d in data:
			if d['class'] not in counts:
				counts[d['class']] = 1
			else:
				counts[d['class']] = counts[d['class']] + 1

		for c in self.classes:
			if c in counts:
				p = counts[c] / float(len(data))
				t = p * (math.log(p) / math.log(2))
				total = total + t

		total = total * -1
		return total

	# Split dataset based on value of given attribute
	def split(self, data, column, value):
		subset = []

		for d in data:
			if d['atts'][column] == value:
				subset.append(d)

		return subset

	# Recursive function to build out nodes of decision tree
	def build(self, data=None, attributes=None, entropy=None, level=0):
		gains = {}
		subs = {}
		ents = {}

		if entropy == 0:
			return

		if data is None:
			data = self.data[:]
		if attributes is None:
			attributes = self.attributes[:]
		if entropy is None:
			entropy = self.entropy()

		for i,a in enumerate(attributes):
			total = 0

			if a is not None:
				if i not in subs:
					subs[i] = {}
					ents[i] = {}

				for v in a['values']:
					subs[i][v] = self.split(data[:], i, v)
					ents[i][v] = self.entropy(subs[i][v][:])

					tmp = (len(subs[i][v]) / float(len(data))) * ents[i][v]
					total = total + tmp

				gains[i] = entropy - total
		
		fulcrum = max(gains, key=gains.get)
		attribute = attributes[fulcrum]
		attributes[fulcrum] = None
		node = self.decisionTreeNode(attribute['name'], attribute['type'])

		if attribute['type'] == 'discrete':
			for value in attribute['values']:
				if len(subs[fulcrum][value]) == 0:
					c = None
				elif len(subs[fulcrum][value]) == 1:
					c = subs[fulcrum][value][0]['class']
				else:
					gs = {}
					for d in data:
						if d['class'] in gs:
							gs[d['class']] = gs[d['class']] + 1
						else:
							gs[d['class']] = 1
					c = max(gs.iteritems(), key=operator.itemgetter(1))[0]
				
				if entropy == 0:
					n = None
				else:
					n = self.build(subs[fulcrum][value][:], attributes[:], ents[fulcrum][value], level+1)

				node.addValue( n, value, None, c )

		if level == 0:
			self.root = node
		else:
			return node

	def predict(self, data):
		return self.root.predict(data)

	def __str__(self):
		if self.root is None:
			return "Empty tree"
		else:
			return self.root.__repr__(0)

count = 0
num_atts = 0
num_data = 0
classes = []
attributes = []
data = []

f = open('contact-lenses.data')
for line in iter(f):
	if count == 1:
		arr = line.split()
		for i,w in enumerate(arr):
			if i > 0:
				classes.append(w)
	if count == 2:
		num_atts = int(line)
	if count > 2 and count <= (num_atts + 2):
		arr = line.split()
		att = {}
		att['name'] = ''
		att['type'] = ''
		att['values'] = []
		num_values = 0

		for i,w in enumerate(arr):
			if i == 1:
				att['name'] = w
			if i == 2:
				num_values = int(w)
				if num_values == 0:
					att['type'] = 'range'
				else:
					att['type'] = 'discrete'
			if i > 2 and i <= (num_values + 2):
				att['values'].append(w)
		attributes.append(att)
	if count == (num_atts + 3):
		num_data = int(line)
	if count > (num_atts + 3) and count <= (num_atts + 3 + num_data):
		arr = line.split()
		d = {}
		d['class'] = ''
		d['atts'] = []

		for i,w in enumerate(arr):
			if i > 0 and i <= num_atts:
				d['atts'].append(w)
			if i > num_atts:
				d['class'] = w
		data.append(d)

	count = count + 1

tree = decisionTree( data, classes, attributes )
tree.build()
print
print tree
print

row = {}
row['age'] = 'presbyopic'
row['prescription'] = 'myope'
row['astigmatism'] = 'no'
row['tear-rate'] = 'normal'
print "Predicting:"
pprint(row)
print "RESULT: %s" % tree.predict(row)