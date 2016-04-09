RAND_WEIGHT_MIN			= -1
RAND_WEIGHT_MAX			= 1
ACTIVATION_FUNCTION		= 'binary_sigmoid'		# threshold, binary_sigmoid, bipolar_sigmoid, or hyperbolic_tangent
HIDDEN_LAYERS			= 1
HIDDEN_LAYER_SIZE		= 0						# 0 is default (2/3 *[#inputs + #outputs])
MOMENTUM 				= True
ADAPTIVE_LEARNING		= False
ALPHA					= .5					# used for momentum calculation
ETA						= .02					# this is just the initil value if adaptive learning is used
THETA					= 0						# only applicable if using threshold function
EPOCH_THRESHOLD			= 1						# will terminate when either threshold is crossed or when
ERROR_THRESHOLD			= .05					#   error plateaus (use -1 for unlimited epochs)
ADAPTIVE_A 				= .01
ADAPTIVE_B				= .1