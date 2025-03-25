from sqlalchemy.orm import Session
from models.aluno import Aluno


class AlunoDAO:
    @staticmethod
    def create(
        db: Session, idUser: int, nome: str, ano: int, curso: str
    ):
        novo_aluno = Aluno(
            idUser=idUser, nome=nome, ano=ano, curso=curso
        )
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        return novo_aluno
