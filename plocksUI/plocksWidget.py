from PySide import QtCore, QtGui

import unittest

# plocks imports
from plocks.plocksUI import plocksBoardWidget

class Communicate(QtCore.QObject):
	dataChanged = QtCore.Signal()
	windowResized = QtCore.Signal()
	sender = None

class MainDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		super(MainDialog, self).__init__(parent)

		self.boardWidget = None
		
		self.createMainMenu()
		
		self.mainLayout = QtGui.QVBoxLayout()
		self.mainLayout.setMenuBar(self.menuBar)
		self.setLayout(self.mainLayout)
		
		self.c = Communicate()
		self.c.sender = self

	def _setActions(self):
		self.addAction = QtGui.QAction("&Add new Plock", self, triggered=self.boardWidget.editAddNewNode)
		self.sc_addAction = QtGui.QKeySequence(QtCore.Qt.Key_Tab)
		self.addAction.setShortcut(self.sc_addAction)
		self.editMenu.addAction(self.addAction)
		
		self.remAction = QtGui.QAction("&Remove Plock", self, triggered=self.boardWidget.editRemoveNodes)
		self.sc_remAction = QtGui.QKeySequence(QtCore.Qt.Key_Delete)
		self.remAction.setShortcut(self.sc_remAction)
		self.editMenu.addAction(self.remAction)
		
		self.connectAction = QtGui.QAction("&Connect Plocks", self, triggered=self.boardWidget.editConnectNodes)
		self.sc_connectAction = QtGui.QKeySequence(QtCore.Qt.Key_C)
		self.connectAction.setShortcut(self.sc_connectAction)
		self.editMenu.addAction(self.connectAction)
		
		self.frameAllAction = QtGui.QAction("&Frame all", self, triggered=self.boardWidget.frameAll)
		self.sc_frameAllAction = QtGui.QKeySequence(QtCore.Qt.Key_A)
		self.frameAllAction.setShortcut(self.sc_frameAllAction)
		self.viewMenu.addAction(self.frameAllAction)
		
		self.frameSelectedAction = QtGui.QAction("&Frame selected", self, triggered=self.boardWidget.frameSelected)
		self.sc_frameSelectedAction = QtGui.QKeySequence(QtCore.Qt.Key_F)
		self.frameSelectedAction.setShortcut(self.sc_frameSelectedAction)
		self.viewMenu.addAction(self.frameSelectedAction)
	
	def newPlocksBoard(self):
		self.boardWidget = plocksBoardWidget.MainDialog(self)
		self.boardWidget.setContentsMargins(-10, -10, -10, -10)
		self.mainLayout.addWidget(self.boardWidget)

		self._setActions()

	@unittest.skip("showAbout(self)")
	def showAbout(self):
		aboutDialog = QtGui.QMessageBox.about(self, "plocks", "Some shit here")
			
	def createMainMenu(self):
		self.menuBar = QtGui.QMenuBar()
		
		self.fileMenu = QtGui.QMenu("&File", self)
		self.newAction = QtGui.QAction("&New", self, triggered=self.newBoard)
		
		self.fileMenu.addAction(self.newAction)
		
		self.editMenu = QtGui.QMenu("&Edit", self)
		
		self.viewMenu = QtGui.QMenu("&View", self)
		
		self.optionsMenu = QtGui.QMenu("&Options", self)
		
		self.helpMenu = QtGui.QMenu("&?", self)
		self.aboutAction = self.helpMenu.addAction(QtGui.QAction("&About", self, triggered=self.showAbout))
		
		self.menuBar.addMenu(self.fileMenu)
		self.menuBar.addMenu(self.editMenu)
		self.menuBar.addMenu(self.viewMenu)
		self.menuBar.addMenu(self.optionsMenu)
		self.menuBar.addMenu(self.helpMenu)
	
	def newBoard(self):
		self.newPlocksBoard()
	
	def resizeEvent(self, event):
		self.c.windowResized.emit()
		return super(QtGui.QDialog, self).resizeEvent(event)