# import emulator.interface as UI
from emulator import Emulator
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
e = Emulator("smth.txt")
# e.show()
# e.update()
sys.exit(app.exec_())



