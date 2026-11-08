# =========================================================
# Projeto: Análise de Vendas de E-commerce
# Arquivo: gerar_dados.py
# Objetivo: Simular dados transacionais de clientes, vendedores, 
#           produtos e pedidos com sazonalidade e regras de negócio.
# =========================================================

import calendar
import os
import random
from collections import Counter
from datetime import date, timedelta
from decimal import Decimal
from dotenv import load_dotenv

# =========================================================
# 1. Parâmetros Globais e Premissas de Simulação
# =========================================================
SEMENTE = 42
TOTAL_CLIENTES = 3200
TOTAL_VENDEDORES = 28
VENDEDORES_INATIVOS = 3
INICIO_VENDAS = date(2024, 1, 1)
FIM_VENDAS = date(2025, 12, 31)
PROB_CLIENTE_SEM_PEDIDOS = 0.12

# Nota: Apenas status 'pago', 'pendente' e 'cancelado' são considerados.
# 'enviado' foi omitido para evitar divergências entre pagamento e entrega.
STATUS_PEDIDO = ["pago", "pendente", "cancelado"]
PESOS_STATUS = [80, 11, 9]

# Distribuição de frequência de compra entre os clientes ativos.
PERFIS = ["compra_unica", "ocasional", "frequente", "fiel"]
PESOS_PERFIS = [48, 32, 17, 3]

# Fatores de ponderação de sazonalidade mensal (picos em novembro/dezembro).
SAZONALIDADE = {
    1: 0.87, 2: 0.82, 3: 0.94, 4: 0.98,
    5: 1.08, 6: 1.10, 7: 1.06, 8: 0.96,
    9: 1.01, 10: 1.13, 11: 1.80, 12: 1.38,
}

PESOS_CATEGORIAS = {
    "Eletrônicos": 19,
    "Roupas": 28,
    "Acessórios": 18,
    "Livros": 17,
    "Casa": 18,
}

NOMES = [
    "Ana", "Bruno", "Carla", "Diego", "Elena", "Fabio", "Gabriela",
    "Helena", "Igor", "Julia", "Lucas", "Mariana", "Pedro", "Rafaela",
    "Thiago", "Beatriz", "Caio", "Fernanda", "Gabriel", "Laura",
]
SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Lima", "Costa",
    "Pereira", "Almeida", "Ferreira", "Rocha",
]
LOCALIDADES = [
    ("São Paulo", "SP"), ("Recife", "PE"), ("Rio de Janeiro", "RJ"),
    ("Fortaleza", "CE"), ("Salvador", "BA"), ("Curitiba", "PR"),
    ("Brasília", "DF"), ("Goiânia", "GO"), ("Manaus", "AM"),
    ("Belo Horizonte", "MG"),
]
REGIOES = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

# Catálogo base: (Nome do Produto, Categoria, Preço de Referência em R$)
PRODUTOS = [
    ("Notebook", "Eletrônicos", 3500),
    ("Smartphone", "Eletrônicos", 2200),
    ("Monitor", "Eletrônicos", 950),
    ("Teclado", "Eletrônicos", 180),
    ("Mouse", "Eletrônicos", 90),
    ("Fone Bluetooth", "Eletrônicos", 250),
    ("Tablet", "Eletrônicos", 1400),
    ("Webcam", "Eletrônicos", 210),
    ("Fone com Fio", "Eletrônicos", 55),
    ("Carregador", "Eletrônicos", 80),
    ("SSD Externo", "Eletrônicos", 420),
    ("Camiseta", "Roupas", 60),
    ("Calça Jeans", "Roupas", 140),
    ("Tênis", "Roupas", 280),
    ("Jaqueta", "Roupas", 320),
    ("Vestido", "Roupas", 190),
    ("Bermuda", "Roupas", 85),
    ("Moletom", "Roupas", 180),
    ("Camisa Social", "Roupas", 155),
    ("Mochila", "Acessórios", 160),
    ("Relógio", "Acessórios", 350),
    ("Óculos de Sol", "Acessórios", 120),
    ("Carteira", "Acessórios", 75),
    ("Bolsa", "Acessórios", 230),
    ("Cinto", "Acessórios", 65),
    ("Boné", "Acessórios", 55),
    ("Livro de SQL", "Livros", 85),
    ("Livro de Python", "Livros", 95),
    ("Livro de Dados", "Livros", 110),
    ("Livro de Excel", "Livros", 75),
    ("Livro de Estatística", "Livros", 115),
    ("Livro de Finanças", "Livros", 90),
    ("Cadeira", "Casa", 650),
    ("Luminária", "Casa", 130),
    ("Garrafa Térmica", "Casa", 75),
    ("Cafeteira", "Casa", 240),
    ("Organizador", "Casa", 50),
    ("Jogo de Toalhas", "Casa", 115),
    ("Travesseiro", "Casa", 100),
    ("Panela", "Casa", 180),
]


