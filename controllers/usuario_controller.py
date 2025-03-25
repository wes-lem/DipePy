from fastapi import APIRouter, Depends, Form, Request, Response, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from dao.usuario_dao import UsuarioDAO
from dao.database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login_page(request: Request):
    erro = request.query_params.get("erro", None)
    return templates.TemplateResponse("login.html", {"request": request, "erro": erro})

@router.get("/index")
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    usuario = UsuarioDAO.get_by_email(db, email)
    if usuario and bcrypt.verify(senha, usuario.senha_hash):
        response = RedirectResponse(
            url="/dashboard" if usuario.tipo == "gestor" else "/perfil", status_code=303
        )
        print(
            f"✅ Login bem-sucedido! Usuário ID: {usuario.id} - Cookie de sessão criado."
        )
        response.set_cookie(
            key="session_user", value=str(usuario.id), httponly=True
        )  # Defina o cookie com o ID correto
        return response

    # Se o login falhar, redireciona para a página de login com um erro
    return RedirectResponse(url="/login?erro=Credenciais inválidas", status_code=303)


@router.post("/sair")
def logout(request: Request, response: Response):
    # Verifica se o cookie está presente antes de remover
    session_user = request.cookies.get("session_user")

    if session_user:
        print(f"🔍 Cookie encontrado antes do logout: {session_user}")
    else:
        print("❌ Nenhum cookie encontrado antes do logout.")
        return RedirectResponse(url="/login", status_code=303)

    # Remove o cookie definindo a expiração para o passado
    response.delete_cookie("session_user", path="/")

    ## Verifica se o cookie foi removido imediatamente
    # session_user_after = request.cookies.get("session_user")

    # if session_user_after:
    #     print("❌ O cookie ainda está presente após a tentativa de remoção.")
    #     return {"status": "erro", "message": "Falha ao remover o cookie."}

    # print("✅ Cookie 'session_user' removido com sucesso.")

    # Redireciona para a página de login após a remoção do cookie
    return RedirectResponse(url="/login", status_code=303)


#  Solução correta para verificar a sessão
def verificar_sessao(request: Request):
    session_user = request.cookies.get("session_user")
    if not session_user:
        print("❌ Tentativa de acesso sem sessão ativa!")
        # Redireciona para o login com o erro de "Usuário não autenticado"
        raise HTTPException(
            status_code=303,
            detail="Usuário não autenticado",
            headers={"Location": "/login?erro=Usuario nao autenticado"},
        )
    return session_user  # Retorna o ID do usuário para uso na rota


@router.get("/perfil")
def perfil(request: Request, user_id: str = Depends(verificar_sessao)):
    # Se não for verificado o id do usuário, desfaz o login
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse(
        "perfil.html", {"request": request, "user_id": user_id}
    )

@router.get("/cadastro")
def cadastro_page(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})


# Rota para processar o cadastro do usuário
@router.post("/cadastro")
def cadastro(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    # Criação do usuário com a senha criptografada
    senha_hash = bcrypt.hash(senha)
    usuario_criado = UsuarioDAO.create(db, email, senha_hash)

    # Redireciona para a página de cadastro do aluno com o id do usuário
    return RedirectResponse(url=f"/cadastro/aluno/{usuario_criado.id}", status_code=303)


@router.get("/dashboard")
def dashboard(request: Request, user_id: str = Depends(verificar_sessao)):
    # Se não for verificado o id do usuário, desfaz o login
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user_id": user_id}
    )
