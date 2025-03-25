from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from models.usuario import Usuario
from dao.aluno_dao import AlunoDAO
from dao.database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Rota para a página de cadastro de aluno, onde o aluno preenche seus dados
@router.get("/cadastro/aluno/{idUser}")
def cadastro_aluno_page(request: Request, idUser: int):
    return templates.TemplateResponse(
        "cadastro_aluno.html", {"request": request, "idUser": idUser}
    )


# Rota para processar o cadastro de aluno
@router.post("/cadastro/aluno/{idUser}")
def cadastrar_aluno(
    idUser: int,
    nome: str,
    ano: int,
    curso: str,
    db: Session = Depends(get_db),
):
    # Valida se o usuário existe e se é do tipo 'aluno'
    usuario = db.query(Usuario).filter(Usuario.id == idUser).first()

    if not usuario:
        raise HTTPException(
            status_code=404, detail="Usuário não encontrado ou não é do tipo aluno"
        )

    # Verifica se o curso informado é válido
    if curso not in ["Redes de Computadores", "Agropecuária"]:
        raise HTTPException(status_code=400, detail="Curso inválido")

    # Criação do aluno associando ao usuário
    aluno_criado = AlunoDAO.create(db, idUser, nome, ano, curso)
    return aluno_criado