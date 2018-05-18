from PyQt4 import QtCore, QtGui
import view_manager

class gui(QtGui.QWidget):

	eventChanged = QtCore.pyqtSignal()
	
	def __init__(self):
		super(gui, self).__init__()
		self._view_manager = None

                self._defaultXView = 24
                self._defaultYView = 0
                self._defaultZView = 45

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
		event_control = self.getEventControlLayout()
		view_control  = self.getViewControlLayout() 
                quit_control  = self.getQuitButton()

                # New layout
                self._leftLayout = QtGui.QVBoxLayout()
                self._leftLayout.addLayout(event_control)
                self._leftLayout.addStretch(1)
		self._leftLayout.addLayout(view_control)
		self._leftLayout.addStretch(1)
                self._leftLayout.addWidget(quit_control)
                self._leftLayout.setAlignment(QtCore.Qt.AlignLeft)

                self._leftWidget = QtGui.QWidget()
                self._leftWidget.setLayout(self._leftLayout)
                self._leftWidget.setMaximumWidth(250)
                self._leftWidget.setMinimumWidth(100)

		return self._leftWidget

	def getViewControlLayout(self):
		self._viewLabel = QtGui.QLabel("View Controls")
		font = QtGui.QFont()
		font.setBold(True)
		self._viewLabel.setFont(font)
		self._viewLabel.setAlignment(QtCore.Qt.AlignCenter)

		self._setCenterLabel = QtGui.QLabel("Set Camera Center")
		self._setCenterLabel.setAlignment(QtCore.Qt.AlignCenter)

		self._xLabel = QtGui.QLabel("X: ")
		self._xEntryBox = QtGui.QLineEdit()
		self._xEntryBox.setText(str(self._defaultXView))
		#self._xEntryBox.returnPressed.connect(self.setViewX)
		self._yLabel = QtGui.QLabel("Y: ")
		self._yEntryBox = QtGui.QLineEdit()
		self._yEntryBox.setText(str(self._defaultYView))
                #self._yEntryBox.returnPressed.connect(self.setViewY)
		self._zLabel = QtGui.QLabel("Z: ")
		self._zEntryBox = QtGui.QLineEdit()
		self._zEntryBox.setText(str(self._defaultZView))
                #self._zEntryBox.returnPressed.connect(self.setViewZ)

		self._unitLabel1 = QtGui.QLabel(" cm")		
		self._unitLabel2 = QtGui.QLabel(" cm")
		self._unitLabel3 = QtGui.QLabel(" cm")

		self._line1 = QtGui.QHBoxLayout()
                self._line1.addWidget(self._xLabel)
                self._line1.addWidget(self._xEntryBox)
		self._line1.addWidget(self._unitLabel1)
		self._line2 = QtGui.QHBoxLayout()
                self._line2.addWidget(self._yLabel)
		self._line2.addWidget(self._yEntryBox)
		self._line2.addWidget(self._unitLabel2)
		self._line3 = QtGui.QHBoxLayout()
                self._line3.addWidget(self._zLabel)
		self._line3.addWidget(self._zEntryBox)
		self._line3.addWidget(self._unitLabel3)

		self._setViewButton = QtGui.QPushButton("Set View")
		self._setViewButton.clicked.connect(self.setView)

		self._setDefaultButton = QtGui.QPushButton("Set Default View")
		self._setDefaultButton.clicked.connect(self.setDefaultView)

		# Put into layout
		self._viewControlBox = QtGui.QVBoxLayout()
		self._viewControlBox.addWidget(self._viewLabel)
		self._viewControlBox.addWidget(self._setCenterLabel)
		self._viewControlBox.addLayout(self._line1)
		self._viewControlBox.addLayout(self._line2)
		self._viewControlBox.addLayout(self._line3)
		self._viewControlBox.addWidget(self._setViewButton)
		self._viewControlBox.addWidget(self._setDefaultButton)

		return self._viewControlBox

	def setView(self):
		x = self._xEntryBox.text()
		y = self._yEntryBox.text()
		z = self._zEntryBox.text()
		self._view_manager.setCenter(x, y, z)

	def setDefaultView(self):
		self._xEntryBox.setText(str(self._defaultXView))
		self._yEntryBox.setText(str(self._defaultYView))
		self._zEntryBox.setText(str(self._defaultZView))
		
		self.setView()

	def getEventControlLayout(self):
		self._eventControlLabel = QtGui.QLabel("Event Controls")
                font = QtGui.QFont()
                font.setBold(True)
                self._eventControlLabel.setFont(font)
                self._eventControlLabel.setAlignment(QtCore.Qt.AlignCenter)

		self._goToLabel = QtGui.QLabel("Go to: ")
                self._nextButton = QtGui.QPushButton("Next")
                self._nextButton.clicked.connect(self.nextEvent)
                self._previousButton = QtGui.QPushButton("Previous")
                self._previousButton.clicked.connect(self.previousEvent)
                self._entryBox = QtGui.QLineEdit()
                self._entryBox.setToolTip("Enter an event to skip to (press enter)")
		self._entryBox.returnPressed.connect(self.goToEvent)
                self._runLabel = QtGui.QLabel("Run: ")
                self._eventLabel = QtGui.QLabel("Event: ")
                self._subrunLabel = QtGui.QLabel("Subrun: ")
		self._eventUpdateButton = QtGui.QPushButton("Start")
		self._eventUpdateButton.clicked.connect(self.eventUpdateButtonHandler)

                # Put into layout
                self._eventControlBox = QtGui.QVBoxLayout()

                self._grid = QtGui.QHBoxLayout()
                self._grid.addWidget(self._goToLabel)
                self._grid.addWidget(self._entryBox)

		self._eventControlBox.addWidget(self._eventControlLabel)
                self._eventControlBox.addLayout(self._grid)
                self._eventControlBox.addWidget(self._nextButton)
                self._eventControlBox.addWidget(self._previousButton)
		self._eventControlBox.addWidget(self._runLabel)
		self._eventControlBox.addWidget(self._subrunLabel)
                self._eventControlBox.addWidget(self._eventLabel)
		self._eventControlBox.addWidget(self._eventUpdateButton)

                return self._eventControlBox

	def eventUpdateButtonHandler(self):
		if self._view_manager.isCycling():
                        self._view_manager.stopCycle()
                        self._eventUpdateButton.setText("Start")

                else:
                        self._eventUpdateButton.setText("Pause")
                        self._view_manager.startCycle()

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
		self._view_manager.previousEvent()
		self._view_manager.eventChanged.emit()
		return

	def goToEvent(self):
		try:
		    event = int(self._entryBox.text())
		except:
		    print "Error, must enter an integer"
		    return
		self._view_manager.goToEvent(event)

	def update(self):
                # Change the labels
                eventLabel = "Event: " + str(self._view_manager.event())
		#print "Event", self._view_manager.event()
                self._eventLabel.setText(eventLabel)

                runLabel = "Run: " + str(self._view_manager.run())
                #print "Run", self._view_manager.run()
                self._runLabel.setText(runLabel)

                subrunLabel = "Subrun: " + str(self._view_manager.subrun())
                self._subrunLabel.setText(subrunLabel)
	        #print "Subrun", self._view_manager.subrun()

                # Update the detector and plot view
                self._view_manager.updateVoxel()
