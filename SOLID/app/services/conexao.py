import sqlite3

_conexao = None


def obterConexao():
    conexao = sqlite3.connect('db_solid.sqlite3')
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao


def Conectar():
    global _conexao
    if _conexao is None:
        try:
            _conexao = obterConexao()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    return _conexao