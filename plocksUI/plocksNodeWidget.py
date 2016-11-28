from PySide import QtCore, QtGui

class proxySignal(QtCore.QObject):
	proxyMoved = QtCore.Signal()
	proxyFrameMouseReleased = QtCore.Signal()
	sender = None


class PlocksNodeItem(QtGui.QGraphicsItem):
	def __init__(self, plockNode, parent=None):
		super(PlocksNodeItem, self).__init__(parent)
		
		self._plock = plockNode
		self._fillColor = QtGui.QColor(0, 255, 0, 255)
		self._outlineColor = QtGui.QColor(50, 255, 50, 255)
		self._size = QtCore.QSize(100, 100)
		self._center = QtCore.QPointF(0, 0)

		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

	def boundingRect(self):
		return QtCore.QRectF(self._center.x(),
							self._center.y(),
							self._size.width(),
							self._size.height())

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
		painter.drawEllipse(self._center.x(),
							self._center.y(),
							self._size.width(),
							self._size.height())

	def setActive(self, status):
		if status:
			self._fillColor = QtGui.QColor(255, 255, 0, 255)
			self._outlineColor = QtGui.QColor(255, 255, 50, 255)
		else:
			self._fillColor = QtGui.QColor(0, 255, 0, 255)
			self._outlineColor = QtGui.QColor(50, 255, 50, 255)