# import emulator.interface as UI
import interface as UI
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
print(UI.get_screen_size())
tmp = UI.roboCanvasWidget("robo.png")
# tmp = UI.controlWidget()
tmp.show()

sys.exit(app.exec_())



