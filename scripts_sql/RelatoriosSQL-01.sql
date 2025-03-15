-- Estudo de Caso 2 - Extraindo Relatórios do Data Warehouse com Linguagem SQL


-- (SQL Nível Básico)


-- Listar todos os Produtos 
SELECT *
FROM dw.Produto;


-- Listar nome, preço e categoria
SELECT Nome, Preco, NomeCategoria
FROM dw.Produto;


-- Listar todos os produtos da Categoria 2
SELECT Nome, Preco, NomeCategoria
FROM dw.Produto
WHERE NomeCategoria = 'Categoria 2';


-- Funções de agregação
SELECT COUNT(Preco), MIN(Preco), SUM(Preco), AVG(Preco), MAX(Preco)
FROM dw.Produto;


-- Funções de agregação e arrendondamento
SELECT COUNT(Preco), MIN(Preco), SUM(Preco), ROUND(AVG(Preco), 2), MAX(Preco)
FROM dw.Produto;


-- Funções de agregação e arrendondamento, com alias
SELECT COUNT(Preco) AS contagem, 
       MIN(Preco) AS valor_minimo, 
       SUM(Preco) AS total, 
       ROUND(AVG(Preco), 2) AS media, 
       MAX(Preco) AS valor_maximo
FROM dw.Produto;


-- Funções de agregação com filtro
SELECT COUNT(Preco) AS contagem, 
       MIN(Preco) AS valor_minimo, 
       SUM(Preco) AS total, 
       ROUND(AVG(Preco), 2) AS media, 
       MAX(Preco) AS valor_maximo
FROM dw.Produto
WHERE NomeCategoria = 'Categoria 2';


-- (SQL Nível Intermediário)


-- Listar os produtos da Categoria 2 e preço maior que 350
SELECT Nome, Preco, NomeCategoria
FROM dw.Produto
WHERE NomeCategoria = 'Categoria 2' AND Preco > 350;


-- Listar os produtos da Categoria 2 ou preço maior que 350
SELECT Nome, Preco, NomeCategoria
FROM dw.Produto
WHERE NomeCategoria = 'Categoria 2' OR Preco > 350;


-- Listar os produtos da Categoria 2 e preço maior que 350, ou apenas preço maior que 350
SELECT Nome, Preco, NomeCategoria
FROM dw.Produto
WHERE (NomeCategoria = 'Categoria 2' AND Preco > 350) OR Preco > 350;


-- Listar nome, categoria e quantidade vendida para cada produto
SELECT p.nome, p.nomecategoria, v.quantidadevendida
FROM dw.Produto p
JOIN dw.Vendas v ON v.produtoid = p.produtoid;


-- Listar nome, categoria, quantidade vendida e data de venda para cada produto
SELECT p.nome, p.nomecategoria, v.quantidadevendida, d.data
FROM dw.Produto p
JOIN dw.Vendas v ON v.produtoid = p.produtoid
JOIN dw.data d ON v.dataid = d.dataid;


-- Listar nome, categoria, quantidade vendida, data de venda e país do cliente, para cada produto
SELECT p.nome, p.nomecategoria, v.quantidadevendida, d.data, c.paiscliente
FROM dw.Produto p
JOIN dw.Vendas v ON v.produtoid = p.produtoid
JOIN dw.data d ON v.dataid = d.dataid
JOIN dw.cliente c ON v.clienteid = c.clienteid;


-- Listar nome, categoria, quantidade vendida, data de venda, país do cliente e nome do distribuidor
-- para cada produto
SELECT p.nome, p.nomecategoria, v.quantidadevendida, dt.data, c.paiscliente, d.nomedistribuidor
FROM dw.Produto p
JOIN dw.Vendas v ON v.produtoid = p.produtoid
JOIN dw.data dt ON v.dataid = dt.dataid
JOIN dw.cliente c ON v.clienteid = c.clienteid
JOIN dw.distribuidor d ON v.distribuidorid = d.distribuidorid;


