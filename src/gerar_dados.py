import os
import random
from datetime import date, timedelta

import psycopg
from dotenv import load_dotenv


# =========================================================
# 1. CONFIGURAÇÃO
# =========================================================

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

if not all(config.values()):
    raise ValueError(
        "Verifique as variáveis DB_* no arquivo .env."
    )

config["port"] = int(config["port"])

# Permite reproduzir os mesmos dados aleatórios.
random.seed(42)


# =========================================================
# 2. VOLUME DE DADOS
# =========================================================

TOTAL_CLIENTES = 1200
TOTAL_VENDEDORES = 20
TOTAL_PEDIDOS = 15000

# Os últimos 50 clientes (1151 a 1200) NÃO terão pedidos.
CLIENTES_COM_PEDIDOS = 1150

# Os dois últimos vendedores não terão vendas.
VENDEDORES_COM_VENDAS = 18


# =========================================================
# 3. DADOS DE APOIO
# =========================================================

nomes = [
    "Ana", "Bruno", "Carla", "Diego", "Elena",
    "Fabio", "Gabriela", "Helena", "Igor", "Julia",
    "Lucas", "Mariana", "Pedro", "Rafaela", "Thiago",
    "Beatriz", "Caio", "Fernanda", "Gabriel", "Laura",
]

sobrenomes = [
    "Silva", "Santos", "Oliveira", "Souza", "Lima",
    "Costa", "Pereira", "Almeida", "Ferreira", "Rocha",
]

localidades = [
    ("São Paulo", "SP"),
    ("Recife", "PE"),
    ("Rio de Janeiro", "RJ"),
    ("Fortaleza", "CE"),
    ("Salvador", "BA"),
    ("Curitiba", "PR"),
    ("Brasília", "DF"),
    ("Goiânia", "GO"),
    ("Manaus", "AM"),
    ("Belo Horizonte", "MG"),
]

regioes = [
    "Norte",
    "Nordeste",
    "Centro-Oeste",
    "Sudeste",
    "Sul",
]

produtos = [
    ("Notebook", "Eletrônicos", 3500.00),
    ("Smartphone", "Eletrônicos", 2200.00),
    ("Monitor", "Eletrônicos", 950.00),
    ("Teclado", "Eletrônicos", 180.00),
    ("Mouse", "Eletrônicos", 90.00),
    ("Fone Bluetooth", "Eletrônicos", 250.00),
    ("Tablet", "Eletrônicos", 1400.00),
    ("Webcam", "Eletrônicos", 210.00),
    ("Camiseta", "Roupas", 60.00),
    ("Calça Jeans", "Roupas", 140.00),
    ("Tênis", "Roupas", 280.00),
    ("Jaqueta", "Roupas", 320.00),
    ("Vestido", "Roupas", 190.00),
    ("Mochila", "Acessórios", 160.00),
    ("Relógio", "Acessórios", 350.00),
    ("Óculos de Sol", "Acessórios", 120.00),
    ("Livro de SQL", "Livros", 85.00),
    ("Livro de Python", "Livros", 95.00),
    ("Livro de Dados", "Livros", 110.00),
    ("Cadeira", "Casa", 650.00),
    ("Luminária", "Casa", 130.00),
    ("Garrafa Térmica", "Casa", 75.00),
    ("Cafeteira", "Casa", 240.00),
    ("Fone com Fio", "Eletrônicos", 55.00),
    ("Carregador", "Eletrônicos", 80.00),
]


# =========================================================
# 4. GERAÇÃO DOS CLIENTES
# =========================================================

clientes = []

for i in range(1, TOTAL_CLIENTES + 1):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    cidade, estado = random.choice(localidades)

    data_cadastro = date(2022, 1, 1) + timedelta(
        days=random.randint(0, 1460)
    )

    clientes.append((
        nome,
        f"cliente{i}@exemplo.com",
        cidade,
        estado,
        data_cadastro,
    ))


# =========================================================
# 5. GERAÇÃO DOS VENDEDORES
# =========================================================

vendedores = []

for i in range(1, TOTAL_VENDEDORES + 1):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"

    vendedores.append((
        nome,
        f"vendedor{i}@exemplo.com",
        random.choice(regioes),
        i <= VENDEDORES_COM_VENDAS,
    ))


# =========================================================
# 6. GERAÇÃO DOS PEDIDOS E ITENS (GARANTINDO EXATAMENTE 50 INATIVOS)
# =========================================================

pedidos_brutos = []

inicio = date(2024, 1, 1)
fim = date(2025, 12, 31)
dias_periodo = (fim - inicio).days

# PASSO A: Garantir que cada um dos primeiros 1150 clientes tenha ao menos 1 pedido
for idx in range(CLIENTES_COM_PEDIDOS):
    cliente = clientes[idx]
    email_cliente = cliente[1]
    data_cadastro = cliente[4]

    # Data do pedido deve ser posterior ou igual à data de cadastro, mas dentro do período
    min_data = max(inicio, data_cadastro)
    if min_data > fim:
        min_data = inicio  # fallback seguro caso o cadastro seja no limite

    dias_validos = (fim - min_data).days
    data_pedido = min_data + timedelta(days=random.randint(0, max(0, dias_validos)))

    numero_vendedor = random.randint(1, VENDEDORES_COM_VENDAS)
    email_vendedor = f"vendedor{numero_vendedor}@exemplo.com"

    status = random.choices(
        ["pago", "enviado", "pendente", "cancelado"],
        weights=[60, 20, 10, 10],
        k=1,
    )[0]

    pedidos_brutos.append((email_cliente, email_vendedor, data_pedido, status))

