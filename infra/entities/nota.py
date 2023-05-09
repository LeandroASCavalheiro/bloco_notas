from DateTime import DateTime

from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, Date


class Notas(Base):
    # nome da tabela
    __tablename__ = 'nota'
    # Colunas da tabela que serao criadas
    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String(length=100), nullable=False)
    data_criacao = Column(Date)
    texto = Column(String(length=100), nullable=False)
    prioridade = Column(String(length=100), nullable=False)

    # Função que sobrescreve a maneiro de "printar" o obj
    def __repr__(self):
        return f'Título da nota = {self.titulo}, id = {self.id}'
