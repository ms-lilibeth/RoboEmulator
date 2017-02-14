# import emulator.interface as UI
from interface import BoardWidget, MainView
from emulator import Emulator
import sys
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
e = Emulator("some")
# e = MainView("smth", 10, 8)
# e.draw_robot((0, 8), 0)
# e.show()
sys.exit(app.exec_())



