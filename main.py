import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from view.principal import MainWindow
import qdarktheme

app = QApplication(sys.argv)
qdarktheme.setup_theme()
window = MainWindow()
icone = QIcon("images/home.svg")
window.setWindowIcon(icone)
window.show()
app.exec()
