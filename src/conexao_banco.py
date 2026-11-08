# =========================================================
# Projeto: Análise de Vendas de E-commerce
# Arquivo: conexao_banco.py
# Objetivo: Validar a conexão entre Python e PostgreSQL
# =========================================================

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Lê as credenciais de forma segura
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

url = URL.create(
    drivername="postgresql+psycopg",
    username=user,
    password=password,
    host=host,
    port=int(port) if port else 5432,
    database=dbname
)

try:
    # Tenta estabelecer a conexão com o PostgreSQL
    engine = create_engine(url)
    with engine.connect() as conexao:
        print("Sucesso! Conexão estabelecida com o banco de dados PostgreSQL.")

        # Valida a conexão consultando a quantidade de clientes
        total_clientes = conexao.execute(
            text("SELECT COUNT(*) FROM clientes;")
        ).scalar_one()
        print(f"Total de clientes cadastrados na base: {total_clientes}")

except Exception as e:
    print("Erro ao conectar ao banco de dados:")
    print(e)
    raise
finally:
    if "engine" in locals():
        engine.dispose()
