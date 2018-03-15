from PyQt4 import QtCore, QtGui
import view_manager

class gui(QtGui.QWidget):

	eventChanged = QtCore.pyqtSignal()
	
	def __init(self, manager):
		super(gui, self).__init__()
		self._view_manager = None

	def setManager(self, manager):
		self._view_manager = manager

	def initUI(self):
		self.main_layout = self._view_manager.getLayout()
		self.leftWidget = self.getLeftLayout()

		self.master = QtGui.QVBoxLayout()
		self.slave = QtGui.QHBoxLayout()

		self.slave.addWidget(self.leftWidget)
		self.slave.addLayout(self.main_layout)

		self.master.addLayout(self.slave)

		self.setLayout(self.master)
		self.setGeometry(10, 10, 1500, 1000)
                self.setWindowTitle('Space Points')
                self.setFocus()
                self.show()

	def getLeftLayout(self):
		event_control = self.getEventControlButtons()
                quit_control = self.getQuitButton()

                # New layout
                self._leftLayout = QtGui.QVBoxLayout()
                self._leftLayout.addLayout(event_control)
                self._leftLayout.addStretch(1)
                self._leftLayout.addWidget(quit_control)
                self._leftLayout.setAlignment(QtCore.Qt.AlignLeft)

                self._leftWidget = QtGui.QWidget()
                self._leftWidget.setLayout(self._leftLayout)
                self._leftWidget.setMaximumWidth(200)
                self._leftWidget.setMinimumWidth(100)

		return self._leftWidget

	def getEventControlButtons(self):
		self._goToLabel = QtGui.QLabel("Go to: ")
                self._nextButton = QtGui.QPushButton("Next")
                self._nextButton.clicked.connect(self.nextEvent)
                self._previousButton = QtGui.QPushButton("Previous")
                self._previousButton.clicked.connect(self.previousEvent)
                self._previousButton = QtGui.QPushButton("Previous")
                self._entryBox = QtGui.QLineEdit()
                self._entryBox.setToolTip("Enter an event to skip to")
                self._runLabel = QtGui.QLabel("Run: ")
                self._eventLabel = QtGui.QLabel("Event: ")
                self._subrunLabel = QtGui.QLabel("Subrun: ")

                # Put into layout
                self._eventControlBox = QtGui.QVBoxLayout()

                self._grid = QtGui.QHBoxLayout()
                self._grid.addWidget(self._goToLabel)
                self._grid.addWidget(self._entryBox)

                self._eventControlBox.addLayout(self._grid)
                self._eventControlBox.addWidget(self._nextButton)
                self._eventControlBox.addWidget(self._previousButton)
		self._eventControlBox.addWidget(self._runLabel)
		self._eventControlBox.addWidget(self._subrunLabel)
                self._eventControlBox.addWidget(self._eventLabel)

                return self._eventControlBox

	def getQuitButton(self):
		self._quitButton = QtGui.QPushButton("Quit")
                self._quitButton.setToolTip("Close Event Display")
                self._quitButton.clicked.connect(self.quit)
                return self._quitButton

	def quit(self):
		QtCore.QCoreApplication.instance().quit()

	def nextEvent(self):
		self._view_manager.nextEvent()
		self._view_manager.eventChanged.emit()
		return

	def previousEvent(self):
		return

	def update(self):
                # Change the labels
                eventLabel = "Event: " + str(self._view_manager.event())
                self._eventLabel.setText(eventLabel)
                runLabel = "Run: " + str(self._view_manager.run())
                self._runLabel.setText(runLabel)
                subrunLabel = "Subrun: " + str(self._view_manager.subrun())
                self._subrunLabel.setText(subrunLabel)

                '''# Update the detector and plot view
                self._view_manager.updateVoxel()
                self._view_manager.updatePlot()'''
