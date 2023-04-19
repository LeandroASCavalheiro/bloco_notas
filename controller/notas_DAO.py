import sqlite3

from model.notas import Notas


class DataBase:
    def __init__(self, nome='system.db'):
        self.connetion = None
        self.name = nome

    def connect(self):
        self.connetion = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connetion.close()
        except sqlite3.Error as e:
            print(e)

    def create_table_notas(self):
        self.connect()
        cursor = self.connetion.cursor()
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS NOTA(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TITULO TEXT,
                    NOTA TEXT,
                    DATA DATE	
                );
                """)
        self.close_connection()

    def registrar_nota(self, nota=Notas):
        self.connect()
        cursor = self.connetion.cursor()
        campos_nota = ('TITULO', 'NOTA', 'DATA')

        valores = f"'{str(nota.titulo)}'," \
                  f"'{str(nota.nota)}'," \
                  f"'{str(nota.data)}'"
        try:
            cursor.execute(f""" INSERT INTO NOTA {campos_nota} VALUES ({valores})""")
            self.connetion.commit()
            return 'OK'
        except sqlite3.Error as e:
            return str(e)
        finally:
            self.close_connection()

    def consultar_nota(self, id_nota):
        self.connect()

        try:
            cursor = self.connetion.cursor()
            cursor.execute(f""" SELECT * FROM NOTA WHERE ID_NOTA ={id_nota}""")
            return cursor.fetchone()
        except sqlite3.Error as e:
          print(e)
          return None
        finally:
         self.close_connection()

    def consultar_todas_notas(self):
        self.connect()
        try:
            cursor = self.connetion.cursor()
            cursor.execute('SELECT * FROM NOTA')
            notas = cursor.fetchall()
            return notas
        except sqlite3.Error as e:
            print(f'Erro {e}')
            return None
        finally:
            self.close_connection()

    def deletar_nota(self, id_nota):
        self.connect()
        try:
            cursor = self.connetion.cursor()
            cursor.execute(f"""DELETE FROM NOTA WHERE ID ={id_nota}""")
            self.connetion.commit()
            return 'OK'
        except sqlite3.Error as e:
            return str(e)
        finally:
            self.close_connection()

    def atualizar_nota(self, nota):
        self.connect()
        try:
            cursor = self.connetion.cursor()
            cursor.execute(f" UPDATE NOTA SET \n"
                           f" NOTA = '{nota.nota}', \n"
                           f" TITULO ='{nota.titulo}', \n"
                           f" DATA = '{nota.data}'"
                           f" WHERE ID = '{nota.id_nota}';")
            self.connetion.commit()
            return 'OK'
        except sqlite3.Error as e:
            return str(e)
        finally:
            self.close_connection()

    def selecionar_notas(self):
        self.connect()

        script = """  SELECT * FROM NOTA; """
        try:
            cursor = self.connetion.cursor()
            cursor.execute(script)
            return cursor.fetchone()
        except sqlite3.Error as e:
            return str(e)
        finally:
            self.close_connection()
