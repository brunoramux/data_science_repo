-- Estudo de Caso 1 - Construindo e Implementando Modelo de Dados Para Portal de E-commerce
-- Processo ETL da Tabela de Distribuidor


-- Cria a Function
CREATE OR REPLACE FUNCTION dw.etl_distribuidores(num_distribuidores INTEGER)
RETURNS VOID AS $$
DECLARE
    i INTEGER := 1;
    nome_distribuidor VARCHAR;
    cidade_distribuidor VARCHAR;
    pais_distribuidor VARCHAR;
    locais_distribuidor VARCHAR[] := ARRAY['São Paulo, Brasil', 'Rio de Janeiro, Brasil', 'New York, EUA', 'Los Angeles, EUA', 'Lisboa, Portugal', 'Madrid, Espanha'];
BEGIN
    WHILE i <= num_distribuidores LOOP
        nome_distribuidor := 'Distribuidor ' || i::TEXT;
        cidade_distribuidor := SPLIT_PART(locais_distribuidor[(i - 1) % ARRAY_LENGTH(locais_distribuidor, 1) + 1], ', ', 1);
        pais_distribuidor := SPLIT_PART(locais_distribuidor[(i - 1) % ARRAY_LENGTH(locais_distribuidor, 1) + 1], ', ', 2);

        INSERT INTO dw.Distribuidor (NomeDistribuidor, CidadeDistribuidor, PaisDistribuidor)
        VALUES (nome_distribuidor, cidade_distribuidor, pais_distribuidor);

        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- Executa a Function
SELECT dw.etl_distribuidores(30);


-- Visualiza os dados
SELECT * FROM dw.distribuidor;



