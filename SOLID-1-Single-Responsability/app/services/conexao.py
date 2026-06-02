import sys
import sqlite3


def obterConexao():
    # obtem a conexao com o banco de dados
    conexao = sqlite3.connect('db_solid.sqlite3')
    # comando para não permitir DELETE CASCADE (exclusão em cascata)
    conexao.execute("PRAGMA foreign_keys = ON;") 
    return conexao

def Conectar():
    private static sqlite3.Connection conexao = null;
    if(conexao == null):
        try:
            conexao = obterConexao()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    return conexao