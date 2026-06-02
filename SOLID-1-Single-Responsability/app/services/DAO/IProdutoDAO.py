import sys
import sqlite3

from django import forms
from django.urls import reverse

from conexao import Conectar

conexao = Conectar()

def produtoIncluir(produto):
    return conexao.execute("INSERT INTO produto (nome) VALUES (?)", (produto.nome,)).lastrowid

def produtoAlterar(produto):
    return conexao.execute("UPDATE produto SET nome = ? WHERE id = ?", (produto.nome, produto.id)).rowcount

def produtoExcluir(produto):
    return conexao.execute("DELETE FROM produto WHERE id = ?", (produto.id,)).rowcount

def produtoObter_por_id(id):
    return conexao.execute("SELECT * FROM produto WHERE id = ?", (id,)).fetchone()
    
def produtoListar():
    return conexao.execute("SELECT * FROM produto").fetchall()