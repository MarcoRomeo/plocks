from PySide import QtCore, QtGui, QtOpenGL
import os

# plocks imports
from plocks.plocksUI.plocksItems import NodeItem
from plocks.plocksUI import plockCompleterWidget
#from plocks.plocksUI import plockConnection


class proxySignal(QtCore.QObject):
	proxyMoved = QtCore.Signal()
	proxyFrameMouseReleased = QtCore.Signal()
	sender = None


class MainDialog(QtGui.QGraphicsView):
	def __init__(self, parent=None):
		super(MainDialog, self).__init__(parent)
		
		self._mouseX = None
		self._mouseY = None
		self.scale(1.0, 1.0)
		self._nodeSize = QtCore.QSize(100, 100)
		
		self._catalog = None
		self._nodes = []
		self.connections = []
		self.selectedNodes = []
		self.selectedConnections = []
		self.newConnectionStart = None
		self.newConnectionEnd = None
		
		self.scene = QtGui.QGraphicsScene(self)
		self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
		
		self.setScene(self.scene)
		self.scene.setSceneRect(-50, -50, 32000, 32000)
		self.boardCenter =  QtCore.QPointF(self.scene.width()/2,
										   self.scene.height()/2)
		self.scene.setStickyFocus(True)
		self.centerOn(0, 0)
		
		self.sceneTransformActive=False
		self.sceneTransformZoom=False
		self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
		self.setRenderHint(QtGui.QPainter.Antialiasing)
		self.setRenderHints(self.renderHints() | QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		self.drawBoard()
		self.centerBoard()
	
	def setCatalog(self, catalog):
		""" Sets the catalog of Plocks nodes available for creation.

			Args:
				catalog (PlocksCatalog): catalog of registered Plock nodes.
		"""
		self._catalog = catalog

	def editAddNewNode(self):
		print self.scene
		mousePosition = self.mapFromGlobal(QtGui.QCursor.pos())
		mousePosition = self.mapToScene(mousePosition)
		print mousePosition.x(), mousePosition.y()
		#relativeMousePosition = sceneRect.x() + mousePosition.x()
		newNode = None
		
		plockClass, ok = plockCompleterWidget.CreateNodeDialog.getNewPlock(self._catalog)
		if ok==True:
			newNode = plockClass(plockClass.__name__)
		
			newNodeItem = NodeItem(newNode)
			newNodeItem.setPos(mousePosition.x() - newNodeItem.size.width() / 2.0, 
								mousePosition.y() - newNodeItem.size.height() / 2.0)
			newNodeItem.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

			self._nodes.append(newNodeItem)
			self.scene.addItem(newNodeItem)
		
	def editConnectNodes(self):
		if (len(self.selectedNodes)>=2):
			for idx in range(len(self.selectedNodes)-1):
				newConnection = None #FIX plockConnection.plockConnection(self.selectedNodes[idx], self.selectedNodes[idx+1], 0, 0, 1)
				self.connections.append(newConnection)
				self.scene.addItem(newConnection)
				newConnection.update()
				
	def editRemoveNodes(self):
		if (len(self.selectedNodes)>0):
			nodesToDelete = []
			connectionsToDelete = []
			for node in self.selectedNodes:
				for connection in self.connections:
					toBeDeleted = False
					if connectionsToDelete.count(connection)==0:
						if connection.iNode == node:
							toBeDeleted = True
						if connection.oNode == node:
							toBeDeleted = True
						if toBeDeleted:
							connectionsToDelete.append(connection)
				nodesToDelete.append(node)
				
			for item in nodesToDelete:
				nodeIndex = self._nodes.index(item)
				self._nodes.remove(item)
				self.scene.removeItem(item)
				self.nodeNames.pop(nodeIndex)
				
			for item in connectionsToDelete:
				self.connections.remove(item)
				self.scene.removeItem(item)
			self.selectedNodes = []
			
		if (len(self.selectedConnections)>0):
			for connection in self.selectedConnections:
				self.connections.remove(connection)
				self.scene.removeItem(connection)
			self.selectedConnections = []
				
				
	def updateBoard(self):
		dirtyNode = self.sender().sender
		for connection in self.connections:
			if connection.iNode==dirtyNode:
				connection.update()

	def setBoardType(self, type):
		self.boardType = type
		
	def createPanels(self):
		self.loadNodes()
		self.arrangeFromStoredPositions()
		self.connectNodes()
		self.setWorkarea()
		self.fitBoard()
		self.frameAll()

	def mousePressEvent(self, event):
		if event.modifiers()!=QtCore.Qt.ALT:
			if event.button()==QtCore.Qt.LeftButton:
				if event.modifiers()==QtCore.Qt.SHIFT:
					self.changeSelection(event, 'add')
				else:
					self.changeSelection(event, 'replace')
			if event.button()==QtCore.Qt.MiddleButton:
				for node in self._nodes:
					nodeGeometry = self.getNodeGeometry(node)
					if nodeGeometry.contains(event.globalPos()):
						mappedPos = self.mapToScene(event.pos())
						inPlugIdx = node.widget().checkInPlugs(mappedPos)
						if inPlugIdx!=None:
							self.newConnectionEnd = (node, inPlugIdx)
							break
						outPlugIdx = node.widget().checkOutPlugs(mappedPos)
						if outPlugIdx!=None:
							self.newConnectionStart = (node, outPlugIdx)
							break
				
		return super(MainDialog, self).mousePressEvent(event)
	
	def mouseReleaseEvent(self, event):
		if event.modifiers()!=QtCore.Qt.ALT:
			if event.button()==QtCore.Qt.MiddleButton:
				if self.newConnectionStart != None or self.newConnectionEnd != None:
					for node in self._nodes:
						nodeGeometry = self.getNodeGeometry(node)
						if nodeGeometry.contains(event.globalPos()):
							mappedPos = self.mapToScene(event.pos())
							if self.newConnectionStart!=None:
								inPlugIdx = node.widget().checkInPlugs(mappedPos)
								if inPlugIdx!=None:
									self.newConnectionEnd = (node, inPlugIdx)
									newConnection = None #FIX plockConnection.plockConnection(self.newConnectionStart[0], self.newConnectionEnd[0], self.newConnectionStart[1], self.newConnectionEnd[1], 1)
									self.connections.append(newConnection)
									self.scene.addItem(newConnection)
									newConnection.update()
									break
							if self.newConnectionEnd!=None:
								outPlugIdx = node.widget().checkInPlugs(mappedPos)
								if outPlugIdx!=None:
									self.newConnectionStart = (node, outPlugIdx)
									newConnection = None #FIX plockConnection.plockConnection(self.newConnectionStart[0], self.newConnectionEnd[0], self.newConnectionStart[1], self.newConnectionEnd[1], 1)
									self.connections.append(newConnection)
									self.scene.addItem(newConnection)
									newConnection.update()
									break
				self.newConnectionStart = None
				self.newConnectionEnd = None
				
		return super(MainDialog, self).mouseReleaseEvent(event)
		
		
	def mouseMoveEvent(self, event):
		if event.modifiers()==QtCore.Qt.AltModifier:
			if self._mouseX==None:
				self._mouseX = event.globalX()
				self._mouseY = event.globalY()
			else:
				mouseDiffY = event.globalY()-self._mouseY
				if mouseDiffY < -100.0:
					mouseDiffY = -100.0
				if mouseDiffY > 100.0:
					mouseDiffY = 100.0
				mouseDiffX = event.globalX()-self._mouseX
				if mouseDiffX < -100.0:
					mouseDiffX = -100.0
				if mouseDiffX > 100.0:
					mouseDiffX = 100.0
		
			if event.buttons() & QtCore.Qt.LeftButton:
				if event.buttons() & QtCore.Qt.MiddleButton:
					self.setTransformationAnchor(QtGui.QGraphicsView.AnchorViewCenter)
					zoomValue = 1.0+float(mouseDiffY)/500.0
					self.scale(zoomValue, zoomValue)
				else:
					'left button'
			elif event.buttons() & QtCore.Qt.MiddleButton:
				if event.buttons() & QtCore.Qt.LeftButton:
					self.setTransformationAnchor(QtGui.QGraphicsView.AnchorViewCenter)
					zoomValue = 1.0+float(mouseDiffY)/500.0
					self.scale(zoomValue, zoomValue)
				else:
					self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
					self.translate(int(mouseDiffX), int(mouseDiffY))
				
			elif event.buttons() & QtCore.Qt.RightButton:
				self.setTransformationAnchor(QtGui.QGraphicsView.AnchorViewCenter)
				zoomValue = 1.0+float(mouseDiffY)/500.0
				self.scale(zoomValue, zoomValue)
					
		self._mouseX = event.globalX()
		self._mouseY = event.globalY()
		return super(MainDialog, self).mouseMoveEvent(event)
	
	
	def event(self, event): 
		""" little, small, tricky, and crucial piece of code to avoid QT from crushing whenever 
			the ALT, CTRL, SHIFT and TAB keys are pressed editing a widget inside a graphicsItem
		"""
		try:
			if event.type()==QtCore.QEvent.KeyPress:
				return super(MainDialog, self).event(event)
			return super(MainDialog, self).event(event)
		except:
			return True
	
	def paintEvent(self, event):
		for c in self.connections:
			c.drawConnection()
			
		self.updateScene([self.scene.sceneRect()])
		
		return super(MainDialog, self).paintEvent(event)
	
	def changeSelection(self, event, mode):
		newItem = None
		selectedNode = None
		
		if (mode=='replace'):
			self.selectedNodes = []
			self.selectedConnections = []
		
		for node in self._nodes:
			nodeGeometry = self.getNodeGeometry(node)
			if nodeGeometry.contains(event.globalPos()):
				node.setSelected(True)
				selectedNode = node
				#node.setShadow(True)
				node.setActive(True)
				if self.selectedNodes.count(node)==0:
					self.selectedNodes.append(node)
				found=True
			else:
				if (mode=='replace'):
					node.setSelected(False)
					#node.setShadow(False)
					node.setActive(False)
		
		for connection in self.connections:
			mappedEventPos = self.mapToScene(event.pos())
			if connection.isNear(mappedEventPos, 20) and selectedNode == None:
				connection.setSelected(True)
				connection.setActive(True)
				if self.selectedConnections.count(connection)==0:
					self.selectedConnections.append(connection)
				found=True
			else:
				if (mode=='replace'):
					connection.setSelected(False)
					connection.setActive(False)

	def destroy(self):
		for node in self._nodes:
			self.scene.removeItem(node)
			
		self.panels = None
		self.items = None
		self.orderedItems = None
		self.panelsData = None
		self.orderedItems = None
		
		self.scene = None
		self.data = None
		
	def drawBoard(self):
		self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(45, 45, 45)))
		backgroundCanvas = QtGui.QGraphicsRectItem(self.scene.sceneRect())

		thePath = os.path.join(os.path.dirname(__file__), '../resources/icons/plocks_logo_transparent.png')
		pixmap = QtGui.QPixmap(thePath)
		backgroundPixmap = QtGui.QGraphicsPixmapItem(pixmap)
		backgroundPixmap.setPos(self.scene.sceneRect().center()-pixmap.rect().center())
		self.scene.addItem(backgroundPixmap)

		self.scene.addItem(backgroundCanvas)

	def centerBoard(self):
		self.centerOn(self.boardCenter.x(), self.boardCenter.y())
	
	def fitBoard(self):
		self.computeActiveItemsBBox()
		#self.computeInactiveItemsBBox()
		self.scene.items()[0].setRect(QtCore.QRectF( self.activeItemsBBox.x()-100, self.activeItemsBBox.y()-100, self.activeItemsBBox.width()+200, self.activeItemsBBox.height()+200))
	
	def frameSelected(self):
		bBox = self.computeSelectedNodesBBox()
		if bBox!=None:
			self.fitInView(bBox, QtCore.Qt.KeepAspectRatio)
		
	def frameAll(self):
		bBox = self.computeAllNodesBBox()
		if bBox!=None:
			self.fitInView(bBox, QtCore.Qt.KeepAspectRatio)
					
	def computeAllNodesBBox(self):
		allItemsBBox=None
		for node in self._nodes:
			nodeX = node.pos().x()
			nodeY = node.pos().y()
			nodeW = node.widget().width()
			nodeH = node.widget().height()
			nodeRect = QtCore.QRect(nodeX, nodeY, nodeW, nodeH)
			if allItemsBBox==None:
				allItemsBBox = nodeRect
			else:
				allItemsBBox|=nodeRect
		return allItemsBBox
				
	def computeSelectedNodesBBox(self):
		selItemsBBox=None
		for node in self._nodes:
			if node.isSelected():
				nodeX = node.pos().x()
				nodeY = node.pos().y()
				nodeW = node.widget().width()
				nodeH = node.widget().height()
				nodeRect = QtCore.QRect(nodeX, nodeY, nodeW, nodeH)
				if selItemsBBox==None:
					selItemsBBox = nodeRect
				else:
					selItemsBBox|=nodeRect
		return selItemsBBox
		
		
	def getNodeGeometry(self, node):
		view = self.scene.views()[0]
		sceneBottomRight = node.mapToScene(node.boundingRect().bottomRight())
		viewBottomRight = view.mapFromScene(sceneBottomRight)
		relativeBottomRight = view.viewport().mapToGlobal(viewBottomRight)
		sceneTopLeft = node.mapToScene(node.boundingRect().topLeft())
		viewTopLeft = view.mapFromScene(sceneTopLeft)
		relativeTopLeft = view.viewport().mapToGlobal(viewTopLeft)
		relativeGeometry = QtCore.QRect(relativeTopLeft, relativeBottomRight)
		return relativeGeometry