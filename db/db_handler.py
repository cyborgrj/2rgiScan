import psycopg2
import configparser
from utils.logger import logger
import traceback
import os

class DBHandler:
    def __init__(self, config_path='config.ini', override_config=None):
        self.config_path = config_path
        self.db_config = self.load_config()

        if override_config:
            self.db_config.update(override_config)  # permite sobrescrever configs

        self.conn = None
        self.cursor = None
        self.connect()
        # self.cria_tabela_teste()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)

        return {
            "host": config.get('postgresql', 'host'),
            "port": config.getint('postgresql', 'port'),
            "dbname": config.get('postgresql', 'database'),
            "user": config.get('postgresql', 'user'),
            "password": config.get('postgresql', 'password')
        }

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            logger.info("Conexão com o banco de dados PostgreSQL estabelecida com sucesso.")
        except Exception as e:
            logger.error("Erro ao conectar com o banco de dados PostgreSQL.")
            logger.error(f"Config usada: {self.db_config}")
            logger.error(traceback.format_exc())
            self.conn = None
            self.cursor = None

    def get_conn(self):
        return psycopg2.connect(**self.db_config)

    def cria_tabela_teste(self):
        if self.conn is None:
            logger.error("Não foi possível criar tabelas porque a conexão com o PostgreSQL falhou.")
            return
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS teste (
                    id SERIAL PRIMARY KEY,
                    teste TEXT NOT NULL,
                );
            """)
            self.conn.commit()
            logger.info("Tabela 'teste' verificada/criada com sucesso.")
        except Exception as e:
            logger.error("Erro ao criar a tabela 'teste'.")
            logger.error(traceback.format_exc())


    def conexao_ativa(self):
        try:
            self.cursor.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Conexão com banco perdida: {e}")
            return False


    def inserir_dado(self, tabela, colunas, valores):
        try:
            placeholders = ', '.join(['%s'] * len(valores))
            query = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
            self.cursor.execute(query, valores)
            self.conn.commit()
            logger.info(f"Dado inserido com sucesso na tabela {tabela}.")
        except psycopg2.OperationalError as e:
            logger.error("Erro de conexão com o banco durante a inserção.")
            logger.error(traceback.format_exc())
            raise ConnectionError("A conexão com o banco foi perdida.")
        except psycopg2.InterfaceError as e:
            logger.error("Erro de interface com o banco.")
            logger.error(traceback.format_exc())
            raise ConnectionError("A conexão com o banco foi encerrada.")


    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logger.info("Conexão com o banco de dados PostgreSQL encerrada.")

if __name__ == "__main__":
    pass