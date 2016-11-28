from PySide import QtCore, QtGui

class proxySignal(QtCore.QObject):
	proxyMoved = QtCore.Signal()
	proxyFrameMouseReleased = QtCore.Signal()
	sender = None


class NodeItem(QtGui.QGraphicsItem):
	def __init__(self, plockNode, parent=None):
		super(NodeItem, self).__init__(parent)
		
		self._plock = plockNode
		
		self._fillColor = QtGui.QColor(200, 200, 200, 255)
		self._outlineColor = QtGui.QColor(100, 100, 100, 255)
		self._textColor = QtGui.QColor(0, 0, 0, 255)
		self._textFont = QtGui.QFont(family="Helvetica",
									 pointSize=10.0)
		self._textFont.setFixedPitch(True)
		self._plugsMargin = 3.0

		self._size = QtCore.QSize(100.0, 100.0)
		self._center = QtCore.QPointF(self._size.width() / 2.0,
									  self._size.height() / 2.0)

		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

	@property
	def size(self):
	    return self._size

	def boundingRect(self):
		return QtCore.QRectF(0.0,
							 0.0,
							 self._size.width(),
							 self._size.height())

	def _paintLabel(self, painter):
		labelPen = painter.pen()
		labelPen.setColor(self._textColor)
		painter.setPen(labelPen)

		nodeName = self._plock.name
		nodeType = "({0})".format(self._plock.type)

		self._textFont.setBold(True)
		fontMetrics = QtGui.QFontMetrics(self._textFont)
		fontHeight = fontMetrics.height()
		nameWidth = fontMetrics.width(nodeName)
		painter.setFont(self._textFont)
		painter.drawText(self._center.x() - nameWidth /2,
						 self._center.y(),
						 nodeName)

		self._textFont.setBold(False)
		fontMetrics = QtGui.QFontMetrics(self._textFont)
		typeWidth = fontMetrics.width(nodeType)
		painter.setFont(self._textFont)
		painter.drawText(self._center.x() - typeWidth /2,
						 self._center.y() + fontHeight,
						 nodeType)

	def _paintPlugs(self, painter):
		nodePlugs = self._plock.getPlugs()
		if nodePlugs:
			for plugId, nodePlug in enumerate(nodePlugs):
				plugBrush = QtGui.QBrush()
				plugBrush	.setStyle(QtCore.Qt.SolidPattern)
				plugColor = QtGui.QColor(255, 0, 0, 255)
				plugBrush.setColor(plugColor)
				painter.setBrush(plugBrush)
				plugSize = QtCore.QSizeF(10.0, 10.0)

				plugPos = QtCore.QPointF(self._center.x() - self._size.width() / 2.0 - self._plugsMargin,
										 self._center.y() - plugSize.height() / 2.0)

				painter.drawEllipse(plugPos.x() - plugSize.width() / 2.0,
									plugPos.y() - plugSize.height() / 2.0,
									plugSize.width(),
									plugSize.height())

	def paint(self, painter, option, widget):
		newPen = QtGui.QPen()
		newPen.setCosmetic(True)
		newPen.setWidth(1)
		newPen.setColor(self._outlineColor)
		painter.setPen(newPen)
		newBrush = painter.brush()
		newBrush.setStyle(QtCore.Qt.SolidPattern)
		newBrush.setColor(self._fillColor)
		painter.setBrush(newBrush)
		painter.drawEllipse(self._center.x() - self._size.width() / 2.0,
							self._center.y() - self._size.height() / 2.0,
							self._size.width(),
							self._size.height())
		self._paintLabel(painter)
		self._paintPlugs(painter)

	def setActive(self, status):
		if status:
			self._fillColor = QtGui.QColor(200, 200, 50, 255)
			self._outlineColor = QtGui.QColor(255, 255, 255, 255)
		else:
			self._fillColor = QtGui.QColor(200, 200, 200, 255)
			self._outlineColor = QtGui.QColor(100, 100, 100, 255)