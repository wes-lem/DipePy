from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    ano = Column(Integer)
    curso = Column(String)

    idUser = Column(
        Integer, ForeignKey("usuarios.id")
    )  # Relacionamento com a tabela usuarios

    usuario = relationship("Usuario", back_populates="aluno")
