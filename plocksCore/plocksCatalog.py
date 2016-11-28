from plocks.plocksCore.plocksNode import PlocksNode

class PlocksCatalog():
	def __init__(self, name):
		if not isinstance(name, str):
			raiseMsg = "Plocks catalog name must be str, not {0}".format(name.__class__.__name__)
			raise TypeError(raiseMsg)

		self._catalog = []
		self._name = name

	def addPlock(self, plockNode):
		exists = False
		if not issubclass(plockNode, PlocksNode):
			raiseMsg = "argument must be a valid PlockNode, not {0}".format(plockNode.__class__.__name__)
			raise TypeError(raiseMsg)

		for idx, node in enumerate(self._catalog):
			if plockNode.__name__ == node.__name__:
				exists = True
		if exists:
			raiseMsg = "Plocks node \"{0}\" already in catalog".format(plockNode.__name__)
			raise ValueError(raiseMsg)
		else:
			self._catalog.append(plockNode)

	def removePlock(self, plockNodeName):
		if not isinstance(plockNodeName, str):
			raiseMsg = "Plocks node name must be str, not {0}".format(plockNodeName.__class__.__name__)
			raise TypeError(raiseMsg)

		exists = None
		for idx, node in enumerate(self._catalog):
			if plockNodeName == node.__name__:
				exists = idx
		
		if exists == None:
			raiseMsg = "could not find Plock node with name {0} in catalog".format(plockNodeName)
			raise ValueError(raiseMsg)
		else:
			self._catalog.pop(exists)

	def getNames(self):
		result = []
		for plock in self._catalog:
			result.append(plock.__name__)
		return result

	def getByName(self, name):
		for plock in self._catalog:
			if plock.__name__ == name:
				return plock

	def __getitem__(self, index):
		if not isinstance(index, int):
			raiseMsg = "catalog indices must be integers, not {0}".format(index.__class__.__name__)
			raise TypeError(raiseMsg)
		if index >= len(self._catalog):
			raiseMsg = "index {0} does not exist in Plocks catalog \"{1}\".".format(index, self._name)
			raise IndexError(raiseMsg)

		return self._catalog[index]

	def __len__(self):
		return len(self._catalog)

	@property
	def name(self):
	    return self._name