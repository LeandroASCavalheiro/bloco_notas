from infra.configs.connection import DBConnectionHandler
from infra.entities.nota import Notas


class NotaRepository:
    # realiza consulta no banco
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Notas).all()
            return data

    def select(self, id):
        with DBConnectionHandler() as db:
            data = db.session.query(Notas).filter(Notas.id == id).first()
            return data

    # insere nota no banco

    def insert(self, nota):
        with DBConnectionHandler() as db:
            try:
                db.session.add(nota)
                db.session.commit()
                return 'OK'
            except Exception as e:
                db.session.rollback()
                return e

        # metodo para deletar do banco

    def delete(self):
        with DBConnectionHandler() as db:
            db.session.query(Notas).filter(Notas.id == id).delete()
            db.session.commit()

        # metodo para atualizar o banco

    def update(self, id, titulo, texto, prioridade):
        with DBConnectionHandler() as db:
            db.session.query(Notas).filter(Notas.id == id).update(
                {'titulo': titulo, 'texto': texto, 'prioridade': prioridade})
            db.session.commit()
