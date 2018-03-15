from PyQt4 import QtCore, QtGui

import fileReader
import viewport

class view_manager(QtCore.QObject):

	eventChanged = QtCore.pyqtSignal()
	
	def __init__(self):
		super(view_manager, self).__init__()

		self._event = 0
		self._run = 0
		self._subrun = 0

		self._fileReader = None
		self._input_file = None
		self._events = []
		self._eventItr = 0
		self._currentData = []

		self._detectorView = viewport.viewport()

		self._layout = QtGui.QVBoxLayout()
		self._layout.addWidget(self._detectorView)

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

	def nextEvent(self):
		print "In nextEvent"
		if self._eventItr >= len(self._events):
			self._eventItr = 0
		self._eventItr = self._eventItr + 1
		self.setCurrentData()

	def setCurrentData(self):
		print "Setting current Data"
		print "EventItr is ", self._eventItr
		print "Length of events is ", len(self._events)
		self._currentData = self._events[self._eventItr - 1]
