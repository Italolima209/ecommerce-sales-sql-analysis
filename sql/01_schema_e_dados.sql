DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS clientes;

-- 1. Tabela Clientes (Chave Primária)
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cidade VARCHAR(50),
    estado VARCHAR(2)
);

-- 2. Tabela Pedidos (Chave Estrangeira apontando para clientes)
CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY,
    id_cliente INT,
    categoria VARCHAR(50),
    valor DECIMAL(10, 2),
    status VARCHAR(20),
    data_pedido DATE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- 3. Inserção de Clientes (Incluindo clientes 9 e 10 sem pedidos para testes de integridade/auditoria)
INSERT INTO clientes (id_cliente, nome, cidade, estado) VALUES
(1, 'Ana Silva', 'São Paulo', 'SP'),
(2, 'Bruno Costa', 'Rio de Janeiro', 'RJ'),
(3, 'Carla Dias', 'Belo Horizonte', 'MG'),
(4, 'Diego Rocha', 'Curitiba', 'PR'),
(5, 'Elena Souza', 'Recife', 'PE'),
(6, 'Fabio Lima', 'Fortaleza', 'CE'),
(7, 'Gabi Martins', 'Salvador', 'BA'),
(8, 'Helena Ramos', 'Porto Alegre', 'RS'),
(9, 'Igor Mendes', 'Manaus', 'AM'),
(10, 'Julia Freitas', 'Goiânia', 'GO');

-- 4. Inserção de Pedidos
INSERT INTO pedidos (id_pedido, id_cliente, categoria, valor, status, data_pedido) VALUES
(1, 1, 'Eletrônicos', 1200.00, 'pago', '2024-01-10'),
(2, 2, 'Roupas', 150.00, 'cancelado', '2024-01-12'),
(3, 3, 'Eletrônicos', 800.00, 'pago', '2024-01-15'),
(4, 4, 'Livros', 50.00, 'pago', '2024-01-18'),
(5, 5, 'Roupas', 250.00, 'pago', '2024-01-20'),
(6, 6, 'Eletrônicos', 300.00, 'cancelado', '2024-01-22'),
(7, 7, 'Livros', 120.00, 'pago', '2024-01-25'),
(8, 1, 'Eletrônicos', 950.00, 'pago', '2024-02-02'),
(9, 2, 'Roupas', 320.00, 'pago', '2024-02-05'),
(10, 8, 'Livros', 85.00, 'pago', '2024-02-08'),
(11, 3, 'Roupas', 190.00, 'pago', '2024-02-10'),
(12, 4, 'Eletrônicos', 1500.00, 'pago', '2024-02-14'),
(13, 5, 'Eletrônicos', 600.00, 'pago', '2024-02-16'),
(14, 1, 'Livros', 90.00, 'pago', '2024-02-18'),
(15, 7, 'Roupas', 210.00, 'pago', '2024-02-20'),
(16, 2, 'Livros', 45.00, 'pago', '2024-02-22'),
(17, 3, 'Eletrônicos', 1100.00, 'pago', '2024-02-24'),
(18, 6, 'Roupas', 180.00, 'pago', '2024-02-25'),
(19, 8, 'Eletrônicos', 400.00, 'cancelado', '2024-02-26'),
(20, 4, 'Livros', 75.00, 'pago', '2024-02-28');