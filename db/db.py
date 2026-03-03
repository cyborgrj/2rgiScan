import sqlite3
import bcrypt
import configparser
import os


class DataBaseUsers:
    def __init__(self, config_path="config.ini", override_path=None):
        self.config_path = config_path
        self.dbname = self.load_config() if override_path is None else override_path
        self.connect_users()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        caminho_servidor = config.get("REDES", "servidor")
        caminho_banco = config.get("sqlite", "user_db_path")

        return os.path.join(caminho_servidor, caminho_banco)

    def connect_users(self):
        try:
            self.db = sqlite3.connect(self.dbname)
        except Exception as error:
            print(f"Erro ao conectar: {error}")
        else:
            self.cursor = self.db.cursor()

    def close_users(self):
        try:
            self.db.close()
        except Exception as error:
            print(f"Erro ao fechar o banco SQLite3 (users): {error}")

    def insert_users(self, user, password, access, user_name) -> str:
        self.connect_users()
        self.cursor = self.db.cursor()
        sigla = user.lower()
        print("Início de cadastro de usuários")
        acessoByte = access.encode("utf-8")
        pwdByte = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashPwd = bcrypt.hashpw(pwdByte, salt)
        hashAcesso = bcrypt.hashpw(acessoByte, salt)
        self.cursor.execute("""SELECT * FROM users WHERE user=?""", (sigla,))
        found = self.cursor.fetchone()
        if found is not None:
            print("Usuário já cadastrado!")
            self.cursor.close()
            self.close_users()
            return "existente"
        else:
            self.cursor.execute(
                """INSERT INTO users(user, password, access, username) 
                            VALUES(?,?,?,?)""",
                (sigla, hashPwd, hashAcesso, user_name),
            )
            self.cursor.close()
            self.db.commit()
            self.close_users()
            return "sucesso"

    def update_user(self, user, password, access, user_name):
        self.connect_users()
        sigla = user.lower()
        acessoByte = access.encode("utf-8")
        pwdByte = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashPwd = bcrypt.hashpw(pwdByte, salt)
        hashAcesso = bcrypt.hashpw(acessoByte, salt)

        self.cursor.execute(
            """UPDATE users 
                            SET password = ?, access = ?, username = ?
                            WHERE user = ?""",
            (hashPwd, hashAcesso, user_name, sigla),
        )
        self.db.commit()
        self.cursor.close()
        self.close_users()

    def get_sigla_users(self):
        self.connect_users()
        usuarios = self.cursor.execute("SELECT user, username FROM users").fetchall()
        self.cursor.close()
        self.close_users()
        return usuarios

    def get_sigla_by_nome(self, nome_completo):
        self.connect_users()
        result = self.cursor.execute(
            "SELECT user FROM users WHERE username = ?", (nome_completo,)
        ).fetchone()
        self.cursor.close()
        self.close_users()
        return result[0] if result else None

    def get_user_info(self, sigla):
        self.connect_users()
        self.cursor = self.db.cursor()

        try:
            self.cursor.execute(
                "SELECT username, access FROM users WHERE user = ?", (sigla.lower(),)
            )
            found = self.cursor.fetchone()
            if found:
                nome_completo, access_hash = found

                # Lista completa de acessos
                lista_acessos_completa = [
                    "administrador",
                    "digitalização",
                    "documentos",
                    "consulta",
                    "digitalização_simples",
                    "digitalização_entrada",
                ]

                # Verifica qual é o acesso correspondente (descriptografado)
                for acesso in lista_acessos_completa:
                    if bcrypt.checkpw(acesso.encode("utf-8"), access_hash):
                        self.cursor.close()
                        self.close_users()
                        return {
                            "existe": True,
                            "nome_usuario": nome_completo,
                            "acesso": acesso,
                        }

                # Se o acesso não for reconhecido
                self.cursor.close()
                self.close_users()
                return {
                    "existe": True,
                    "nome_usuario": nome_completo,
                    "acesso": "desconhecido",
                }

            else:
                self.cursor.close()
                self.close_users()
                return {"existe": False}

        except Exception as erro:
            self.cursor.close()
            self.close_users()
            print(f"Erro ao buscar usuário: {erro}")
            return {"existe": False, "erro": str(erro)}

    def listar_nomes_usuarios(self, siglas):
        self.connect_users()
        self.cursor = self.db.cursor()
        try:
            nomes = []
            for sigla in siglas:
                self.cursor.execute(
                    "SELECT username FROM users WHERE user = ?", (sigla.lower(),)
                )
                row = self.cursor.fetchone()
                if row:
                    nomes.append(row[0])
            return nomes
        finally:
            self.cursor.close()
            self.close_users()

    def check_users(self, user, password):
        self.connect_users()
        found = None
        acesso_usuario = ""
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute("""SELECT * FROM users WHERE user=?""", (user,))
        except Exception as error:
            print(f"Erro: {error}")
            self.cursor.close()
            self.close_users()
            return "credenciais", "incorretas"
        else:
            found = self.cursor.fetchone()
            if found is not None:
                stored_psswd = found[2]
                stored_acesso = found[3]
                user_name = found[1]
                lista_acessos = [
                    "administrador",
                    "digitalização",
                    "documentos",
                    "consulta",
                    "digitalização_simples",
                    "digitalização_entrada",
                ]

                typed_psswd = password.encode("utf-8")

                try:
                    psswd_ok = bcrypt.checkpw(typed_psswd, stored_psswd)
                except:
                    self.cursor.close()
                    self.close_users()
                    return "credenciais", "incorretas"

                for acesso in lista_acessos:
                    chk_acesso = acesso.encode("utf-8")
                    if bcrypt.checkpw(chk_acesso, stored_acesso):
                        acesso_usuario = acesso
                        break

                if psswd_ok and acesso_usuario != "":
                    self.cursor.close()
                    self.close_users()
                    return user_name, acesso_usuario
                else:
                    self.cursor.close()
                    self.close_users()
                    return "credenciais", "incorretas"
            else:
                self.cursor.close()
                self.close_users()
                return "credenciais", "incorretas"


if __name__ == "__main__":
    print("Caso ainda não exista um banco criar com dbtest.py")
    sigla = "edu"
    password = "1234"
    acesso = "administrador"
    nome_usuario = "Eduardo Rossini Xavier da Silva"
    db_test = DataBaseUsers()

    db_test.insert_users(
        user=sigla, password=password, access=acesso, user_name=nome_usuario
    )

    print(db_test.get_sigla_users())

    print(db_test.check_users(sigla, password))

    db_test.close_users()
