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
		error = 1.0

		while epoch < config.EPOCH_THRESHOLD and error > config.ERROR_THRESHOLD:
			prev = error
			error = 0
			cache.clear()
			et = 0
			ec = 0

			for (index,row) in enumerate(inputs):
				e = 0

				# set input values
				for (i,v) in enumerate(row):
						self.layers[0][i+1].value = v

				# calculate result
				l = 1
				while l < len(self.layers):
					for (c,n) in enumerate(self.layers[l]):
						if not n.is_bias:
							n.value = 0
							for n2 in self.layers[l-1]:
								n.value += (n2.value * n2.weights[c-1])
							n.value = self.y(n.value)
					l += 1

				# calculate error and adjust weights
				l = len(self.layers) - 1
				while l >= 0:
					for (c,n) in enumerate(self.layers[l]):
						if c not in cache:
							cache[c] = {}

						if l == len(self.layers)-1:
							n.error = n.value * (1 - n.value) * (outputs[index][c] - n.value)
							e1 = math.pow((outputs[index][c] - n.value), 2)
							e += e1
							et += e1
							ec += 1
							print "%f, %f => %f (%f)" % (outputs[index][c], n.value, e1, e)
							#print "\tACTUAL: %d, PREDICTED: %f, ERROR: %f" %(outputs[index][c], n.value, n.error)
							#print "\t%f * (1 - %f) * (%d - %f)" % (n.value, n.value, outputs[index][c], n.value)
							#print
						else:
							weight_error = 0
							for (wi,wv) in enumerate(n.weights):
								if wi not in cache[c]:
										cache[c][wi] = 0

								if l < (len(self.layers) - 2):
									# connects to hidden layer
									weight_error += (wv * self.layers[l+1][wi+1].error)
									d = config.ETA * self.layers[l+1][wi+1].error * n.value
								else:
									# connects to output layer
									weight_error += (wv + self.layers[l+1][wi].error)
									d = config.ETA * self.layers[l+1][wi].error * self.layers[l+1][wi].value

								if config.MOMENTUM:
									d += config.ALPHA * cache[c][wi]

								n.weights[wi] = wv + d
								cache[c][wi] = d

							n.error = n.value * (1 - n.value) * weight_error
					l -= 1
				print
				error += e
			epoch += 1
			#error = error * .5
			error = et / float(ec)
		print "EPOCH: %d, ERROR: %f" % (epoch, error)
	
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
