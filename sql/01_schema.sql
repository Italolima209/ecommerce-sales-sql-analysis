
-- =========================================================
-- Projeto: Análise de Vendas de E-commerce
-- Arquivo: 01_schema.sql
-- Banco: PostgreSQL
-- Objetivo: Criar a estrutura relacional do projeto
-- =========================================================

-- ATENÇÃO: recria as tabelas e apaga os dados existentes.

DROP TABLE IF EXISTS itens_pedido, pedidos, produtos, vendedores, clientes CASCADE;

-- 1. CLIENTES
CREATE TABLE clientes (
    id_cliente INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    cidade VARCHAR(100),
    estado CHAR(2),
    data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT chk_clientes_estado
        CHECK (estado IS NULL OR estado ~ '^[A-Z]{2}$')
);


-- 2. VENDEDORES
CREATE TABLE vendedores (
    id_vendedor INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    regiao VARCHAR(50) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);


-- 3. PRODUTOS
CREATE TABLE produtos (
    id_produto INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco_atual NUMERIC(12, 2) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_produtos_preco
        CHECK (preco_atual > 0)
);


-- 4. PEDIDOS
CREATE TABLE pedidos (
    id_pedido INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_vendedor INTEGER NOT NULL,
    data_pedido DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',

    CONSTRAINT fk_pedidos_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    CONSTRAINT fk_pedidos_vendedor
        FOREIGN KEY (id_vendedor)
        REFERENCES vendedores(id_vendedor),

    CONSTRAINT chk_pedidos_status
        CHECK (status IN ('pago', 'pendente', 'cancelado', 'enviado'))
);


-- 5. ITENS DOS PEDIDOS
CREATE TABLE itens_pedido (
    id_item INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pedido INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario NUMERIC(12, 2) NOT NULL,

    CONSTRAINT fk_itens_pedido
        FOREIGN KEY (id_pedido)
        REFERENCES pedidos(id_pedido)
        ON DELETE CASCADE,

    CONSTRAINT fk_itens_produto
        FOREIGN KEY (id_produto)
        REFERENCES produtos(id_produto),

    CONSTRAINT uq_item_pedido_produto
        UNIQUE (id_pedido, id_produto),

    CONSTRAINT chk_itens_quantidade
        CHECK (quantidade > 0),

    CONSTRAINT chk_itens_preco
        CHECK (preco_unitario > 0)
);


-- 6. ÍNDICES
-- Índices adicionais para chaves estrangeiras e filtros frequentes.
-- As chaves primárias e UNIQUE já criam seus próprios índices.

CREATE INDEX idx_pedidos_cliente ON pedidos(id_cliente);
CREATE INDEX idx_pedidos_vendedor ON pedidos(id_vendedor);
CREATE INDEX idx_pedidos_data ON pedidos(data_pedido);
CREATE INDEX idx_pedidos_status ON pedidos(status);
CREATE INDEX idx_itens_produto ON itens_pedido(id_produto);
