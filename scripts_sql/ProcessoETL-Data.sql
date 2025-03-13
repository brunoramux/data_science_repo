-- Estudo de Caso 1 - Construindo e Implementando Modelo de Dados Para Portal de E-commerce
-- Processo ETL da Tabela de Data


-- Cria a Function
CREATE OR REPLACE FUNCTION dw.gerar_datas()
RETURNS VOID AS $$
DECLARE
    data_atual DATE;
BEGIN
    data_atual := '2021-01-01'; -- Data de início

    WHILE data_atual <= '2025-12-31' LOOP
        INSERT INTO dw.Data (Data, Dia, Mes, Ano, DiaDaSemana)
        VALUES (data_atual, EXTRACT(DAY FROM data_atual), EXTRACT(MONTH FROM data_atual), EXTRACT(YEAR FROM data_atual), TO_CHAR(data_atual, 'Day'));

        data_atual := data_atual + INTERVAL '1 day'; -- Incrementa um dia
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- Executa a Function
SELECT dw.gerar_datas();


-- Visualiza os dados
SELECT * FROM dw.data;



