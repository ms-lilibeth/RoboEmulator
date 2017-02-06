# import emulator.interface as UI
import interface as UI
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
e = UI.Emulator()
# e.update()
sys.exit(app.exec_())



