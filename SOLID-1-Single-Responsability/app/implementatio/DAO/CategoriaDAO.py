from conexao import Conectar
from ICategoriaDAO import ICategoriaDAO
 

class CategoriaDAO(ICategoriaDAO):
    def __init__(self):
        self._conexao = Conectar()
 
 
    def categoriaIncluir(self, categoria):
        return self._conexao.execute( "INSERT INTO categoria (nome) VALUES (?)", (categoria.nome,) ).lastrowid
 
 
    def categoriaAlterar(self, categoria):
        return self._conexao.execute( "UPDATE categoria SET nome = ? WHERE id = ?", (categoria.nome, categoria.id) ).rowcount
 
 
    def categoriaExcluir(self, categoria):
        return self._conexao.execute( "DELETE FROM categoria WHERE id = ?", (categoria.id,) ).rowcount

 
    def categoriaObter_por_id(self, id):
        return self._conexao.execute( "SELECT * FROM categoria WHERE id = ?", (id,) ).fetchone()
 
 
    def categoriaListar(self):
        return self._conexao.execute( "SELECT * FROM categoria" ).fetchall()