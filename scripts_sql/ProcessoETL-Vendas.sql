-- Estudo de Caso 1 - Construindo e Implementando Modelo de Dados Para Portal de E-commerce
-- Processo ETL da Tabela de Vendas


-- Cria a Function
CREATE OR REPLACE FUNCTION dw.etl_vendas(num_vendas INTEGER)
RETURNS VOID AS $$
DECLARE
    i INT := 1;
    cliente_id INT;
    produto_id INT;
    distribuidor_id INT;
    data_id INT;
    quantidade_vendida INT;
    faturamento DECIMAL;
    custo_frete DECIMAL;
BEGIN
    FOR i IN 1..num_vendas LOOP
    
        -- Selecionar IDs aleatórios das tabelas de dimensão
        SELECT INTO cliente_id ClienteID FROM dw.Cliente ORDER BY RANDOM() LIMIT 1;
        SELECT INTO produto_id ProdutoID FROM dw.Produto ORDER BY RANDOM() LIMIT 1;
        SELECT INTO distribuidor_id DistribuidorID FROM dw.Distribuidor ORDER BY RANDOM() LIMIT 1;
        SELECT INTO data_id DataID FROM dw.Data ORDER BY RANDOM() LIMIT 1;

        -- Gerar dados fictícios para os outros campos
        quantidade_vendida := TRUNC(RANDOM() * 100 + 1);
        faturamento := quantidade_vendida * (RANDOM() * 100);
        custo_frete := faturamento * RANDOM() * 0.1;  -- Custo de frete aleatório, até 10% do faturamento

        INSERT INTO dw.Vendas (ClienteID, ProdutoID, DistribuidorID, DataID, QuantidadeVendida, Faturamento, CustoFrete)
        VALUES (cliente_id, produto_id, distribuidor_id, data_id, quantidade_vendida, faturamento, custo_frete);
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- Executa a Function
SELECT dw.etl_vendas(10000);


-- Visualiza os dados
SELECT * FROM dw.vendas;



