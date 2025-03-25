import importlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Aluno = importlib.import_module("models.aluno")
Usuario = importlib.import_module("models.usuario")

# Configuração do banco de dados MySQL
DATABASE_URL = "mysql+pymysql://root:1234@localhost/sistema_login"

# Criação do engine do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})

# Sessão local para o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()


# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
