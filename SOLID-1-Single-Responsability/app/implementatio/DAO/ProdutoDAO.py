from conexao import Conectar
from IProdutoDAO import IProdutoDAO
 

class ProdutoDAO(IProdutoDAO):
    def __init__(self):
        self._conexao = Conectar()
 
 
    def produtoIncluir(self, produto):
        return self._conexao.execute( "INSERT INTO produto (nome) VALUES (?)", (produto.nome,) ).lastrowid
 
 
    def produtoAlterar(self, produto):
        return self._conexao.execute( "UPDATE produto SET nome = ? WHERE id = ?", (produto.nome, produto.id) ).rowcount
 
 
    def produtoExcluir(self, produto):
        return self._conexao.execute( "DELETE FROM produto WHERE id = ?", (produto.id,) ).rowcount

 
    def produtoObter_por_id(self, id):
        return self._conexao.execute( "SELECT * FROM produto WHERE id = ?", (id,) ).fetchone()
 
 
    def produtoListar(self):
        return self._conexao.execute( "SELECT * FROM produto" ).fetchall()