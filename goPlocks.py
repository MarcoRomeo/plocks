from PySide import QtCore, QtGui

# plocks imports
from plocks.plocksUI.plocksWidget import MainDialog
from plocks.plocksCore.plocksCatalog import PlocksCatalog
from plocks.plocksCore.plocksNode import PlocksNode
from plocks.plocksCore.plocksNode import PlocksPlug
from plocks.plocksCore import plocksConstants as PC

if __name__ == '__main__':
	
	import sys
	
	app = QtGui.QApplication(sys.argv)
	#app.setWindowIcon(QtGui.QIcon('./icons/plocks_icon.png'))
	dummyPlugs = [PlocksPlug("inPlug1", PC.PlugType.kINTEGER, PC.PlugDirection.kIN),
				  PlocksPlug("outPlug1", PC.PlugType.kINTEGER, PC.PlugDirection.kOUT)]
	class DummyPlock(PlocksNode):
		def __init__(self, name):
			super(DummyPlock, self).__init__(name)
			self._plugs = dummyPlugs

	dummyCatalog = PlocksCatalog("Dummy Catalog")
	dummyCatalog.addPlock(PlocksNode)
	dummyCatalog.addPlock(DummyPlock)
	mainPlocksWdg = MainDialog()
	mainPlocksWdg.newPlocksBoard()
	mainPlocksWdg.boardWidget.setCatalog(dummyCatalog)
	
	plocksWindow = QtGui.QMainWindow(parent=None)
	plocksWindow.setWindowTitle('plocks')
	plocksWindow.resize(1600,900)
	plocksWindow.setCentralWidget(mainPlocksWdg)
	
	plocksWindow.show()
	sys.exit(app.exec_())