import math
import random
import config
import functions

class neuralNetwork(object):
	class neuralNetworkNode(object):
		def __init__(self, connections):
			self.value = 0.0
			self.error = 1.0
			self.weights = []
			self.is_bias = False

			while len(self.weights) < connections:
				weight = random.uniform(config.RAND_WEIGHT_MIN, config.RAND_WEIGHT_MAX)
				self.weights.append(weight)
	
	def __init__(self, data):
		self.layers = []
		self.translate = data['translate']
		i_size = len(data['inputs'][0])
		o_size = len(data['outputs'][0])

		if config.HIDDEN_LAYER_SIZE == 0:
			config.HIDDEN_LAYER_SIZE = math.floor((2/float(3)) * (i_size + o_size))

		if config.ACTIVATION_FUNCTION == 'threshold':
			self.y = functions.threshold
		elif config.ACTIVATION_FUNCTION == 'binary_sigmoid':
			self.y = functions.binary_sigmoid
		elif config.ACTIVATION_FUNCTION == 'bipolar_sigmoid':
			self.y = functions.bipolar_sigmoid
		elif config.ACTIVATION_FUNCTION == 'hyperbolic_tangent':
			self.y = functions.hyperbolic_tangent
		else:
			raise Exception("Invalid ACTIVATION FUNCTION provided")

		# build input layer
		bias = self.neuralNetworkNode(config.HIDDEN_LAYER_SIZE)
		bias.value = 1.0
		bias.is_bias = True
		self.layers.append([bias])
		while len(self.layers[0]) < (i_size + 1):
			self.layers[0].append(self.neuralNetworkNode(config.HIDDEN_LAYER_SIZE))

		# build hidden layers
		l = 1
		while l < (config.HIDDEN_LAYERS + 1):
			if l == config.HIDDEN_LAYERS:
				# will be connecting to output layer
				size = o_size
			else: 
				# will be connecting to another hidden layer
				size = config.HIDDEN_LAYER_SIZE

			bias = self.neuralNetworkNode(size)
			bias.value = 1.0
			bias.is_value = True
			self.layers.append([bias])
			while len(self.layers[l]) < (config.HIDDEN_LAYER_SIZE + 1):
				self.layers[l].append(self.neuralNetworkNode(size))
			l += 1

		# build output layer
		self.layers.append([])
		while len(self.layers[l]) < o_size:
			self.layers[l].append(self.neuralNetworkNode(0))

		self.train( data['inputs'], data['outputs'] )

	def train(self, inputs, outputs):
		epoch = 0
		error_avg = 1.0
		error_ttl = 0
		error_cnt = 0

		while epoch < config.EPOCH_THRESHOLD and error_avg > config.ERROR_THRESHOLD:
			for (index,row) in enumerate(inputs):
				error = 0
				# set input values
				for (i,v) in enumerate(row):
					self.layers[0][i+1].value = v

				# calculate result
				for (i,l) in enumerate(self.layers):
					if i > 0:
						for (j,n) in enumerate(l):
							if not n.is_bias:
								n.value = 0
								for inp in self.layers[i-1]:
									n.value += (inp.value * inp.weights[j-1])
								n.value = self.y(n.value)

				# calculate error
				for (i,l) in reversed(list(enumerate(self.layers))):
					if i > 0:
						for (j,n) in enumerate(l):
							if i == len(self.layers)-1:
								actual = outputs[index][j]
								n.error = (actual - n.value) * n.value * (1 - n.value)
								error += (.5 * math.pow((n.value - actual), 2))
								#print "RETURNED: %f, SHOULD BE: %f" % (n.value, actual)
							else:
								out = self.layers[i+1]
								weights = 0
								for (k,w) in enumerate(n.weights):
									weights += w * out[k].error

									# adjust weight
									n.weights[k] = w + config.ETA * out[k].error * n.value
									#print "\t%f, %f => %f" % (w, out[k].error, n.weights[k])

								n.error = n.value * (1 - n.value) * weights
						#print "ERROR: " + str(error)
				error_ttl += error
				error_cnt += 1
			error_avg = error_ttl / float(error_cnt)
			epoch += 1
			print "AVG ERROR: " + str(error_avg)
		print "EPOCHS: " + str(epoch)

	def predict(self, data):
		# set input layer values
		for (i,v) in enumerate(data):
			self.layers[0][i+1].value = v

		l = 1
		while l < len(self.layers):
			for (c,n) in enumerate(self.layers[l]):
				if not n.is_bias:
					n.value = 0
					for n2 in self.layers[l-1]:
						n.value += (n2.value * n2.weights[c-1])
					n.value = self.y(n.value)
			l += 1

		out = str(data) + "\n"
		for (i,n) in enumerate(self.layers[len(self.layers)-1]):
			out += "\tLABEL: %s, VALUE: %f, ERROR: %f\n" % (self.classes[len(self.classes)-1][i], n.value, n.error)
		return out

	def __str__(self):
		out = ''

		for layer in self.layers:
			for node in layer:
				rounded = ['%.4f' % elem for elem in node.weights]

				out = out + "VALUE: " + str(node.value) + "\n"
				out = out + "ERROR: " + str(node.error) + "\n"
				out = out + "WEIGHTS: " + str(rounded) + "\n"
				out = out + "\n"
			out = out + "%i NODES\n" % len(layer)
			out = out + "\n"
		out = out + "%i LAYERS" % len(self.layers)

		return out
