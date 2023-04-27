from PySide6.QtWidgets import QMainWindow, QLabel, QTextEdit, QVBoxLayout, QWidget, QSizePolicy, QMessageBox, QLineEdit, \
    QPushButton, QTableWidget, QComboBox, QAbstractItemView, QTableWidgetItem
from datetime import date

from controller.notas_DAO import DataBase
from model.notas import Notas

from infra.configs.connection import DBConnectionHandler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        conn = DBConnectionHandler
        conn.create_database()
        self.setMinimumSize(520, 500)

        self.setWindowTitle('BLOCO DE NOTAS ')

        self.lbl_id = QLabel('Id')
        self.txt_id = QLineEdit()
        self.lbl_id.setVisible(False)
        self.txt_id.setReadOnly(True)
        self.txt_id.setVisible(False)
        self.lbl_titulo = QLabel('Titulo')
        self.txt_titulo = QLineEdit()
        self.lbl_nota = QLabel('Nota')
        self.txt_nota = QTextEdit()
        self.lbl_data = QLabel('Data')
        self.txt_data = QTextEdit()
        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('limpar')
        self.btn_remover = QPushButton('remover')
        self.tabela_notas = QTableWidget()

        self.tabela_notas.setColumnCount(4)
        self.tabela_notas.setHorizontalHeaderLabels(['Id', 'Titulo', 'Nota', 'Data'])
        self.tabela_notas.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_notas.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.txt_titulo)
        layout.addWidget(self.lbl_nota)
        layout.addWidget(self.txt_nota)
        layout.addWidget(self.tabela_notas)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        self.btn_salvar.clicked.connect(self.registrar_nota)
        self.btn_remover.clicked.connect(self.deletar_nota)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.tabela_notas.cellDoubleClicked.connect(self.carregar_notas)
        self.popula_tabela_notas()

    def registrar_nota(self):
        db = DataBase()

        nota = Notas(self.txt_titulo.text(), self.txt_nota.toPlainText(), date.today())
        nota.id_nota = self.txt_id.text()

        if self.btn_salvar.text() == 'Salvar':
            retorno = db.registrar_nota(nota)
            if retorno == 'OK':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Cadastro Realizado')
                msg.setText('Cadastro realizado com sucesso')
                msg.exec()
                self.limpar_campos()

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao Cadastrar NOTA')
                msg.setText(f'erro ao cadastrar NOTA, verificar dados')
                msg.exec()
        if self.btn_salvar.text() == 'Atualizar':
            retorno = db.atualizar_nota(nota)
            print(retorno)
            if retorno == 'OK':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('cadastro atualizado')
                msg.setText('cadastro atualizado com sucesso')
                msg.exec()
                self.limpar_campos()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao atualizar')
                msg.setText(f'erro ao atualizar nota, verifique os dados inseridos')
                msg.exec()
        self.popula_tabela_notas()
        self.txt_nota.setReadOnly(False)

    def consultar_nota(self):
        if self.txt_nota != '':
            db = DataBase()
            returno = db.consultar_nota(str(self.txt_nota.text()))

            if returno is not None:
                self.btn_salvar.setText('Atualizar')
                msg = QMessageBox()
                msg.setWindowTitle('nota já cadastrada')
                msg.setText(f'A NOTA {self.txt_nota.text()} já está cadastrada')
                msg.exec()
                #   self.txt_id_nota.setText(returno[0])
                self.txt_titulo.setText(returno[1])
                self.txt_nota.setText(returno[2])
                self.txt_data.setText(returno[3])
                self.btn_remover.setVisible(True)

    def deletar_nota(self):
        msg = QMessageBox()
        msg.setWindowTitle('Remover nota')
        msg.setText('Esta nota será removida')
        msg.setInformativeText(f"Voçê deseja remover o Titulo, NOTA {self.txt_nota.toPlainText()} ?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        resposta = msg.exec()

        if resposta == QMessageBox.Yes:
            db = DataBase()
            retorno = db.deletar_nota(self.txt_id.text())

            if retorno == 'OK':
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover nota')
                nv_msg.setText('nota excluida.')
                nv_msg.exec()
                self.limpar_campos()
            else:
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover nota')
                nv_msg.setText('Erro ao remover nota')
                nv_msg.exec()
        self.txt_nota.setReadOnly(False)
        self.popula_tabela_notas()

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)

        self.btn_remover.setVisible(False)
        self.btn_salvar.setText('Salvar')
        self.lbl_id.setVisible(False)
        self.txt_id.setVisible(False)

    def popula_tabela_notas(self):
        self.tabela_notas.setRowCount(0)
        db = DataBase()
        lista_notas = db.consultar_todas_notas()
        self.tabela_notas.setRowCount(len(lista_notas))

        for linha, nota in enumerate(lista_notas):
            for coluna, valor in enumerate(nota):
                self.tabela_notas.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carregar_notas(self, row):
        self.txt_id.setText(self.tabela_notas.item(row, 0).text())
        self.txt_titulo.setText(self.tabela_notas.item(row, 1).text())
        self.txt_nota.setText(self.tabela_notas.item(row, 2).text())
        self.txt_data.setText(self.tabela_notas.item(row, 3).text())
        self.btn_salvar.setText('Atualizar')
        self.btn_remover.setVisible(True)
        self.lbl_id.setVisible(True)
        self.txt_id.setVisible(True)
