try:
        import pyqtgraph.opengl as gl
except:
        print "Error, must have pyqtgraph to use this viewer."
        exit(1)

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy
import math

class viewport(gl.GLViewWidget):

	def __init__(self):
		super(viewport, self).__init__()

		# Detector dimensions
		self._x = 48
                self._y = 40/2
                self._z = 90

		# Center view coordinates
		self._xCenter = self._x/2
		self._yCenter = 0
		self._zCenter = self._z/2

	        self.pan(self._xCenter, self._yCenter, self._zCenter)

		self.setBackgroundColor((255,255,255,255))
                self._background_items =  []
                self.drawDetector()
                self.drawAxes()
		self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

	def drawDetector(self):
	
		pts = numpy.array([ [0,-self._y,0], [0,self._y,0],
				    [self._x, self._y,0], [self._x,-self._y,0],
 				    [0,-self._y,0], [0,-self._y,self._z],
				    [0,self._y,self._z], [self._x, self._y,self._z], 
				    [self._x,-self._y,self._z], [0,-self._y,self._z], 
				    [0,-self._y,self._z], [0,-self._y,self._z],
				    [self._x,-self._y,self._z], [self._x,-self._y,0],
			            [self._x,self._y,0], [self._x,self._y,self._z],
				    [0,self._y,self._z], [0,self._y,0] ],
				    dtype=float)	

		for _item in self._background_items:
                        self.removeItem(_item)
                        self._background_items = []

		self._det_outline = gl.GLLinePlotItem(pos=pts,color=(0,0,0,255), width=3)
		self._det_outline.setGLOptions('translucent')
                self.addItem(self._det_outline)
                self._background_items.append(self._det_outline)

	def drawAxes(self):
                self._axes = gl.GLAxisItem()
                self._axes.setSize(self._x,self._y,self._z)
                self.addItem(self._axes)
                self._background_items.append(self._axes)

	def setCenter(self, x, y, z):
		self.opts['center'] = QtGui.QVector3D(0,0,0)
		self._xCenter = float(x)
		self._yCenter = float(y)
		self._zCenter = float(z)
		self.pan(self._xCenter, self._yCenter, self._zCenter)
