
import sys
from PySide6.QtWidgets import QApplication

from view.principal import MainWindow
from controller.notas_DAO import DataBase

from PySide6.QtGui import QIcon
#import qdarrktheme
db = DataBase()
db.connect()
db.create_table_notas()
db.close_connection()

app = QApplication(sys.argv)
#qdarktheme.setup_theme()
window = MainWindow()
#icone = QIcon("images/home.svg")
#window.setWindowIcon(icone)
window.show()
app.exec()

