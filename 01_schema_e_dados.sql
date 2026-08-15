DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY,
    cliente VARCHAR(50),
    categoria VARCHAR(50),
    valor DECIMAL(10, 2),
    status VARCHAR(20),
    data_pedido DATE
);

INSERT INTO pedidos (id_pedido, cliente, categoria, valor, status, data_pedido) VALUES
(1, 'Ana Silva', 'Eletrônicos', 1200.00, 'pago', '2024-01-10'),
(2, 'Bruno Costa', 'Roupas', 150.00, 'cancelado', '2024-01-12'),
(3, 'Carla Dias', 'Eletrônicos', 800.00, 'pago', '2024-01-15'),
(4, 'Diego Rocha', 'Livros', 50.00, 'pago', '2024-01-18'),
(5, 'Elena Souza', 'Roupas', 250.00, 'pago', '2024-01-20'),
(6, 'Fabio Lima', 'Eletrônicos', 300.00, 'cancelado', '2024-01-22'),
(7, 'Gabi Martins', 'Livros', 120.00, 'pago', '2024-01-25'),
(8, 'Ana Silva', 'Eletrônicos', 950.00, 'pago', '2024-02-02'),
(9, 'Bruno Costa', 'Roupas', 320.00, 'pago', '2024-02-05'),
(10, 'Helena Ramos', 'Livros', 85.00, 'pago', '2024-02-08'),
(11, 'Carla Dias', 'Roupas', 190.00, 'pago', '2024-02-10'),
(12, 'Diego Rocha', 'Eletrônicos', 1500.00, 'pago', '2024-02-14');