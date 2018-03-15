from PyQt4 import QtGui, QtCore
import sys

import view_manager
import gui
import argparse

def main():

	parser = argparse.ArgumentParser(description = "Display space points")
        group = parser.add_mutually_exclusive_group()
        parser.add_argument("file", help = "The file you wish " + \
                        "to read.", type = str)
        args = parser.parse_args()

	input_file = args.file

	app = QtGui.QApplication(sys.argv)

	manager = view_manager.view_manager()
	manager.setInputFile(input_file)

	thisgui = gui.gui()
	thisgui.setManager(manager)
	thisgui.initUI()

	manager.eventChanged.connect(thisgui.update)

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
