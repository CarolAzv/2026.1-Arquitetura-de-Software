from app.services.conexao import Conectar
 

class ProdutoDAO:
    def __init__(self):
        self._conexao = Conectar()
 
 
    def produtoIncluir(self, produto):
        return self._conexao.execute(
            "INSERT INTO Produto (descricao, preco_unitario, quantidade_estoque, categoria_id) VALUES (?, ?, ?, ?)",
            (produto.descricao, produto.preco_unitario, produto.quantidade_estoque, produto.categoria_id)
        ).lastrowid
 
 
    def produtoAlterar(self, produto):
        return self._conexao.execute(
            "UPDATE Produto SET descricao = ?, preco_unitario = ?, quantidade_estoque = ?, categoria_id = ? WHERE id = ?",
            (produto.descricao, produto.preco_unitario, produto.quantidade_estoque, produto.categoria_id, produto.id)
        ).rowcount
 
 
    def produtoExcluir(self, produto):
        return self._conexao.execute( "DELETE FROM Produto WHERE id = ?", (produto.id,) ).rowcount

 
    def produtoObter_por_id(self, id):
        return self._conexao.execute( "SELECT * FROM Produto WHERE id = ?", (id,) ).fetchone()
 
 
    def produtoListar(self):
        return self._conexao.execute(
            "SELECT Produto.id, Produto.descricao, Produto.preco_unitario, Produto.quantidade_estoque, Produto.categoria_id, Categoria.descricao AS categoria_nome"
            " FROM Produto JOIN Categoria ON Produto.categoria_id = Categoria.id"
        ).fetchall()