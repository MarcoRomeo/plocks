from PySide import QtCore, QtGui

class CreateNodeDialog(QtGui.QDialog):
	def __init__(self, plocksCatalog, parent=None):
		""" 
		"""
		super(CreateNodeDialog, self).__init__(parent)
		self.setModal(False)
		self._plocksCatalog = plocksCatalog
		
		self.commandsComplete = QtGui.QCompleter(self._plocksCatalog.getNames())
		self.commandsComplete.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		
		self.commandSelect = QtGui.QLineEdit()
		self.commandSelect.setCompleter(self.commandsComplete)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(self.commandSelect)
		self.setLayout(mainLayout)
		
		self.setWindowTitle("Create new Plock")
		self.commandSelect.returnPressed.connect(self.accept)
	
	def getPlock(self):
		plock = self._plocksCatalog.getByName(self.commandSelect.text())
		return (plock)
		
	@staticmethod
	def getNewPlock(data, parent = None):
		dialog = CreateNodeDialog(data, parent)
		result = dialog.exec_()
		newCommand = dialog.getPlock()
		return (newCommand, result == QtGui.QDialog.Accepted)