import sys
import sqlite3

from django import forms
from django.urls import reverse

class ServiceCateogria:

    # obtem a conexao com o banco de dados
    conexao = sqlite3.connect('db_solid.sqlite3')
    # comando para não permitir DELETE CASCADE (exclusão em cascata)
    conexao.execute("PRAGMA foreign_keys = ON;")
    
    def listarCategoria():

        # define o comando SQL que será executado
        sql = '''
            SELECT  id, 
                descricao
            FROM Categoria 
            ORDER BY descricao
        '''

        # cria um cursor(), executa o SELECT informado e traz os todos os registros
        registros = conexao.cursor().execute(sql).fetchall()

        return registros
    
    def salvarCategoria():
        if acao_form == 'Inclusão':
            sql = f"INSERT INTO Categoria(descricao) VALUES('{form_data['descricao']}')"

        elif acao_form == 'Exclusão':
            sql = f"DELETE FROM Categoria WHERE id = {form_data['id']}"

        else:
            sql = f'''
                UPDATE Categoria 
                SET descricao = '{form_data['descricao']}' 
                WHERE id = {form_data['id']}
            '''

        # cria um cursor() e executa o SQL informado
        conexao.cursor().execute(sql)
        conexao.commit()
        