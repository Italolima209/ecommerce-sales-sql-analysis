import os
from dotenv import load_dotenv
import psycopg

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Lê as credenciais de forma segura
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

try:
    # Tenta estabelecer a conexão com o PostgreSQL
    conexao = psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    
    print("Sucesso! Conexão estabelecida com o banco de dados PostgreSQL.")
    
    # Valida a conexão consultando a quantidade de clientes
    with conexao.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM clientes;")
        total_clientes = cursor.fetchone()[0]
        print(f"Total de clientes cadastrados na base: {total_clientes}")
        
    # Fecha a conexão corretamente
    conexao.close()
    
except Exception as e:
    print("Erro ao conectar ao banco de dados:")
    print(e)