# =========================================================
# 2. Funções Auxiliares de Data e Temporalidade
# =========================================================

def mes_seguinte(dia):
    return date(dia.year + (dia.month == 12), dia.month % 12 + 1, 1)


def meses_disponiveis(data_cadastro):
    primeiro = max(INICIO_VENDAS, data_cadastro)
    mes = date(primeiro.year, primeiro.month, 1)
    meses = []
    while mes <= FIM_VENDAS:
        meses.append(mes)
        mes = mes_seguinte(mes)
    return meses


def sortear_dia(rng, mes, data_cadastro):
    ultimo_dia = calendar.monthrange(mes.year, mes.month)[1]
    minimo = max(date(mes.year, mes.month, 1), data_cadastro, INICIO_VENDAS)
    maximo = min(date(mes.year, mes.month, ultimo_dia), FIM_VENDAS)
    if minimo > maximo:
        raise ValueError("O intervalo de datas calculado é inválido.")

    # Concentração de transações para o período da Black Friday em novembro.
    if mes.month == 11 and rng.random() < 0.33:
        promocao = max(minimo, date(mes.year, 11, 24))
        if promocao <= maximo:
            minimo = promocao
    dias = (maximo - minimo).days
    return minimo + timedelta(days=rng.randint(0, dias))


def peso_mes(mes):
    fator_crescimento = 1.10 if mes.year == 2025 else 1.0
    return SAZONALIDADE[mes.month] * fator_crescimento


# =========================================================
# 3. Funções de Geração de Entidades e Transações
# =========================================================

def quantidade_pedidos_cliente(rng, perfil, total_meses):
    if perfil == "compra_unica":
        return 1
    faixas_anuais = {
        "ocasional": (1.3, 3.1),
        "frequente": (4.5, 8.5),
        "fiel": (12.0, 20.0),
    }
    minimo, maximo = faixas_anuais[perfil]
    adicionais = round(total_meses / 12 * rng.uniform(minimo, maximo))
    return 1 + max(1, adicionais)


def escolher_produtos(rng, data_pedido):
    quantidade_tipos = rng.choices([1, 2, 3, 4], weights=[58, 27, 11, 4])[0]
    disponiveis = PRODUTOS.copy()
    itens = []
    categoria_anterior = None

    for _ in range(quantidade_tipos):
        categorias = list(PESOS_CATEGORIAS)
        pesos = [PESOS_CATEGORIAS[c] for c in categorias]
        
        # Viés de afinidade para itens da mesma categoria no mesmo carrinho.
        if categoria_anterior and rng.random() < 0.42:
            categoria_escolhida = categoria_anterior
        else:
            categoria_escolhida = rng.choices(categorias, weights=pesos)[0]

        candidatos = [p for p in disponiveis if p[1] == categoria_escolhida]
        if not candidatos:
            candidatos = disponiveis
        producto = rng.choice(candidatos)
        disponiveis.remove(producto)
        nome, categoria_anterior, preco_referencia = producto

        if categoria_anterior == "Eletrônicos":
            quantidade = rng.choices([1, 2, 3], weights=[91, 8, 1])[0]
        else:
            quantidade = rng.choices([1, 2, 3], weights=[78, 18, 4])[0]

        variacao = rng.uniform(0.94, 1.07)
        if data_pedido.month == 11 and rng.random() < 0.50:
            variacao *= rng.uniform(0.78, 0.94)
        preco = Decimal(str(round(preco_referencia * variacao, 2)))
        itens.append((nome, quantidade, preco))
    return itens