-- Listar nome, categoria, quantidade vendida, data de venda, país do cliente e nome do distribuidor
-- para cada produto que atenda esta regra: 
-- produtos da Categoria 2 e preço maior que 350, ou apenas preço maior que 350
SELECT p.nome, p.nomecategoria, v.quantidadevendida, dt.data, c.paiscliente, d.nomedistribuidor
FROM dw.Produto p
JOIN dw.Vendas v ON v.produtoid = p.produtoid
JOIN dw.data dt ON v.dataid = dt.dataid
JOIN dw.cliente c ON v.clienteid = c.clienteid
JOIN dw.distribuidor d ON v.distribuidorid = d.distribuidorid
WHERE (NomeCategoria = 'Categoria 2' AND Preco > 350) OR Preco > 350;


-- (SQL Nível Avançado)


-- Média de Preço por Categoria de Produto 
SELECT p.NomeCategoria, ROUND(AVG(p.Preco),2) AS MediaPreco
FROM dw.Produto p 
GROUP BY p.NomeCategoria;


-- Média de Faturamento por Categoria de Produto 
SELECT p.NomeCategoria, ROUND(AVG(v.Faturamento),2) AS MediaFaturamento
FROM dw.Vendas v
JOIN dw.Produto p ON v.ProdutoID = p.ProdutoID
GROUP BY p.NomeCategoria;


-- Soma do Faturamento por Cidade do Cliente 
SELECT c.CidadeCliente, SUM(v.Faturamento) AS TotalFaturamento
FROM dw.Vendas v
JOIN dw.Cliente c ON v.ClienteID = c.ClienteID
GROUP BY c.CidadeCliente;


-- Faturamento Médio por Dia da Semana, Ordenado Por Faturamento 
-- e Somente Para Dias Úteis 
SELECT d.DiaDaSemana, ROUND(AVG(v.Faturamento),2) AS MediaFaturamento
FROM dw.Vendas v
JOIN dw.Data d ON v.DataID = d.DataID
WHERE TRIM(d.DiaDaSemana) NOT IN ('Sunday', 'Saturday')
GROUP BY d.DiaDaSemana
ORDER BY MediaFaturamento DESC;


-- Total de Vendas e Custo de Frete por País do Cliente e Categoria de Produto, para o Ano de 2024 
SELECT c.PaisCliente, p.NomeCategoria, SUM(v.QuantidadeVendida) AS TotalVendas, SUM(v.CustoFrete) AS TotalCustoFrete
FROM dw.Vendas v
JOIN dw.Cliente c ON v.ClienteID = c.ClienteID
JOIN dw.Produto p ON v.ProdutoID = p.ProdutoID
JOIN dw.Data d ON v.DataID = d.DataID
WHERE d.Ano = 2024
GROUP BY c.PaisCliente, p.NomeCategoria
ORDER BY c.PaisCliente, p.NomeCategoria;


-- Interprete a query abaixo
SELECT p.nomecategoria, 
       d.nomedistribuidor, 
       MIN(v.quantidadevendida) AS ValorMinimo,
       ROUND(AVG(v.quantidadevendida), 2) AS MediaQuantidadeVendida,
       MAX(v.quantidadevendida) AS ValorMaximo
FROM dw.Produto p
JOIN dw.Vendas v ON v.produtoid = p.produtoid
JOIN dw.data dt ON v.dataid = dt.dataid
JOIN dw.cliente c ON v.clienteid = c.clienteid
JOIN dw.distribuidor d ON v.distribuidorid = d.distribuidorid
WHERE ((c.CidadeCliente = 'New York' AND Preco > 350) OR Preco > 350) 
  AND TRIM(dt.DiaDaSemana) NOT IN ('Sunday', 'Saturday')
GROUP BY p.nomecategoria, d.nomedistribuidor
ORDER BY p.nomecategoria, d.nomedistribuidor;



-- (SQL Nível Ninja Master)


-- Total de Vendas e Custo de Frete por País do Cliente e Categoria de Produto, para o Ano de 2024 
-- somente se o custo total de frete for maior do que 30.000 
SELECT c.PaisCliente, p.NomeCategoria, SUM(v.QuantidadeVendida) AS TotalVendas, SUM(v.CustoFrete) AS TotalCustoFrete
FROM dw.Vendas v
JOIN dw.Cliente c ON v.ClienteID = c.ClienteID
JOIN dw.Produto p ON v.ProdutoID = p.ProdutoID
JOIN dw.Data d ON v.DataID = d.DataID
WHERE d.Ano = 2024
GROUP BY c.PaisCliente, p.NomeCategoria
HAVING SUM(v.CustoFrete) > 30000
ORDER BY c.PaisCliente, p.NomeCategoria;


