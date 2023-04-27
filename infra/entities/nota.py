from DateTime import DateTime

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer


class Notas(Base):
    # nome da tabela
    __tablename__ = 'nota'
    # Colunas da tabela que serao criadas
    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String, nullable=False)
    data_criacao = Column(DateTime)
    texto = Column(String, nullable=False)
    prioridade = Column(String, nullable=False)

    # Função que sobrescreve a maneiro de "printar" o obj
    def __repr__(self):
        return f'Título da nota = {self.titulo}, id = {self.id}'