def gerar_registros():
    rng = random.Random(SEMENTE)
    clientes = []
    perfis_clientes = []

    # Geração de base de clientes com datas de cadastro distribuídas.
    faixas_cadastro = [
        (date(2023, 1, 1), date(2023, 12, 31)),
        (date(2024, 1, 1), date(2024, 12, 31)),
        (date(2025, 1, 1), date(2025, 11, 30)),
    ]
    for i in range(1, TOTAL_CLIENTES + 1):
        inicio, fim = rng.choices(faixas_cadastro, weights=[50, 32, 18])[0]
        cadastro = inicio + timedelta(days=rng.randint(0, (fim - inicio).days))
        cidade, estado = rng.choice(LOCALIDADES)
        clientes.append((
            f"{rng.choice(NOMES)} {rng.choice(SOBRENOMES)}",
            f"cliente{i}@exemplo.com", cidade, estado, cadastro,
        ))
        if rng.random() < PROB_CLIENTE_SEM_PEDIDOS:
            perfis_clientes.append("sem_pedidos")
        else:
            perfis_clientes.append(rng.choices(PERFIS, weights=PESOS_PERFIS)[0])

    # Geração da equipe de vendas, configurando agentes inativos.
    vendedores = []
    for i in range(1, TOTAL_VENDEDORES + 1):
        vendedores.append((
            f"{rng.choice(NOMES)} {rng.choice(SOBRENOMES)}",
            f"vendedor{i}@exemplo.com",
            rng.choice(REGIOES),
            i <= TOTAL_VENDEDORES - VENDEDORES_INATIVOS,
        ))
    ativos = vendedores[:TOTAL_VENDEDORES - VENDEDORES_INATIVOS]
    pesos_vendedores = [rng.uniform(0.7, 1.4) for _ in ativos]

    # Simulação de pedidos associados aos clientes e vendedores ativos.
    pedidos = []
    for cliente, perfil in zip(clientes, perfis_clientes):
        if perfil == "sem_pedidos":
            continue
        meses = meses_disponiveis(cliente[4])
        if not meses:
            continue
        total = quantidade_pedidos_cliente(rng, perfil, len(meses))
        pesos_meses = [peso_mes(mes) for mes in meses]
        meses_pedidos = rng.choices(meses, weights=pesos_meses, k=total)

        for mes in meses_pedidos:
            data_pedido = sortear_dia(rng, mes, cliente[4])
            vendedor = rng.choices(ativos, weights=pesos_vendedores)[0]
            status = rng.choices(STATUS_PEDIDO, weights=PESOS_STATUS)[0]
            itens = escolher_produtos(rng, data_pedido)
            pedidos.append((cliente[1], vendedor[1], data_pedido, status, itens))

    # Randomização da ordem dos registros para evitar viés sequencial de IDs.
    rng.shuffle(pedidos)

    # Validação de integridade em memória pré-persistência.
    assert len(clientes) == TOTAL_CLIENTES
    assert len(vendedores) == TOTAL_VENDEDORES
    assert len({p[0] for p in PRODUTOS}) == len(PRODUTOS)
    cadastro_por_email = {c[1]: c[4] for c in clientes}
    for email, _, data_pedido, status, itens in pedidos:
        assert INICIO_VENDAS <= data_pedido <= FIM_VENDAS
        assert data_pedido >= cadastro_por_email[email]
        assert status in STATUS_PEDIDO
        assert itens and len({item[0] for item in itens}) == len(itens)
        assert all(qtd > 0 and preco > 0 for _, qtd, preco in itens)

    return clientes, vendedores, pedidos, perfis_clientes


def mostrar_resumo(clientes, vendedores, pedidos, perfis):
    quantidade_itens = sum(len(p[4]) for p in pedidos)
    print("\nRESUMO DA BASE SINTÉTICA GERADA")
    print(f"Clientes: {len(clientes):,}")
    print(f"Vendedores: {len(vendedores):,}")
    print(f"Produtos: {len(PRODUTOS):,}")
    print(f"Pedidos: {len(pedidos):,}")
    print(f"Itens de pedidos: {quantidade_itens:,}")
    print("Perfis de clientes:", dict(Counter(perfis)))
    print("Status dos pedidos:", dict(Counter(p[3] for p in pedidos)))
    meses = Counter(p[2].strftime("%Y-%m") for p in pedidos)
    print("Pedidos por mês:")
    print("-" * 30)
    for mes, quantidade in sorted(meses.items()):
        print(f"  {mes}: {quantidade}")


