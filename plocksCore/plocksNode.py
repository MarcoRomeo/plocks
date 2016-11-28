from plocks.plocksCore import plocksConstants

class PlocksPlug():
	def __init__(self, plugName, plugType, plugDirection):
		if not isinstance(plugName, str):
			raiseMsg = "plug name must be str, not {0}".format(plugName.__class__.__name__)
			raise TypeError(raiseMsg)
		if not isinstance(plugType, int):
			raiseMsg = "plug type must be PlugType, not {0}".format(plugType.__class__.__name__)
			raise TypeError(raiseMsg)
		if not isinstance(plugDirection, int):
			raiseMsg = "plug direction must be PlugDirection, not {0}".format(plugDirection.__class__.__name__)
			raise TypeError(raiseMsg)
		
		self._name = plugName
		self._type = plugType
		self._direction = plugDirection

class PlocksNode(object):
	def __init__(self, name):
		if not isinstance(name, str):
			raiseMsg = "node name must be str, not {0}".format(name.__class__.__name__)
			raise TypeError(raiseMsg)
		self._name = name
		self._type = self.__class__.__name__
		self._plugs = []

	def addPlug(self, plug):
		if not isinstance(plug, PlocksPlug):
			raiseMsg = "plug must be PlockPlug, not {0}".format(plug.__class__.__name__)
			raise TypeError(raiseMsg)
		self._plugs.append(plug)

	def addPlugs(self, plugs):
		if not isinstance(plugs, list):
			raiseMsg = "argument plugs must be a list of PlockPlugs, not {0}".format(plugs.__class__.__name__)
			raise TypeError(raiseMsg)
		for plug in plugs:
			self.addPlug(plug)

	def getPlugs(self):
		return self._plugs

	def getPlug(self, index):
		if index >= len(self._plugs):
			raiseMsg = "plug index {0} does not exist in node".format(index)
			raise ValueError(raiseMsg)
		return self._plugs[index]

	@property
	def name(self):
	    return self._name

	@property
	def type(self):
	    return self._type
	