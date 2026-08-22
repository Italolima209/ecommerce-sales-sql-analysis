# 📊 Análise de Vendas de E-commerce e Modelagem Relacional (PostgreSQL)

Projeto prático de análise de dados e engenharia de consultas SQL, focado em modelagem relacional, integridade referencial, relatórios gerenciais e auditoria cadastral de ponta a ponta.

---

## 🎯 Objetivo de Negócio
Simular um ambiente real de e-commerce estruturado sob arquitetura relacional para extrair métricas estratégicas de performance comercial e integridade de base:
- Faturamento consolidado, volume transacional e ticket médio por cliente e estado.
- Performance de receita e volume por categoria de produto.
- Monitoramento e impacto financeiro de pedidos cancelados.
- Auditoria de base cadastral: identificação de clientes inativos (anti-join), taxa de ativação regional e tratamento rigoroso de valores nulos.

---

## 🛠️ Tecnologias e Conceitos Aplicados
- **SGBD & Ambiente:** PostgreSQL, VS Code, Git e GitHub.
- **DDL & DML:** Modelagem de tabelas, tipos de dados (`DECIMAL`, `DATE`, `VARCHAR`), constraints (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`).
- **DQL & Análise Relacional:**
  - Junções: `INNER JOIN`, `LEFT JOIN`, Anti-Joins (`IS NULL`), predicados na cláusula `ON`.
  - Agregações & Filtros: `GROUP BY`, `HAVING`, `COUNT(DISTINCT)`, `SUM`, `AVG`, `ROUND`.
  - Tratamento de Dados: `COALESCE` para substituição de valores `NULL` em relatórios gerenciais.

---

## 🗄️ Modelagem Relacional (Schema)

```text
+-------------------+              +----------------------+
|     CLIENTES      |              |       PEDIDOS        |
+-------------------+              +----------------------+
| id_cliente (PK)   | 1 -------- < N | id_pedido (PK)       |
| nome              |              | id_cliente (FK)      |
| cidade            |              | categoria            |
| estado            |              | valor                |
|                   |              | status               |
|                   |              | data_pedido          |
+-------------------+              +----------------------+
