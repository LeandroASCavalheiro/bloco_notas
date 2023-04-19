import sys
import sys
from PySide6.QtWidgets import QApplication

from view.principal import MainWindow
from controller.notas_DAO import DataBase


db = DataBase()
db.connect()
db.create_table_notas()
db.close_connection()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
