-- Estudo de Caso 2 - Extraindo Relatórios do Data Warehouse com Linguagem SQL


-- Cria a tabela
CREATE TABLE IF NOT EXISTS dw.tb_relatorio_vendas_acima_10000 (
    Cliente VARCHAR(255),
    TotalFaturamento DECIMAL(10, 2)
);


-- Stored Procedure para gravar em uma tabela os clientes que geraram faturamento acima de 10000
CREATE OR REPLACE PROCEDURE dw.sp_relatorio_vendas_cliente()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Cria uma tabela temporária para armazenar o relatório de vendas
    CREATE TEMP TABLE IF NOT EXISTS temp_sales_report ON COMMIT DROP AS
    SELECT 
        c.Nome AS Cliente,
        SUM(v.Faturamento) AS TotalFaturamento
    FROM 
        dw.Vendas v
    JOIN 
        dw.Cliente c ON v.ClienteID = c.ClienteID
    GROUP BY 
        c.Nome
    ORDER BY 
        TotalFaturamento DESC;
    
    -- Insere na tabela de relatório somente os clientes com total de faturamento maior que 10000
    INSERT INTO dw.tb_relatorio_vendas_acima_10000(Cliente, TotalFaturamento)
    SELECT 
        Cliente,
        TotalFaturamento
    FROM 
        temp_sales_report
    WHERE 
        TotalFaturamento > 10000;
    
END;
$$;


-- Executa a SP
CALL dw.sp_relatorio_vendas_cliente();


-- Select na tabela
SELECT * FROM dw.tb_relatorio_vendas_acima_10000;


-- Tabela de Cliente
SELECT * FROM dw.Cliente;


-- Função que retorna o total de vendas por categoria para o cliente desejado
-- indicando se o total de vendas supera 100.000
CREATE OR REPLACE FUNCTION dw.fn_relatorio_vendas_categoria(NomeCliente VARCHAR(255))
RETURNS TABLE(
    Categoria VARCHAR(255), 
    TotalVendas DECIMAL(10,2),
    Supera100000 VARCHAR(5) 
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verifica se o NomeCliente está no formato correto ('Cliente DSA ' seguido de números)
    IF NomeCliente ~ 'Cliente DSA [0-9]+' THEN
        RETURN QUERY
        SELECT 
            p.NomeCategoria AS Categoria,
            SUM(v.Faturamento) AS TotalVendas,
            CASE
                WHEN SUM(v.Faturamento) > 100000 THEN 'Sim'::VARCHAR(5)
                ELSE 'Não'::VARCHAR(5)
            END AS Supera100000 
        FROM 
            dw.Vendas v
        JOIN 
            dw.Produto p ON v.ProdutoID = p.ProdutoID
        JOIN
            dw.Cliente c ON v.ClienteID = c.ClienteID
        WHERE 
            c.Nome = NomeCliente
        GROUP BY 
            p.NomeCategoria
        ORDER BY 
            p.NomeCategoria;
    ELSE
        RAISE EXCEPTION 'O nome do cliente não está no formato esperado: ''Cliente DSA [0-9]+''';
    END IF;
END;
$$;


-- Executa a função
SELECT * FROM dw.fn_relatorio_vendas_categoria('Cliente DSA 10');
SELECT * FROM dw.fn_relatorio_vendas_categoria('Cliente DSA 42');
SELECT * FROM dw.fn_relatorio_vendas_categoria('Cliente DSA');




