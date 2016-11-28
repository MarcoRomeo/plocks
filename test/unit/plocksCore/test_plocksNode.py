import unittest
from nose.tools import raises

from plocks.plocksCore.plocksNode import PlocksNode
from plocks.plocksCore.plocksNode import PlocksPlug
from plocks.plocksCore import plocksConstants

class PlocksPlugTest(unittest.TestCase):
	def setUp(self):
		self._testPlug = PlocksPlug("TestPlug", 
									plocksConstants.PlugType.kINTEGER,
									plocksConstants.PlugDirection.kIN)

	# init
	@raises(TypeError)
	def test_init_wrongNameType(self):
		self._testPlug = PlocksPlug(123, 
									plocksConstants.PlugType.kINTEGER,
									plocksConstants.PlugDirection.kIN)

	@raises(TypeError)
	def test_init_wrongTypeType(self):
		self._testPlug = PlocksPlug("TestPlug", 
									"wrongType",
									plocksConstants.PlugDirection.kIN)

	@raises(TypeError)
	def test_init_wrongDirectionType(self):
		self._testPlug = PlocksPlug("TestPlug", 
									plocksConstants.PlugType.kINTEGER,
									"wrongDirection")

class PlocksNodeTest(unittest.TestCase):
	def setUp(self):
		self._testNode = PlocksNode("TestNode")

	# init
	@raises(TypeError)
	def test_init_wrongNameType(self):
		self._testNode = PlocksNode(123)

	# name
	def test_name(self):
		assert(self._testNode.name == "TestNode")

	# addPlug
	def test_addPlug(self):
		testPlug = PlocksPlug("TestPlug",
							   plocksConstants.PlugType.kINTEGER,
							   plocksConstants.PlugDirection.kIN)
		self._testNode.addPlug(testPlug)
		assert(self._testNode.getPlug(0) == testPlug)

	@raises(TypeError)
	def test_addPlug_wrongPlugType(self):
		self._testNode.addPlug(123)

	# getPlug
	def test_getPlug(self):
		testPlug = PlocksPlug("TestPlug",
							   plocksConstants.PlugType.kINTEGER,
							   plocksConstants.PlugDirection.kIN)
		self._testNode.addPlug(testPlug)

		assert(self._testNode.getPlug(0) == testPlug)

	@raises(ValueError)
	def test_getPlug_wrongIndex(self):
		testPlug = PlocksPlug("TestPlug",
							   plocksConstants.PlugType.kINTEGER,
							   plocksConstants.PlugDirection.kIN)
		self._testNode.addPlug(testPlug)

		self._testNode.getPlug(1)