-- Para ilustrar o uso de subquery no contexto deste modelo de dados, vamos criar uma consulta que identifique 
-- os clientes que realizaram compras acima da média. Esta consulta irá calcular o total de faturamento por cliente e, 
-- em seguida, utilizar uma subquery para selecionar apenas aqueles clientes cujo total de faturamento 
-- esteja acima da média.
SELECT c.ClienteID, c.Nome, SUM(v.Faturamento) AS TotalFaturamento
FROM dw.Vendas v
JOIN dw.Cliente c ON v.ClienteID = c.ClienteID
GROUP BY c.ClienteID
HAVING SUM(v.Faturamento) > (
    SELECT AVG(TotalFaturamento) 
    FROM (
        SELECT SUM(v.Faturamento) AS TotalFaturamento
        FROM dw.Vendas v
        GROUP BY v.ClienteID
    ) AS SubQuery
)
ORDER BY TotalFaturamento DESC;


-- Mesma query detalhada:

SELECT c.Nome, SUM(v.Faturamento) AS TotalFaturamento
FROM dw.Vendas v
JOIN dw.Cliente c ON v.ClienteID = c.ClienteID
GROUP BY c.Nome

-- Retorna somente os cliente cujo total de faturamento tenha sido acima da média
HAVING SUM(v.Faturamento) > (
    
    -- Calcula a média de faturamento  
    SELECT AVG(TotalFaturamento) 
    FROM (
        
        -- Calcula a soma de faturamento por cliente
        SELECT SUM(v.Faturamento) AS TotalFaturamento
        FROM dw.Vendas v
        GROUP BY v.ClienteID
    ) AS SubQuery
)
ORDER BY TotalFaturamento DESC;


-- Neste exemplo, a subquery interna calcula o faturamento total por cliente e, em seguida, a subquery externa 
-- calcula a média desses totais de faturamento. A cláusula HAVING é então usada para filtrar apenas os clientes 
-- cujo total de faturamento é maior que a média calculada. Este é um exemplo clássico de como as subqueries 
-- podem ser utilizadas para realizar operações de comparação complexas dentro de consultas SQL, permitindo análises 
-- mais profundas e insights mais detalhados a partir dos dados disponíveis no banco de dados.


-- (SQL Nível Ninja Master das Galáxias)


-- Para ilustrar o uso de uma função de janela (window function) em SQL vamos criar uma consulta 
-- que calcula o total cumulativo de vendas em termos de faturamento por cliente, ordenado por data. 
-- Esse tipo de consulta é útil para análises temporais, como entender como o faturamento se acumula 
-- ao longo do tempo para cada cliente.

-- Suponha que queremos calcular o total cumulativo de faturamento para cada cliente, ordenado pela data da venda. 
-- Vamos utilizar a tabela Vendas em junção com a tabela Data para ter acesso às datas das vendas e a tabela Cliente 
-- para identificar os clientes. 
SELECT c.Nome, 
       d.Data, 
       v.Faturamento,
	   SUM(v.Faturamento) OVER (PARTITION BY v.ClienteID ORDER BY d.Data ASC) AS TotalCumulativo
FROM 
    dw.Vendas v
JOIN 
    dw.Cliente c ON v.ClienteID = c.ClienteID
JOIN 
    dw.Data d ON v.DataID = d.DataID
ORDER BY 
    c.Nome, d.Data;

-- Nesta consulta, utilizamos a função SUM() como uma função de janela (definida pelo OVER()), 
-- que calcula a soma cumulativa do faturamento. A cláusula PARTITION BY v.ClienteID garante que o cálculo 
-- do total cumulativo seja reiniciado para cada cliente. A ordenação dentro de cada partição é especificada 
-- por ORDER BY d.Data ASC, o que significa que as vendas são somadas na ordem cronológica.






