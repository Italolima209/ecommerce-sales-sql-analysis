
import os
from dotenv import load_dotenv
import psycopg
import pandas as pd

# Carrega as credenciais do .env
load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

try:
    # Conecta ao PostgreSQL
    with psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    ) as conectar:
        print("Conexão estabelecida para exportação!")

        # Consulta os pedidos
        query = "SELECT * FROM pedidos;"
        df_pedido = pd.read_sql(query, conectar)

        # Agrupa os pedidos por categoria e Ordena pelo maior faturamento
        resumo_categoria = df_pedido.groupby("categoria")["valor"].agg(
            faturamento="sum",
            qtd_pedidos="count",
            ticket_medio="mean"
        ).reset_index().sort_values(by='faturamento', ascending=False)

        # Exporta o resultado para Excel
        nome_ficheiro = "relatorio_vendas.xlsx"
        resumo_categoria.to_excel(
            nome_ficheiro,
            index=False,
            engine="openpyxl"
        )

        print(f"Relatório exportado com sucesso: {nome_ficheiro}")

except Exception as e:
    print("Erro ao gerar relatório:")
    print(e)
