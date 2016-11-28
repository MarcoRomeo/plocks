import unittest
from nose.tools import raises

from plocks.plocksCore.plocksCatalog import PlocksCatalog
from plocks.plocksCore.plocksNode import PlocksNode

class PlocksCatalogTest(unittest.TestCase):
	def setUp(self):
		self._testCatalog = PlocksCatalog("TestCatalog")

	# __init__
	@raises(TypeError)
	def test_init_wrongNameType(self):
		self._testCatalog = PlocksCatalog(123)

	# addPlock
	def test_addPlock(self):
		testNode = PlocksNode("TestNode")
		self._testCatalog.addPlock(testNode)
		assert (self._testCatalog[0] == testNode)

	@raises(TypeError)
	def test_addPlock_wrongNameType(self):
		self._testCatalog.addPlock("strArgument")
	
	@raises(ValueError)
	def test_addPlock_existingName(self):
		testNode1 = PlocksNode("TestNode")
		testNode2 = PlocksNode("TestNode")
		self._testCatalog.addPlock(testNode1)

		self._testCatalog.addPlock(testNode2)

	# removePlock
	def test_removePlock(self):
		testNode1 = PlocksNode("TestNode1")
		testNode2 = PlocksNode("TestNode2")
		self._testCatalog.addPlock(testNode1)
		self._testCatalog.addPlock(testNode2)

		self._testCatalog.removePlock("TestNode1")
		assert (self._testCatalog[0] == testNode2)

	@raises(TypeError)
	def test_removePlock_wrongNameType(self):
		self._testCatalog.removePlock(123)

	@raises(ValueError)
	def test_removePlock_nonExistingName(self):
		testNode1 = PlocksNode("TestNode1")
		self._testCatalog.addPlock(testNode1)

		self._testCatalog.removePlock("WrongName")

	# __getItem__
	def test_getItem(self):
		testNode1 = PlocksNode("TestNode1")
		testNode2 = PlocksNode("TestNode2")
		self._testCatalog.addPlock(testNode1)
		self._testCatalog.addPlock(testNode2)

		assert (self._testCatalog[0] == testNode1)

	@raises(TypeError)
	def test_getItem_wrongIndexType(self):
		testNode1 = PlocksNode("TestNode1")
		self._testCatalog.addPlock(testNode1)

		self._testCatalog["0"]

	@raises(IndexError)
	def test_getItem_wrongIndex(self):
		testNode1 = PlocksNode("TestNode1")
		self._testCatalog.addPlock(testNode1)

		self._testCatalog[1]

	# __len__
	def test_len(self):
		testNode1 = PlocksNode("TestNode1")
		testNode2 = PlocksNode("TestNode2")
		self._testCatalog.addPlock(testNode1)
		self._testCatalog.addPlock(testNode2)
		assert( len(self._testCatalog) == 2)

	# name
	def test_name(self):
		assert(self._testCatalog.name == "TestCatalog")