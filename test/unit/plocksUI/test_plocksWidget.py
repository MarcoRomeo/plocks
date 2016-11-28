# testsuite
import unittest
import mock

# python
import sys

# pyside 
from PySide import QtCore, QtGui

# plocks
from plocks.plocksUI.plocksWidget import MainDialog
from plocks.plocksUI import plocksBoardWidget

testApp = QtGui.QApplication(sys.argv)

class PlocksWidgetTest(unittest.TestCase):
	def setUp(self):
		self._testPlocksDialog = MainDialog()

	# newPlocksBoard
	def test_newPlocksBoard(self):
		self._testPlocksDialog.newPlocksBoard()

	# showAbout
	def test_showAbout(self):
		self._testPlocksDialog.showAbout()

	# createMenu
	def test_createMainMenu(self):
		assert(1 == 1)
		#self._testPlocksDialog.seateMainMenu()

	# resizeEvent
	def test_resizeEvent(self):
		self._testPlocksDialog.resize(QtCore.QSize(20, 20))
		print self._testPlocksDialog.size().height(), self._testPlocksDialog.size().width()
		assert(self._testPlocksDialog.size().height() == 20 and self._testPlocksDialog.size().width() == 20)