# =========================================================
# 4. Camada de Persistência (PostgreSQL)
# =========================================================

def gravar_no_postgresql(clientes, vendedores, pedidos):
    import psycopg

    load_dotenv()
    config = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
    if not all(config.values()):
        raise ValueError("Variáveis de ambiente do banco de dados incompletas no arquivo .env.")
    config["port"] = int(config["port"])

    # Execução em bloco transacional único (ACID). Rollback automático em caso de exceção.
    with psycopg.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                TRUNCATE TABLE itens_pedido, pedidos, produtos, vendedores, clientes
                RESTART IDENTITY CASCADE;
            """)
            
            cursor.executemany("""
                INSERT INTO clientes (nome, email, cidade, estado, data_cadastro)
                VALUES (%s, %s, %s, %s, %s)
            """, clientes)
            cursor.execute("SELECT id_cliente, email FROM clientes")
            ids_clientes = {email: ident for ident, email in cursor.fetchall()}

            cursor.executemany("""
                INSERT INTO vendedores (nome, email, regiao, ativo)
                VALUES (%s, %s, %s, %s)
            """, vendedores)
            cursor.execute("SELECT id_vendedor, email FROM vendedores")
            ids_vendedores = {email: ident for ident, email in cursor.fetchall()}

            ids_produtos = {}
            for nome, categoria, preco in PRODUTOS:
                cursor.execute("""
                    INSERT INTO produtos (nome, categoria, preco_atual)
                    VALUES (%s, %s, %s)
                    RETURNING id_produto
                """, (nome, categoria, preco))
                ids_produtos[nome] = cursor.fetchone()[0]

            todos_itens = []
            for email_cliente, email_vendedor, data_pedido, status, itens in pedidos:
                cursor.execute("""
                    INSERT INTO pedidos (id_cliente, id_vendedor, data_pedido, status)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_pedido
                """, (
                    ids_clientes[email_cliente], ids_vendedores[email_vendedor],
                    data_pedido, status,
                ))
                id_pedido = cursor.fetchone()[0]
                todos_itens.extend(
                    (id_pedido, ids_produtos[nome], quantidade, preco)
                    for nome, quantidade, preco in itens
                )

            cursor.executemany("""
                INSERT INTO itens_pedido
                    (id_pedido, id_produto, quantidade, preco_unitario)
                VALUES (%s, %s, %s, %s)
            """, todos_itens)

            # Validações de integridade referencial pós-carga
            cursor.execute("""
                SELECT COUNT(*) FROM pedidos ped
                INNER JOIN clientes c ON ped.id_cliente = c.id_cliente
                WHERE ped.data_pedido < c.data_cadastro
            """)
            if cursor.fetchone()[0]:
                raise ValueError("Violação de integridade: Pedido anterior à data de cadastro do cliente.")

            cursor.execute("""
                SELECT COUNT(*) FROM pedidos ped
                WHERE NOT EXISTS (
                    SELECT 1 FROM itens_pedido ip WHERE ip.id_pedido = ped.id_pedido
                )
            """)
            if cursor.fetchone()[0]:
                raise ValueError("Violação de integridade: Pedido registrado sem itens associados.")

            cursor.execute("SELECT COUNT(*) FROM pedidos")
            if cursor.fetchone()[0] != len(pedidos):
                raise ValueError("Divergência detectada na contagem total de pedidos persistidos.")

    print("\nCarga e validação de dados concluídas com sucesso no banco de dados.")


def main():
    clientes, vendedores, pedidos, perfis = gerar_registros()
    mostrar_resumo(clientes, vendedores, pedidos, perfis)
    print("\nAVISO: A execução deste script sobrescreverá os dados existentes nas tabelas.")
    confirmacao = input("Digite SIM para confirmar a carga (ou pressione Enter para abortar): ")
    if confirmacao.strip().upper() != "SIM":
        print("Operação cancelada pelo usuário. Nenhuma alteração foi realizada.")
        return
    gravar_no_postgresql(clientes, vendedores, pedidos)


if __name__ == "__main__":
    main()