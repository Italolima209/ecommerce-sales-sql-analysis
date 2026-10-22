import os
from dotenv import load_dotenv
import psycopg
import pandas as pd

# Carrega credenciais do .env de forma segura
load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

try:
    # Tenta estabelecer conexão com o PostgreSQL
    conexao = psycopg.connect(
        host=host, port=port, dbname=dbname, user=user, password=password
    )
    print("Conexão estabelecida com sucesso para análise em Pandas!\n")
    
    # 1. Carrega os pedidos do banco de dados para um DataFrame do Pandas
    query_pedidos = "SELECT * FROM pedidos;"
    df_pedidos = pd.read_sql(query_pedidos, conexao)
    
    # 2. Métricas Gerais (KPIs)
    faturamento_total = df_pedidos['valor'].sum()
    total_pedidos = df_pedidos['id_pedido'].count()
    ticket_medio = df_pedidos['valor'].mean()
    
    print("=== RESUMO FINANCEIRO DO E-COMMERCE ===")
    print(f"Faturamento Total : R$ {faturamento_total:,.2f}")
    print(f"Total de Pedidos  : {total_pedidos}")
    print(f"Ticket Médio      : R$ {ticket_medio:,.2f}")
    print("="*39 + "\n")
    
    # 3. Análise por Categoria
    df_categoria = df_pedidos.groupby('categoria')['valor'].agg(
        Qtd_Pedidos='count',
        Faturamento='sum',
        Ticket_Medio='mean'
    ).reset_index()
    
    print("=== DESEMPENHO POR CATEGORIA ===")
    print(df_categoria.to_string(index=False))

    # Fecha a conexão corretamente
    conexao.close()

except Exception as e:
    print("Erro durante a análise de vendas:", e)