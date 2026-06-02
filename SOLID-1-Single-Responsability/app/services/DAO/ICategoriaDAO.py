import sys
import sqlite3

from django import forms
from django.urls import reverse

from conexao import Conectar

conexao = Conectar()

def categoriaIncluir(Categoria):
    return conexao.execute("INSERT INTO categoria (nome) VALUES (?)", (Categoria.nome,)).lastrowid

def categoriaAlterar(Categoria):
    return conexao.execute("UPDATE categoria SET nome = ? WHERE id = ?", (Categoria.nome, Categoria.id)).rowcount

def categoriaExcluir(Categoria):
    return conexao.execute("DELETE FROM categoria WHERE id = ?", (Categoria.id,)).rowcount

def categoriaObter_por_id(id):
    return conexao.execute("SELECT * FROM categoria WHERE id = ?", (id,)).fetchone()

def categoriaListar():
    return conexao.execute("SELECT * FROM categoria").fetchall()
