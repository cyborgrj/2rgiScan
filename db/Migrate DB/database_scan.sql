-- Criação do banco de dados (executar no PostgreSQL como usuário com permissões)
CREATE DATABASE rgiscan_db;

-- Conectar ao banco criado antes de continuar:
-- \c rgiscan_db

-- Tabelas de auditoria:

CREATE TABLE IF NOT EXISTS Protocolo (
    numprot TEXT,
    operacao TEXT,
    usuario TEXT,
    data_hora TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Matricula (
    nummat TEXT,
    operacao TEXT,
    usuario TEXT,
    data_hora TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Certidao (
    numcert TEXT,
    anocert TEXT,
    operacao TEXT,
    usuario TEXT,
    data_hora TIMESTAMP
);

CREATE TABLE IF NOT EXISTS RegistroAuxiliar (
    numreg TEXT,
    operacao TEXT,
    usuario TEXT,
    data_hora TIMESTAMP
);

CREATE TABLE IF NOT EXISTS CertidaoCancelada (
    numcertcanc TEXT,
    anocertcanc TEXT,
    operacao TEXT,
    usuario TEXT,
    data_hora TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ProtocoloCancelado (
    numprotcanc TEXT,
    operacao TEXT,
    usuario TEXT,
    data_hora TIMESTAMP
);


-- certidao
ALTER TABLE certidao RENAME COLUMN operacao TO tipo_alteracao;
ALTER TABLE certidao ADD COLUMN qtd_paginas INTEGER;

-- certidaocancelada
ALTER TABLE certidaocancelada RENAME COLUMN operacao TO tipo_alteracao;
ALTER TABLE certidaocancelada ADD COLUMN qtd_paginas INTEGER;

-- matricula
ALTER TABLE matricula RENAME COLUMN operacao TO tipo_alteracao;
ALTER TABLE matricula ADD COLUMN qtd_paginas INTEGER;

-- protocolo
ALTER TABLE protocolo RENAME COLUMN operacao TO tipo_alteracao;
ALTER TABLE protocolo ADD COLUMN qtd_paginas INTEGER;

-- protocolocancelado
ALTER TABLE protocolocancelado RENAME COLUMN operacao TO tipo_alteracao;
ALTER TABLE protocolocancelado ADD COLUMN qtd_paginas INTEGER;

-- registroauxiliar
ALTER TABLE registroauxiliar RENAME COLUMN operacao TO tipo_alteracao;
ALTER TABLE registroauxiliar ADD COLUMN qtd_paginas INTEGER;


UPDATE Protocolo SET data_hora = date_trunc('second', data_hora);
UPDATE Matricula SET data_hora = date_trunc('second', data_hora);
UPDATE Certidao SET data_hora = date_trunc('second', data_hora);
UPDATE RegistroAuxiliar SET data_hora = date_trunc('second', data_hora);
UPDATE CertidaoCancelada SET data_hora = date_trunc('second', data_hora);
UPDATE ProtocoloCancelado SET data_hora = date_trunc('second', data_hora);

-- Adiciona o campo 'correto' com restrição e valor padrão
ALTER TABLE Matricula ADD COLUMN correto CHAR(1) CHECK (correto IN ('S', 'N')) DEFAULT 'S';
ALTER TABLE Protocolo ADD COLUMN correto CHAR(1) CHECK (correto IN ('S', 'N')) DEFAULT 'S';
ALTER TABLE RegistroAuxiliar ADD COLUMN correto CHAR(1) CHECK (correto IN ('S', 'N')) DEFAULT 'S';
ALTER TABLE ProtocoloCancelado ADD COLUMN correto CHAR(1) CHECK (correto IN ('S', 'N')) DEFAULT 'S';
ALTER TABLE Certidao ADD COLUMN correto CHAR(1) CHECK (correto IN ('S', 'N')) DEFAULT 'S';
ALTER TABLE CertidaoCancelada ADD COLUMN correto CHAR(1) CHECK (correto IN ('S', 'N')) DEFAULT 'S';

-- Garante que os registros existentes estejam com valor 'S'
UPDATE Matricula SET correto = 'S' WHERE correto IS NULL;
UPDATE Protocolo SET correto = 'S' WHERE correto IS NULL;
UPDATE RegistroAuxiliar SET correto = 'S' WHERE correto IS NULL;
UPDATE ProtocoloCancelado SET correto = 'S' WHERE correto IS NULL;
UPDATE Certidao SET correto = 'S' WHERE correto IS NULL;
UPDATE CertidaoCancelada SET correto = 'S' WHERE correto IS NULL;


CREATE TABLE documentos_simples (
    id SERIAL PRIMARY KEY,
    tipo_documento VARCHAR(255) NOT NULL,
    nome_documento VARCHAR(255) NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