# PASSO B: Gerar o restante dos pedidos aleatoriamente entre os 1150 clientes elegíveis
pedidos_restantes = TOTAL_PEDIDOS - CLIENTES_COM_PEDIDOS

for _ in range(pedidos_restantes):
    cliente = clientes[random.randint(0, CLIENTES_COM_PEDIDOS - 1)]
    email_cliente = cliente[1]
    data_cadastro = cliente[4]

    min_data = max(inicio, data_cadastro)
    if min_data > fim:
        min_data = inicio

    dias_validos = (fim - min_data).days
    data_pedido = min_data + timedelta(days=random.randint(0, max(0, dias_validos)))

    numero_vendedor = random.randint(1, VENDEDORES_COM_VENDAS)
    email_vendedor = f"vendedor{numero_vendedor}@exemplo.com"

    status = random.choices(
        ["pago", "enviado", "pendente", "cancelado"],
        weights=[60, 20, 10, 10],
        k=1,
    )[0]

    pedidos_brutos.append((email_cliente, email_vendedor, data_pedido, status))

# Embaralha a ordem dos pedidos para que não fiquem cronologicamente ordenados por cliente
random.shuffle(pedidos_brutos)

# PASSO C: Montar os itens para cada pedido gerado
pedidos = []

for email_cliente, email_vendedor, data_pedido, status in pedidos_brutos:
    produtos_escolhidos = random.sample(
        produtos,
        k=random.randint(1, 4),
    )

    itens_do_pedido = []

    for nome_produto, categoria, preco_atual in produtos_escolhidos:
        quantidade = random.randint(1, 4)
        preco_unitario = round(
            preco_atual * random.uniform(0.90, 1.10),
            2,
        )

        itens_do_pedido.append((
            nome_produto,
            quantidade,
            preco_unitario,
        ))

    pedidos.append((
        email_cliente,
        email_vendedor,
        data_pedido,
        status,
        itens_do_pedido,
    ))


# =========================================================
# 7. RESUMO E CONFIRMAÇÃO
# =========================================================

total_itens = sum(
    len(pedido[4])
    for pedido in pedidos
)

print("\nResumo dos dados que serão gerados:")
print(f"Clientes: {len(clientes)} (sendo exatos {TOTAL_CLIENTES - CLIENTES_COM_PEDIDOS} sem pedidos)")
print(f"Vendedores: {len(vendedores)}")
print(f"Produtos: {len(produtos)}")
print(f"Pedidos: {len(pedidos)}")
print(f"Itens dos pedidos: {total_itens}")

print(
    "\nATENÇÃO: os dados atuais das cinco tabelas "
    "serão apagados e substituídos."
)

confirmacao = input(
    'Digite SIM para continuar: '
).upper()

if confirmacao != "SIM":
    print("Operação cancelada. Nenhum dado foi alterado.")
    raise SystemExit


# =========================================================
# 8. INSERÇÃO NO POSTGRESQL
# =========================================================

with psycopg.connect(**config) as conn:
    with conn.cursor() as cursor:

        # Limpa as tabelas e reinicia os IDs.
        cursor.execute("""
            TRUNCATE TABLE
                itens_pedido,
                pedidos,
                produtos,
                vendedores,
                clientes
            RESTART IDENTITY CASCADE;
        """)

        # Insere os clientes.
        cursor.executemany("""
            INSERT INTO clientes
                (nome, email, cidade, estado, data_cadastro)
            VALUES (%s, %s, %s, %s, %s)
        """, clientes)

        # Recupera os IDs reais dos clientes.
        cursor.execute("""
            SELECT id_cliente, email
            FROM clientes
        """)

        ids_clientes = {
            email: id_cliente
            for id_cliente, email in cursor.fetchall()
        }

        # Insere os vendedores.
        cursor.executemany("""
            INSERT INTO vendedores
                (nome, email, regiao, ativo)
            VALUES (%s, %s, %s, %s)
        """, vendedores)

        # Recupera os IDs reais dos vendedores.
        cursor.execute("""
            SELECT id_vendedor, email
            FROM vendedores
        """)

        ids_vendedores = {
            email: id_vendedor
            for id_vendedor, email in cursor.fetchall()
        }

        # Insere os produtos e guarda seus IDs reais.
        ids_produtos = {}

        for nome, categoria, preco in produtos:
            cursor.execute("""
                INSERT INTO produtos
                    (nome, categoria, preco_atual)
                VALUES (%s, %s, %s)
                RETURNING id_produto
            """, (nome, categoria, preco))

            ids_produtos[nome] = cursor.fetchone()[0]

        # Insere cada pedido e recupera seu ID real.
        for pedido in pedidos:
            (
                email_cliente,
                email_vendedor,
                data_pedido,
                status,
                itens_do_pedido,
            ) = pedido

            cursor.execute("""
                INSERT INTO pedidos
                    (id_cliente, id_vendedor, data_pedido, status)
                VALUES (%s, %s, %s, %s)
                RETURNING id_pedido
            """, (
                ids_clientes[email_email := email_cliente],
                ids_vendedores[email_vendedor],
                data_pedido,
                status,
            ))

            id_pedido = cursor.fetchone()[0]

            # Insere os itens relacionados ao pedido.
            for nome_produto, quantidade, preco_unitario in itens_do_pedido:
                cursor.execute("""
                    INSERT INTO itens_pedido
                        (id_pedido, id_produto, quantidade, preco_unitario)
                    VALUES (%s, %s, %s, %s)
                """, (
                    id_pedido,
                    ids_produtos[nome_produto],
                    quantidade,
                    preco_unitario,
                ))

print("\nDados gerados e inseridos com sucesso!")
