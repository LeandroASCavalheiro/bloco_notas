from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:

    def __init__(self):
        # Dados de endereço do banco
        self.__connection_string = 'mysql+pymysql://root:Senac2021@localhost:3306/notas'
        # instãncia do engine(gerenciador do banco)
        self.__engine = self.__create_data_base_engine()
        # sessão nula para que possa ser alocada uma nova ao ser instanciado um obj
        self.session = None
        # valida o banco
        self.__create_database()

    # valida se o banco existe, caso nao, cria um banco
    def create_database(self):
        engine = create_engine(self.__connection_string, echo=True)

        try:
            engine.connect()
        except Exception as e:
            if '1049' in str(e):
                engine = create_engine(self.__connection_string.rsplit('/', 1)[0], echo=True)
                conn = engine.connect()
                conn.execute(f'CREATE DATABASE IF NOT EXISTS {self.__connection_string.rsplit("/", 1)[1]}')
                conn.close()
                print('Banco criado')
            else:
                raise e

    # funçao para criacao da engine sem necessidade de informar o endereço do banco
    def __create_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    # função magica que definem qualquer comportamento ao serem geradas
    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        print("Gerando conexão")
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Fechando conexão')
        self.session.close(

        )
