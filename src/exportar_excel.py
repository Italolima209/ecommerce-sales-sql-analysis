# =========================================================
# Projeto: Análise de Vendas de E-commerce
# Arquivo: exportar_excel.py
# Objetivo: Exportar os indicadores de vendas por categoria para um relatório Excel
# =========================================================

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# 1. Carregar as credenciais de conexão com o PostgreSQL
load_dotenv()

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
    # 2. Conectar ao banco de dados
    engine = create_engine(url)
    with engine.connect() as conectar:
        print("Conexão com PostgreSQL estabelecida!")

        # 3. Consultar os itens dos pedidos pagos
        query = """
            SELECT
            ped.id_pedido,
            prod.categoria,
            ip.quantidade,
            ip.preco_unitario
            FROM pedidos ped
            INNER JOIN itens_pedido ip
                ON ped.id_pedido = ip.id_pedido
            INNER JOIN produtos prod
                ON ip.id_produto = prod.id_produto
            WHERE ped.status = 'pago'
            """

        df_vendas = pd.read_sql(text(query), conectar)
        print("Dados carregados com sucesso!")

    # 4. Calcular o faturamento de cada item vendido
    df_vendas["faturamento"] = (
        df_vendas["quantidade"] * df_vendas["preco_unitario"]
    )

    # 5. Calcular faturamento e pedidos distintos por categoria
    df_categoria = df_vendas.groupby("categoria").agg(
        quantidade_pedidos=("id_pedido", "nunique"),
        faturamento=("faturamento", "sum")
    ).reset_index()

    # 6. Calcular o ticket médio de cada categoria
    df_categoria["ticket_medio"] = (
        df_categoria["faturamento"]
        / df_categoria["quantidade_pedidos"]
    ).round(2)

    # 7. Ordenar as categorias pelo maior faturamento
    df_categoria = df_categoria.sort_values(
        by="faturamento",
        ascending=False
    )

    # 8. Exportar o relatório para Excel
    df_categoria.to_excel(
        "relatorio_vendas.xlsx",
        index=False,
        sheet_name="Vendas por Categoria"
    )

    print("Relatório Excel exportado com sucesso!")

except Exception as e:
    print("Erro ao gerar o relatório Excel:", e)
    raise
finally:
    if "engine" in locals():
        engine.dispose()
