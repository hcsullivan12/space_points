import pyqtgraph.opengl as gl
import pyqtgraph as pg

from PyQt4 import QtCore, QtGui

import fileReader
import viewport

import threading
import math
import numpy

class view_manager(QtCore.QObject):

	eventChanged = QtCore.pyqtSignal()
	
	def __init__(self):
		super(view_manager, self).__init__()

		self._event = 0
		self._run = 0
		self._subrun = 0

		self._xCenter = 0
		self._yCenter = 0
		self._zCenter = 0

		self._fileReader = None
		self._input_file = None
		self._events = []
		self._eventItr = 0
		self._currentData = []

		self._gl_hits = None

		self._detectorView = viewport.viewport()

		self._layout = QtGui.QVBoxLayout()
		self._layout.addWidget(self._detectorView)

		self._isCycling = False

	def startCycle(self):
                print "Starting Cycle!"
                self._isCycling = True
                #self._stopCycleFlag = threading.Event()
                #self._cycleWatcher = delayTimer(self._stopCycleFlag, delay)
                #self._cycleWatcher.delayExpired.connect(self.next)
                #self._cycleWatcher.start()
                timer = threading.Timer(2, self.next)
                timer.start()

	def next(self):
                if self._isCycling:
                        timer = threading.Timer(2, self.next)
                        timer.start()
			# Set the next event
			self.nextEvent()
                        # self.goToEvent(self._event + 1)
			self.eventChanged.emit()

        def stopCycle(self):
                print "Stopping Cycle!"
                self._isCycling = False

	def isCycling(self):
                return self._isCycling

	def setInputFile(self, input_file):
		self._input_file = input_file
		self._fileReader = fileReader.fileReader(self._input_file)
		print "Getting events"
		self._events = self._fileReader._events

	def getLayout(self):
		return self._layout	

	def event(self):
		return self._currentData._event

	def run(self):
		return self._currentData._run

	def subrun(self):
		return self._currentData._subrun

	def previousEvent(self):
		# Move to last event
		self._eventItr  = self._eventItr - 1
		# Make sure eventItr > 0 and loops back
                if self._eventItr <= 0:
                        self._eventItr = len(self._events)
		self.setCurrentData()


	def nextEvent(self):
		# Move to next event
		self._eventItr = self._eventItr + 1

		# Make sure eventItr < number of events and loops back
		if self._eventItr > len(self._events):
			self._eventItr = 1
		self.setCurrentData()

	def goToEvent(self, event):
		# Look for event in data
		foundEvent = False
		evtItr = 1
		for evt in self._events:
			if int(evt._event) == int(event):
				self._eventItr = evtItr
				foundEvent = True
			evtItr = evtItr + 1
		if foundEvent:
			self.setCurrentData()
			self.eventChanged.emit()
		else: 
			print "Error, couldn't find event", event

	def setCurrentData(self):
		# Set the data to look at on next update
		self._currentData = self._events[self._eventItr - 1]
	
	def updateVoxel(self):
		# Remove any old data
		if self._gl_hits is not None:
                        self._detectorView.removeItem(self._gl_hits)
                        self._gl_hits = None

		# Get new data
		pt_list = []
		for point in self._currentData._data:
			pt_list.append( point )

		pts = numpy.array(pt_list)
		hits = gl.GLScatterPlotItem(pos=pts,color=(0,0,255,255), size=0.5, pxMode=False)
		hits.setGLOptions('translucent')
		self._gl_hits = hits
		self._detectorView.addItem(self._gl_hits)
		self._detectorView._background_items.append(self._gl_hits)

	def setCenter(self, x, y, z):
		self._detectorView.setCenter(x, y, z)
		#self.updateVoxel()
