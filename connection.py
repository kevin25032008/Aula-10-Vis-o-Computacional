import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from conexão import engine, Base, SessionLocal
# Tenta carregar o arquivo .env
load_dotenv()

# Pega a URL do banco. Se não existir, usa um banco SQLite local para testes da aula
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Plano B: Cria um arquivo chamado 'banco_local.db' na sua pasta para a aula funcionar
    DATABASE_URL = "sqlite:///banco_local.db"

# Ajuste automático se for o link do Neon/Postgres antigo
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Se for SQLite, precisa de uma configuração extra de segurança
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
